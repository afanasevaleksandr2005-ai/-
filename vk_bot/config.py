import os

VK_TOKEN = os.environ.get("VK_TOKEN", "")
GROUP_ID = os.environ.get("VK_GROUP_ID", "")

# VK user IDs allowed to trigger admin commands (e.g. broadcast), comma-separated.
ADMIN_IDS = {
    int(uid) for uid in os.environ.get("VK_ADMIN_IDS", "").split(",") if uid.strip()
}

DB_PATH = os.environ.get("VK_BOT_DB_PATH", "bot.db")

# Delay between broadcast messages to stay under VK's flood-control limit.
BROADCAST_DELAY_SECONDS = 0.34
