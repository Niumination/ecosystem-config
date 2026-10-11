# Activating OAuth sign-in on a deployed app

For apps whose login is brokered by a hosted auth provider (Supabase Auth and similar): the provider holds the OAuth client id/secret, the app only calls `signInWithOAuth`. Four independent layers must all be right, and three of them are invisible from the app's own code. Check them in this order.

## The four layers

1. **App → provider handoff.** The app builds `redirectTo` from its own site URL. A fallback that reads a platform-injected deploy URL (`VERCEL_URL` and friends) points at the per-deployment host, which sits behind Deployment Protection — the provider will bounce the user to a Vercel sign-in page instead of the app. Set an explicit public site URL env var for the custom domain and confirm it is baked into the client bundle (see "Proving the redirect landed" below).
2. **Provider auth config.** `site_url` and the redirect allowlist. A freshly created project commonly still has `site_url = http://localhost:3000` and an empty allowlist, which fails every production redirect. Set both to the real domain and include the preview/localhost origins you actually use.
3. **Provider → upstream IdP callback.** The IdP is registered against the **provider's** callback (`https://<project-ref>.supabase.co/auth/v1/callback`), not your app's `/auth/callback`. Pointing the IdP at your own domain is the single most common cause of `redirect_uri_mismatch`.
4. **App callback route.** `/auth/callback` must exchange the code for a session. Usually already correct — read it before touching config.

## Probing without a browser

You can drive the provider's authorize endpoint and inspect the `Location` header — this proves layers 2 and 3 without any login:

```python
# suppress redirects so the 302 Location is readable
class NR(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NR)
url = f'https://<ref>.supabase.co/auth/v1/authorize?provider=github&redirect_to=https://<domain>/auth/callback'
try: op.open(url, timeout=30)
except urllib.error.HTTPError as e:
    print(e.code, e.headers.get('location'))
```

- **302 to the IdP's authorize URL** = layers 1–3 wired. Read the `redirect_uri` query parameter in that Location: it should be the provider's callback, and its `client_id` should match the one in the provider's auth config.
- **302 to the IdP's error page** = the IdP rejected the request. Decode the error to get the real reason.

### Decoding a Google error

Google returns `https://accounts.google.com/signin/oauth/error?authError=<base64url>`. The payload is protobuf-shaped; strip non-printable bytes and read the strings — it names the exact `redirect_uri` it rejected:

```python
import base64, re, urllib.parse
raw = base64.urlsafe_b64decode(urllib.parse.unquote(auth_error_param) + '=' * (-len(x) % 4))
print(re.sub(r'[^\x20-\x7e\u00a0-\uffff]', ' ', raw.decode('utf-8', 'ignore')))
```

Expect a message naming the missing URI and pointing at the Cloud Console — that is the fix, not a code change.

### GitHub does not validate pre-login

GitHub returns 302 to `github.com/login?client_id=...` for **both** a registered and a bogus `redirect_uri`, so a probe cannot confirm its callback registration. Say so plainly and hand the owner the exact URL to check in the app settings, rather than implying it verified. A wrong GitHub callback only surfaces after the user authenticates, as an error on the IdP's redirect back.

### Provider-specific: Google needs the exact URI registered

Google validates the redirect URI against the Cloud Console registration before login and fails hard with `redirect_uri_mismatch`. Add `https://<project-ref>.supabase.co/auth/v1/callback` under Authorized redirect URIs. Changes propagate in about a minute. The fix is owner-only: it needs console access you do not have.

## Proving the redirect landed (baked, not just set)

Setting a `NEXT_PUBLIC_*` site URL in the deploy platform is not proof it reached the client — the var must exist at build time and the redeploy must have run after it was set. Grep the shipped bundle:

```python
# fetch /masuk (or any page), collect /_next/static/... chunk URLs from the HTML,
# then fetch each chunk and search for the custom domain
for c in chunks:
    js = fetch(base + c)
    if '<domain>/auth/callback' in js:
        print('baked into', c)
```

Finding the domain plus the callback path inside a JS chunk proves the app is handing the provider the right `redirect_to`. Absence means the redeploy did not pick the var up.

## Pitfalls

- **Read the auth config before changing anything.** Providers may already be enabled with valid credentials, and the real fault is only `site_url`/allowlist. Re-adding credentials you already have risks invalidating a working client.
- **`site_url` is used for email links and redirect defaults**, so a localhost value also breaks magic-link/OTP emails, not just OAuth. Fix it once for all auth flows.
- **A per-deployment URL in the app's own redirect fallback is a config bug, not a protection bug.** Do not disable Deployment Protection to "fix" it; set the public site URL.
- **Separate the layers in your report.** "Provider enabled", "callback registered", "app env baked", and "end-to-end login works" are four different claims. Only the last one is a working login, and it needs a real user click.
- **Anything requiring console access stays an owner action.** State the exact URL and the exact value to paste; do not describe it as done.
