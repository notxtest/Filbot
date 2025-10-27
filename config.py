import os

# Bot Configuration
API_ID = int(os.getenv("API_ID", 23566820))
API_HASH = os.getenv("API_HASH", "3094c1bb23a29c3c3db3587bf2ab8679")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8021675724:AAFjluR96BQRGHqwEPVfJTsyMdF7p0e3qzw")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://krishnaonly999:Krishdiya07@cluster0.h4rzpxv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Admin Configuration
ADMIN_ID = int(os.getenv("ADMIN_ID", 7171541681))
OTHER_ADMINS = [int(x) for x in os.getenv("OTHER_ADMINS", "8190398973,6496242324,8060017785,6772161432").split(",")]

# Logs Channel
LOGS_CHANNEL = int(os.getenv("LOGS_CHANNEL", -1003109116424))

# Database Name
DB_NAME = os.getenv("DB_NAME", "anime_filter_bot")

# Bot Details
BOT_USERNAME = os.getenv("BOT_USERNAME", "Siesta_Anime_FilterBot")
BOT_NAME = os.getenv("BOT_NAME", "Siesta Anime Filter Bot")

# Images
START_IMAGE = os.getenv("START_IMAGE", "https://graph.org/file/0b1133612eff647e661ea-95ee6b8b644e7e8675.jpg")
HELP_IMAGE = os.getenv("HELP_IMAGE", "https://graph.org/file/a56c098b2449c7e447585-4fc9a5a6c6ab95012e.jpg")
CMD_IMAGE = os.getenv("CMD_IMAGE", "https://graph.org/file/9b84ec73a967e27c15de9-d1e9e4da7828acaedc.jpg")
PING_IMAGE = os.getenv("PING_IMAGE", "https://graph.org/file/8b60e9b5e97fef5fd9527-fa78d1ad522cc663a7.jpg")
STATS_IMAGE = os.getenv("STATS_IMAGE", "https://graph.org/file/bc527ce98ebbdcd4554f3-1b127b2e2646da8ada.jpg")

# Links
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/Multiverse_Anime_Gc")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "https://t.me/Anime_frenzy")
MOVIES_CHANNEL = os.getenv("MOVIES_CHANNEL", "https://t.me/+t_3x_LtwTWdkODg9")
