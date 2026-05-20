# YQ Web Services

Singapore websites that actually do something. Built by an engineer, owned by you.

Live at: https://web.yqservices.org

## What this is

The umbrella landing site for YQ Web Services — a sub-brand of YQ Services.
Pricing, demos, project intake form. Built as a single-file HTML app for fast
loading and easy hosting.

## Stack

- Static HTML/CSS/JS (no build step)
- Supabase Postgres + RPC for the intake form
- Telegram bot for new-brief notifications (`@Yiqin88_bot`)
- Hosted on GitHub Pages with custom domain

## Local development

Just open `index.html` in a browser. No build, no dev server needed.

## Deployment

Push to `main` → GitHub Pages auto-deploys within 1–2 minutes.

## Architecture notes

- Form submits to Supabase RPC `submit_web_brief(payload jsonb)` (security definer)
- `web_briefs` table has RLS enabled with zero policies — anon can only call the RPC
- Postgres trigger `trg_notify_new_brief` fires `pg_net.http_post` to Telegram on insert
- Bot token lives in Supabase Vault, not in code

## License

Proprietary. © 2026 YQ Services.
