#!/bin/bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "usage: $0 /path/to/target-repo" >&2
    exit 1
fi

TARGET_REPO="$1"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_REPO="$(cd "$SKILL_DIR/../../.." && pwd)"

mkdir -p "$TARGET_REPO/scripts"

cp "$SOURCE_REPO/scripts/deploy-bot.sh" "$TARGET_REPO/scripts/deploy-bot.sh"
cp "$SOURCE_REPO/scripts/aca_env_secrets_agent.py" "$TARGET_REPO/scripts/aca_env_secrets_agent.py"
cp "$SOURCE_REPO/scripts/launch.sh" "$TARGET_REPO/scripts/launch.sh"

chmod +x "$TARGET_REPO/scripts/deploy-bot.sh" "$TARGET_REPO/scripts/launch.sh"

echo "Installed deploy assets into $TARGET_REPO/scripts"
