# OpenExam Supabase SaaS Mode

Local mode remains the default:

```powershell
$env:OPENEXAM_MODE = "local"
```

To activate the optional SaaS bridge, configure `SUPABASE_URL`,
`SUPABASE_PUBLISHABLE_KEY`, and server-only `SUPABASE_SERVICE_ROLE_KEY`, then set:

```powershell
$env:OPENEXAM_MODE = "supabase"
```

SaaS API requests require a Supabase access-token bearer JWT. The Next.js
middleware refreshes SSR cookies only when browser-safe Supabase variables are
present.

Transfers are always explicit:

- `GET /api/export` creates a versioned local bundle.
- `POST /api/import` defaults to a cloud-to-local dry run.
- `POST /api/import` with `direction=local-to-cloud` defaults to a cloud-upload
  dry run and requires an organization ID.

There is no automatic bidirectional synchronization.
