#!/usr/bin/env bash
set -euo pipefail

U="${WGER_ADMIN:-admin}"
P="${WGER_PASS:-adminadmin}"

curl -sf -X POST "http://localhost/api/v2/login/" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$U\",\"password\":\"$P\"}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])"
