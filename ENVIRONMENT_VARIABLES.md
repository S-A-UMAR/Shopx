# ShopX environment variables

Use these exact names in **Vercel → Settings → Environment Variables**.
Do **not** include backticks or spaces in variable names.

## Required
- `SECRET_KEY`
- `DB_HOST`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- `DB_PORT` (usually `4000` for TiDB)

## Optional alternative
- `DATABASE_URL` (if set, this is used instead of the split DB vars)

## Optional integrations
- `RESEND_API_KEY`
- `PAYSTACK_PUBLIC_KEY`
- `PAYSTACK_MERCHANT_EMAIL`

## Runtime
- `FLASK_DEBUG` (`true`/`false`)
- `PORT` (local only, default `5000`)
