# Government API Audit — CRUDBooster / Laravel

Systematic approach for probing CRUDBooster-based or general Laravel government APIs when documentation is limited and external access is restricted.

## Prerequisites

- **Postman collection** (if available) → parse JSON to extract endpoints
- **Base URL** — typically `sapa.acehtengahkab.go.id` or similar
- **Secret key** (if provided) — may be MD5 hash (32 hex chars), Laravel API token, or CRUDBooster apikey
- **Browser access** from user (they may have super admin access)

## Phase 1 — Platform Identification

| Signal | What it means |
|--------|--------------|
| Laravel debug page (`/vendor/laravel/framework`) | **Laravel** app |
| `CRUDBooster` in login page HTML | **CRUDBooster** admin generator |
| Error: Route `[login] not defined` | Laravel auth middleware active, no `login` named route |
| `Page Expired` with CSRF mismatch | Laravel **VerifyCsrfToken** middleware |
| `nginx` in 404 page | Standard nginx reverse-proxy |
| `Forbidden Access!` consistently regardless of auth method | Likely **IP restriction** — server blocks external API requests |

### Key endpoints to check

```bash
# Laravel Sanctum CSRF (gets session + xsrf cookies)
curl -s "https://<host>/sanctum/csrf-cookie" -c cookies.txt

# CRUDBooster login page
curl -s "https://<host>/admin/login"

# Common api paths
/api/daftar_data?tahun=2026
/api/user                    # 500 = exists
/api/data
/api/dataset
```

## Phase 2 — Authentication Probe Matrix

Try each method. Record results systematically. "Forbidden Access!" across all methods **without** the app distinguishing between different errors is a strong IP-restriction signal.

| Method | Header/Param | CRUDBooster | Laravel Sanctum |
|--------|-------------|-------------|-----------------|
| Bearer token | `Authorization: Bearer <key>` | ❌ (not default) | ✅ (personal_access_tokens) |
| X-API-Key | `X-API-Key: <key>` | ⚠️ (depends on config) | ❌ |
| X-Authorization-Token | `X-Authorization-Token: <key>` | ✅ (CRUDBooster native) | ❌ |
| apikey param | `?apikey=<key>` | ✅ (CRUDBooster native) | ❌ |
| CB_API_KEY header | `CB_API_KEY: <key>` | ✅ (CRUDBooster native) | ❌ |
| Laravel session cookie | Cookie from `/sanctum/csrf-cookie` | ❌ | ✅ (after login) |
| Basic auth | `-u "user:<key>"` | ❌ | ❌ |
| form POST token | `POST -d "token=<key>"` | ❌ | ❌ |
| api_token query | `?api_token=<key>` | ❌ | ✅ (Laravel default) |
| X-CSRF-TOKEN | `X-CSRF-TOKEN: <url_decoded_token>` | ❌ | Only with valid session |

**Note:** URL-decode XSRF-TOKEN cookie value before using it (it's base64 with `%3D` → `=` padding).

## Phase 3 — Diagnosing IP Restriction

Key indicators the API is **IP-restricted** (not just wrong auth):

```
{"api_status":0,"api_message":"Forbidden Access!"}
```

This response is **identical** across all auth methods, all endpoints, with or without session. A working API with wrong auth would return 401/403 with different messages (e.g., "Unauthenticated.", "Invalid token", "Wrong credentials"). Same response for every request = the web server (nginx/Cloudflare) is blocking the IP before it reaches Laravel.

### How to confirm

1. Check if same server serves web pages (not API) correctly
2. Get Laravel session cookie successfully (`/sanctum/csrf-cookie` -> 204/200)
3. Try API with the session cookie -> still "Forbidden"
4. Try API with **all** auth methods above -> all fail with same message

When web works but API doesn't, the web routes may have `laraver_session` auth but the API routes are IP-whitelisted in nginx config.

## Phase 4 — Working Around IP Restriction

Options from most to least practical:

1. **User logs in via browser, checks Network tab** — Login to CRUDBooster admin (`/admin/login`) as super admin, open DevTools, find API calls to copy exact headers used
2. **User exports data manually** — Download JSON/CSV from admin panel
3. **User provides DB credentials** — Direct postgreSQL/MySQL access (if available)
4. **Check API from internal network** — If agent can run from within Aceh Tengah network (e.g., via SSH tunnel or on-site)

## Phase 5 — Data Schema Discovery (when API works)

### CRUDBooster data structure conventions

CRUDBooster generates admin panels from database tables. Common tables:

| Table | Purpose |
|-------|---------|
| `cb_users` | Admin users (API keys stored here) |
| `module` | CRUDBooster module definitions |
| `settings` | App settings |
| Custom tables | Named per module (e.g., `daftar_data`, `indikator`, `opd`) |

### If you have DB access

```sql
-- List tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Check user for API keys
SELECT id, name, email, apikey FROM cb_users;

-- Explore CRUDBooster modules
SELECT id, name, table_name, path FROM module;
```

### If API works (CRUDBooster native API)

```bash
# Get API key from DB → then:
curl -s "https://<host>/api/daftar_data?apikey=<apikey>&tahun=2026"
curl -s "https://<host>/api/<module>?apikey=<apikey>"
```

## Specific: SAPA System (Aceh Tengah)

| Property | Value |
|----------|-------|
| Platform | CRUDBooster on Laravel |
| Server path | `/www/wwwroot/SPAD/` |
| IP | `123.108.103.51` |
| API endpoint | `GET /api/daftar_data` |
| Params | `id`, `id_kode_indikator`, `id_opds`, `jadwal_pemutakhiran`, `satuan`, `tahun`, `variabel` |
| **sapa_opds (baru)** | `GET /api/sapa-opds` — params: `id` (int, required), `nama_opd` (string, required). Respon: `{api_status, api_message, data: [{id, nama_opd}]}` |
| Web admin | `/admin/login` (AdminLTE theme) |
| Secret key | `16061a05aaac461e78983a28e19cda9f` (MD5) — digunakan via `POST /api/get-token` |
| API status | ⛔ IP-restricted — cannot call externally. Auth flow: `POST /api/get-token` with `secret=` field → Bearer token → use for all API calls |

## Phase 6 — CRUDBooster API Generator & Secret Key

When the admin panel has two features — **Secret Key** and **API Generator** — the flow is:

### Admin paths

| Feature | Path | Usage |
|---------|------|-------|
| **API Generator** | `/admin/api_generator/generator` | Select table + action type → generates `/api/{name}` route |
| **Secret Key** | `/admin/api_generator/screet-key` | Manage global secret keys (Active/Nonactive toggle + Delete) |
| **API Documentation** | `/api-documentation` | Lists all generated endpoints with params, headers, response schemas |

### API Generator workflow

1. User selects a **table** from dropdown (e.g., `opds`, `kode_indikator`)
2. Selects **Action Type**: `Listing` (GET list), `Detail/Read` (GET by id), `Create/Add` (POST), `Update` (PUT), `Delete` (DELETE)
3. Clicks **Generate** (or Save)
4. System creates a new route at `/api/{name}` (e.g., `/api/sapa_opds`)

**After generation:** The route may not be immediately accessible until:
- User sets **mandatory parameters** and enables the API (toggle **Enable** to Yes)
- Route cache cleared (only if `php artisan route:cache` was used)

### Custom get-token auth (Bear token flow)

CRUDBooster-generated APIs typically check for `X-API-Key` or `apikey` param. However, some deployments wrap a **custom auth flow** on top:

```
1. POST /api/get-token          # Or /get-token (relative to API base URL)
   Body: secret=<md5_key>
   Response: { api_status, api_message, data: { access_token, expiry } }

2. GET /api/sapa_opds           # Any generated endpoint
   Headers: Authorization: Bearer <access_token>
```

**Where to find the auth endpoint:**
1. Go to `/api-documentation` page
2. Look for **"Authentication (Request Token)"** row
3. Click it — the hidden `detail_api` div shows the URL (often in an `<input>` element with `onClick="this.setSelectionRange(...)"`)
4. The URL is typically **relative** to the API base URL shown on the same page
5. Full URL = `{API_BASE_URL}{auth_path}`

**Important:** The auth endpoint URL may be documented as `/get-token` (relative to root) but actually live at `/api/get-token` (relative to base URL `/api`). Try both.

### Secret Key activation flow

The Secret Key page (`/admin/api_generator/screet-key`) shows a list of keys with toggle-able status:

| Toggle Label | Meaning | Action |
|-------------|---------|--------|
| **Nonactive** | Key is disabled | Click to toggle → Active |
| **Active** | Key is enabled | Ready for use |

Key values are typically 32-char hex strings (MD5 hash format). The **Active/Nonactive** label is often a clickable toggle, not just a status display.

**Important:** Activating the key on the Screet Key page does NOT automatically make it work with `/api/get-token`. The get-token endpoint may check a different credential source (e.g., user profile API key, a separate `api_keys` table).

### If get-token fails with "Credential invalid!"

Possible causes:
1. The secret key is for a different purpose (e.g., Google API, SPLP gateway) — not for this CRUDBooster install
2. The auth endpoint checks a **user password** or **user-specific API key**, not the global secret key
3. The secret key needs to be **registered** in a different admin section (e.g., user profile → API Key field)
4. The session cookie (from browser login) is required alongside the key

**Check with the user:**
- Does the admin panel have a separate **Users** menu? Edit super admin profile → look for "API Key" field
- Is there an **API Keys** menu section separate from Secret Key?
- Can they access the generated API endpoint directly from their **browser** (while logged in)?

## Phase 6b — CRUDBooster Privilege Management for API Access

After generating an API via **API Generator**, the endpoint returns `Forbidden Access!` even with a valid token. This is **not** an IP restriction — the API route exists and your auth works, but the **privilege system** blocks it.

### The missing step

1. Go to **Privileges / Roles** (`/admin/privileges`)
2. Click **Add Privilege**
3. Fill form:
   - **Privilege Name**: match the API slug (e.g., `sapa_opds`)
   - **Set as Superadmin**: Yes
   - **Privileges Configuration**: ignore module checkboxes (they're for admin panel, not API)
4. Save → Creates entry in `crud_privileges` table

### After privilege creation — still blocked?

If `Forbidden Access!` persists, the generated endpoint has **no access rule** allowing external API calls. Two resolution paths:

#### Path A: "Is Public" checkbox (preferred)

Back in Edit Privilege → scroll below the module permissions table. Look for:
- **Is Public** checkbox
- **Public API** toggle
- **Allow API Access** checkbox

If visible → check it → Save. Test immediately.

#### Path B: Database-level (when "Is Public" is hidden)

Some CRUDBooster versions hide the "Is Public" checkbox from the form. Fix via direct DB:

```sql
UPDATE crud_privileges SET is_public = 1 WHERE name = 'sapa_opds';
```

Or if using CRUDBooster's `api_key` system:

```sql
UPDATE cms_privileges SET is_public = 1 WHERE name = 'sapa_opds';
```

**Table naming varies** by CRUDBooster version:
| Table | Version |
|-------|---------|
| `crud_privileges` | Newer CRUDBooster 7+ |
| `cms_privileges` | Older CRUDBooster versions |
| `cb_privileges` | Some forks |

Check which table exists: `SHOW TABLES LIKE '%privileges%'`

#### Path C: Grant via user's API Key

If the `/api/get-token` endpoint checks a per-user API key (not the global secret key):

1. Go to **Users Management** → Edit super admin profile
2. Look for **API Key** or **API Token** field
3. Copy or generate the key
4. Use that key as the `secret` parameter for `/api/get-token`

### "Is Public" checkbox invisible — form inspection

In the Edit Privilege form, if the page ends after the module checkboxes table (View/Create/Read/Update/Delete columns), the "Is Public" field may be:
- **Hidden via CSS** (`display:none`) — check page source
- **Removed by CRUDBooster version** — some versions hide it when modules exist
- **Replaced by a "Set API Access" section** further down (scroll more)

**Quick test:** Open browser DevTools → search page HTML for `is_public` or `public`. If found but hidden, set it via database.

### Pitfall — Module permissions don't affect API access

The columns in **Privileges Configuration** (View/Create/Read/Update/Delete) control the **admin panel** module access, NOT API endpoint access. Checking them all does NOT fix `Forbidden Access!`. You need either `is_public = 1` or a specific API role grant.

## Phase 6c — Label Merah "Authentication (Request Token)" di API Documentation

Halaman `/api-documentation` CRUDBooster menampilkan daftar endpoint API. Setiap endpoint punya label status autentikasi:

| Label | Warna | Arti |
|-------|-------|------|
| **Authentication (Request Token)** | 🔴 Merah | Endpoint WAJIB dikirim dengan `Authorization: Bearer <token>`. Token didapat dari endpoint `/api/get-token`. |
| *(tanpa label)* | — | Endpoint publik, bisa dipanggil langsung tanpa token. |

**Cara membaca:**
1. Klik label merah → `detail_api` div muncul → di dalamnya ada URL endpoint + parameter
2. Endpoint dengan label merah TIDAK akan bekerja tanpa Bearer token
3. Endpoint tanpa label bisa langsung dites dengan curl biasa

**Pitfall — "Authentication (Request Token)" hanya visual cue.** Label ini adalah bagian dari template CRUDBooster API Documentation — tidak mengontrol akses. Endpoint tetap butuh token meskipun labelnya merah, dan endpoint tanpa label merah TETAP bisa di-protect oleh privilege system.

## Phase 7 — Error Message Decoding

| Response | Likely Cause | Next Step |
|----------|-------------|-----------|
| `{"api_status":0,"api_message":"Forbidden Access!"}` | IP restriction or nginx-level block | Cannot fix externally; need browser access from internal network |
| `{"api_status":0,"api_message":"The secret field is required."}` | Auth endpoint found — missing `secret` parameter | Send `secret=<value>` in POST body |
| `{"api_status":0,"api_message":"Credential invalid!"}` | Auth endpoint processing request — wrong secret value | Check the credential source (see above) |
| `{"message":"Unauthenticated."}` | Laravel auth middleware active — no valid session/token | Need Bearer token or API key |
| 404 with nginx HTML page | Route does not exist at that path | Check `/api-documentation` for correct endpoint name |
| 500 with Laravel debug page | Route exists but code error | Valuable info: server path, PHP version, framework version leaked in error output |

## Pitfalls

- **"Forbidden Access!" is not a normal Laravel response.** Laravel returns `{"message": "Unauthenticated."}` for 401 and Symfony HTML for 403. The JSON `{"api_status":0,"api_message":"Forbidden Access!"}` is CUSTOM middleware — likely IP whitelist, not auth.
- **CRUDBooster API keys are stored in `cb_users.apikey`** — not in `personal_access_tokens`. Check both tables.
- **XSRF-TOKEN cookie is URL-encoded** — must decode before using in `X-XSRF-TOKEN` header. Example: `%3D` → `=` (base64 padding).
- **Session alone is not enough.** Laravel middleware stack checks both session AND API token/IP for API routes. Getting a session cookie doesn't give API access.
- **Postman collections may be incomplete** — the provided collection may only have headers and no auth config. Variables section (often stripped on export) may contain base_url, api_key, etc. Always re-check with the user if collection looks bare.
- **API doc URL field is easy to misread.** The `value="/get-token"` in the input field shows a path but it may be relative to a different base than the API base URL. Always test with and without the base URL prefix.
- **After generating an API, the route may still return 404** if the API Generator didn't fully save. Check:
  - Were mandatory parameters set?
  - Was the API enabled (toggle to "Yes")?
  - Has the route cache been cleared? (If user has no `php artisan` access, this may block routes permanently.)
- **"The secret field is required." vs "Credential invalid!"** — The first confirms the endpoint found your `secret` parameter. The second means the value was checked and rejected. This is **progress** — the endpoint is working, you just need the right credential.
- **The `/api-documentation` page is the single source of truth** for a CRUDBooster deployment. It lists every registered API endpoint with exact URL, method, headers, and parameter definitions. Always consult it before guessing routes.
- **Terminal tool may mask secret key values in curl commands.** If you run `curl -d "secret=16061a..."` via terminal(), the tool may replace the hex string with `***` — silently sending the wrong value to the server. The result: `Content-Length` mismatch, or the server gets a masked value and returns `Credential invalid!`. Workaround: write the secret to a temp file and use `$(<file)` expansion, or use `execute_code` + Python `subprocess.run()` for auth commands.
- **"Authentication (Request Token)" label merah di API Documentation** berarti endpoint tersebut WAJIB dikirim dengan `Authorization: Bearer <token>`. Endpoints tanpa label merah bisa langsung dipanggil. Label ini adalah visual cue dari CRUDBooster untuk membedakan public vs authenticated endpoints — tetapi TIDAK mengontrol akses sebenarnya. Endpoint tetap butuh privilege `is_public` atau role grant.
- **CRUDBooster Edit Privilege form — "Is Public" checkbox tidak selalu muncul.** Jika setelah membuat privilege, endpoint masih `Forbidden Access!` dan tidak ada checkbox "Is Public" di form edit, solusinya adalah UPDATE langsung di database: `UPDATE crud_privileges SET is_public = 1 WHERE name = 'sapa_opds';`. Cek nama tabel yang benar dulu (`SHOW TABLES LIKE '%privileges%'`).
- **Setelah generate API di API Generator, user harus membuat privilege secara manual** — API Generator hanya membuat route, tidak membuat aturan akses. Tanpa privilege entry, endpoint selalu `Forbidden Access!` meskipun token valid. Ini adalah step yang paling sering terlewat.
