# Wiring up Supabase (accounts + a shared recipe database)

Right now the live site (https://openfeld.github.io/oppidu-recipes/) still
runs in **local-only mode**: every submission is saved to that one
browser's `localStorage` and nobody else can see it. This is the one-time
setup to switch it to real, shared accounts.

## 1. Create the project

This has to be done by a person, not Claude — account/project creation on
a third-party service isn't something an assistant can do on your behalf.

1. Go to [supabase.com](https://supabase.com) and sign in (or create an
   account — a fresh account gets its own 2 free projects, independent of
   any other Supabase account/project you already have).
2. **New project** → any name (e.g. "oppidu-recipes") → any region → set
   a database password (write it down somewhere safe; you likely won't
   need it day-to-day, `supabase-js` uses the URL + anon key below
   instead).

## 2. Run the schema

1. In the project, open **SQL Editor** → **New query**.
2. Paste the entire contents of [`schema.sql`](schema.sql) and click **Run**.
   Safe to re-run later if this file changes — every statement is
   idempotent.

This creates two tables (`profiles`, `recipes`) with row-level security
already configured: anyone can browse recipes, only a signed-in user can
submit one (and only as themselves), and a recipe's owner — or an admin —
can edit or delete it.

## 3. Get the URL + anon key

**Settings → API** in the project. You need two values:

- **Project URL** (`https://xxxxxxxx.supabase.co`)
- **anon / public key** (a long JWT starting `eyJ...`)

Both are safe to put in client-side code — that's what they're for. Do
**not** use the `service_role` key or the database password anywhere in
the app; those bypass row-level security entirely.

Open `preview_template.html`, find:

```js
const SUPABASE_URL = "";
const SUPABASE_ANON_KEY = "";
```

and fill in your two values. Then rebuild (`python3 scripts/build_preview.py`)
and push — `preview.html` and `index.html` both pick up the change.

## 4. Sign up, then become the admin

1. Open the live site, click **Sign in** → **Create account**, and sign
   up with whatever email/password you want to manage the app with. (If
   the project has email confirmation on by default, confirm via the link
   Supabase emails you before signing in.)
2. Back in the SQL Editor, run:

   ```sql
   update public.profiles set role = 'admin' where email = 'you@example.com';
   ```

   using the email you just signed up with. Reload the site — you'll see
   an **Admin** badge next to your email in the header, and a **Delete
   recipe** button on every recipe's detail view, not just your own.

That's the whole "give me a super admin login" step: your login is
whatever email+password you chose in step 1 above — nothing to memorize
that Claude generated for you, since account passwords are exactly the
kind of credential an assistant shouldn't be the one setting.

## Handling problem accounts

The in-app admin role covers **recipe moderation** — deleting any recipe,
for any reason. It does not (and shouldn't) reach into people's accounts
directly. For that, Supabase's own dashboard already has everything
needed, no code required:

**Authentication → Users** in your Supabase project lets you, per user:
search by email, see their sign-up/last-sign-in time, **disable** their
account (blocks sign-in without deleting their data), **delete** the
account outright, or send a password-reset email on their behalf. This is
also where you'd go if someone's account is "stuck" (e.g. an unconfirmed
signup) or you need to confirm an email manually.

## Multiple admins

Repeat step 4 for anyone else's email who should have admin access — role
is just a column, not a separate login flow.

## More than one project sharing this database

If you ever want the *same* Supabase project backing more than one app,
put each app's tables in their own Postgres **schema** (not the default
`public` one) rather than mixing tables — keeps the two logically
separated even inside one project. Not needed for the setup above, and
not something to do without deciding it deliberately.
