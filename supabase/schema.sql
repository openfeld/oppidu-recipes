-- Oppidu Recipes — Supabase schema.
--
-- Run this once, in full, in your Supabase project's SQL Editor
-- (Dashboard → SQL Editor → New query → paste → Run). Safe to re-run:
-- every statement is idempotent (`if not exists` / `create or replace`).
--
-- What this creates:
--   1. public.profiles   — one row per signed-up user (role, kitchen name)
--   2. public.is_admin()  — helper used by the RLS policies below
--   3. a trigger that adds a profiles row automatically on sign-up
--   4. public.recipes    — every submitted recipe, shared across all users
--   5. RLS policies for both tables
--
-- This is intentionally separate from the seed recipes: the 19 curated
-- seed dishes stay bundled in the app itself (see preview_template.html's
-- SEED_RECIPES) and are never written here — this table holds only what
-- real users submit through the app.

-- ---------------------------------------------------------------------
-- 1. profiles
-- ---------------------------------------------------------------------
create table if not exists public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  email text,
  kitchen_name text,
  role text not null default 'user' check (role in ('user', 'admin')),
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

-- ---------------------------------------------------------------------
-- 2. is_admin() — security definer so it can read public.profiles
-- without re-triggering that table's own RLS policies (which call this
-- same function) and causing infinite recursion. This is the standard
-- Supabase-recommended pattern for a role check used inside RLS.
-- ---------------------------------------------------------------------
create or replace function public.is_admin()
returns boolean
language sql
security definer
set search_path = public
stable
as $$
  select exists (
    select 1 from public.profiles where id = auth.uid() and role = 'admin'
  );
$$;

drop policy if exists "profiles are viewable by their owner or an admin" on public.profiles;
create policy "profiles are viewable by their owner or an admin"
  on public.profiles for select
  using (auth.uid() = id or public.is_admin());

drop policy if exists "profiles are updatable by their owner or an admin" on public.profiles;
create policy "profiles are updatable by their owner or an admin"
  on public.profiles for update
  using (auth.uid() = id or public.is_admin());

-- ---------------------------------------------------------------------
-- 3. Auto-create a profile row the moment someone signs up.
-- ---------------------------------------------------------------------
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, email)
  values (new.id, new.email);
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ---------------------------------------------------------------------
-- 4. recipes — mirrors schema/recipe.schema.json's fields 1:1, so the
-- app's RecipeStore.save()/list() can read/write these rows with no
-- translation layer. jsonb columns hold whatever the JS side already
-- builds as plain arrays/objects (supabase-js serializes automatically).
-- ---------------------------------------------------------------------
create table if not exists public.recipes (
  id text primary key,
  title text not null,
  description text not null default '',
  cuisine text not null,
  category text not null,
  servings integer not null,
  prep_time_minutes integer not null default 0,
  cook_time_minutes integer not null default 0,
  difficulty text not null default 'medium',
  ingredients jsonb not null default '[]'::jsonb,
  instructions jsonb not null default '[]'::jsonb,
  tags jsonb not null default '[]'::jsonb,
  dietary jsonb not null default '[]'::jsonb,
  source text not null default 'user-submitted',
  status text not null default 'submitted',
  submitted_by uuid references public.profiles (id) on delete set null,
  submitted_kitchen text,
  photos_needed jsonb not null default '[]'::jsonb,
  translations jsonb,
  created_at timestamptz not null default now()
);

alter table public.recipes enable row level security;

-- Anyone — signed in or not — can browse every submitted recipe.
drop policy if exists "recipes are viewable by everyone" on public.recipes;
create policy "recipes are viewable by everyone"
  on public.recipes for select
  using (true);

-- Only a signed-in user can submit, and only ever as themselves.
drop policy if exists "authenticated users can submit their own recipes" on public.recipes;
create policy "authenticated users can submit their own recipes"
  on public.recipes for insert
  with check (auth.uid() = submitted_by);

-- A recipe's own submitter can edit/delete it; an admin can edit/delete
-- ANY recipe (moderation — see the README section on becoming an admin).
drop policy if exists "owners or admins can update a recipe" on public.recipes;
create policy "owners or admins can update a recipe"
  on public.recipes for update
  using (auth.uid() = submitted_by or public.is_admin());

drop policy if exists "owners or admins can delete a recipe" on public.recipes;
create policy "owners or admins can delete a recipe"
  on public.recipes for delete
  using (auth.uid() = submitted_by or public.is_admin());
