#!/usr/bin/env bash
# Reproducible install on a fresh Debian/Ubuntu VM (tested target: Ubuntu 24.04, e2-standard-2).
# Usage (as root): REPO_URL=https://github.com/chawlavaibhav/media-intelligence REF=<branch-or-commit> ./install.sh
# Creates no cloud resources; the VM itself, DNS and billing are the founder's decision.
set -euo pipefail
: "${REF:?set REF to the branch or commit to deploy}"
REPO_URL="${REPO_URL:-https://github.com/chawlavaibhav/media-intelligence}"
apt-get update -q
apt-get install -y -q python3 python3-yaml python3-jinja2 python3-cryptography python3-pil python3-numpy libraqm0 ffmpeg librsvg2-bin \
    fonts-dejavu-core fonts-noto-core git sqlite3 caddy
id mi >/dev/null 2>&1 || useradd --system --home /srv/mi --shell /usr/sbin/nologin mi
mkdir -p /srv/mi/data/backups /etc/mi
if [ ! -d /srv/mi/app/.git ]; then git clone --filter=blob:none "$REPO_URL" /srv/mi/app; fi
git -C /srv/mi/app fetch -q origin "$REF" && git -C /srv/mi/app checkout -q FETCH_HEAD
chown -R mi:mi /srv/mi/data
if [ ! -f /etc/mi/mi.env ]; then
  cp /srv/mi/app/deploy/mi.env.example /etc/mi/mi.env
  sed -i "s/^MI_SECRET_KEY=.*/MI_SECRET_KEY=$(python3 -c 'import secrets;print(secrets.token_hex(32))')/" /etc/mi/mi.env
fi
chown root:mi /etc/mi/mi.env && chmod 0640 /etc/mi/mi.env
cp /srv/mi/app/deploy/mi-web.service /srv/mi/app/deploy/mi-worker.service /srv/mi/app/deploy/mi-backup.service \
   /srv/mi/app/deploy/mi-backup.timer /etc/systemd/system/
systemctl daemon-reload
# smoke BEFORE the services take traffic: media engine on this host + dry jobs + backup/restore (USD 0)
sudo -u mi env PYTHONPATH=/srv/mi/app python3 -m product.smoke
systemctl enable --now mi-web mi-worker mi-backup.timer
echo "Installed. Next: edit /etc/mi/mi.env (hostname, keys), put deploy/Caddyfile at /etc/caddy/Caddyfile, systemctl reload caddy,"
echo "then: sudo -u mi env \$(cat /etc/mi/mi.env | xargs) PYTHONPATH=/srv/mi/app python3 -m product.admin init-operator --email <you>"
