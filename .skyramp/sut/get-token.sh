#!/usr/bin/env bash
set -euo pipefail

# wger 2.7+ removed the /api/v2/login/ HTTP endpoint. Obtain the DRF token
# directly via Django shell. Use bash -c with 2>/dev/null inside the container
# so Django startup messages (system checks, warnings) go to stderr and are
# suppressed, leaving only the 40-char hex token key on stdout.
# DRF token keys are hex-only so stripping all whitespace is safe.
docker compose -f ./.skyramp/sut/docker-compose.testbot.yml exec -T web \
  bash -c 'python3 manage.py shell -c "
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
user = User.objects.get(username=\"admin\")
token, _ = Token.objects.get_or_create(user=user)
import sys; sys.stdout.write(token.key)
" 2>/dev/null' | tr -d '[:space:]'
