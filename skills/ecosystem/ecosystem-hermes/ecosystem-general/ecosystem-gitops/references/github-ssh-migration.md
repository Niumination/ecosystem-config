# GitHub SSH Migration — Post-Incident Recovery

When all repos were forced to HTTPS via `url."https://github.com/".insteadOf = git@github.com:` after SSH rejection, recovery to SSH:

1. Verify key: `ls ~/.ssh/id_rsa.pub` (reconstruct: `ssh-keygen -y -f ~/.ssh/id_rsa > ~/.ssh/id_rsa.pub`)
2. Check PAT scopes: `curl -I -H "Authorization: token $(cat vault/github-pat.md)" https://api.github.com/user | grep x-oauth-scopes` — need `admin:public_key` + `read:org`
3. Upload: `curl -X POST -H "Authorization: token $T" https://api.github.com/user/keys -d '{"title":"zaryu-mac-rsa-YYYYMMDD","key":"'"$(cat ~/.ssh/id_rsa.pub)"'"}'`
4. Verify: `ssh -T git@github.com` → `Hi <user>!`
5. Remove rewrite: `git config --global --unset url."https://github.com/".insteadOf`
6. Mass migrate HTTPS→SSH across ecosystem, verify counts SSH:46 HTTPS:0 + `git ls-remote` sample
Pitfall: `get-url` still shows HTTPS if global insteadOf remains — check `~/.gitconfig`.
