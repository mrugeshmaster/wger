#!/usr/bin/env bash
set -euo pipefail

# wger 2.7+ removed the /api/v2/login/ HTTP endpoint. Obtain the DRF token
# directly via Django shell — no HTTP roundtrip needed.
docker compose -f ./.skyramp/sut/docker-compose.testbot.yml exec -T web \
  python3 manage.py shell -c "
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
user = User.objects.get(username='admin')
token, _ = Token.objects.get_or_create(user=user)
import sys; sys.stdout.write(token.key)
" | tr -d '\r\n'
