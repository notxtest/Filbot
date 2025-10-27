from telebot import types
from config import START_IMAGE, HELP_IMAGE, CMD_IMAGE, PING_IMAGE, STATS_IMAGE
from config import SUPPORT_GROUP, UPDATE_CHANNEL, MOVIES_CHANNEL, BOT_NAME, BOT_USERNAME
from config import ADMIN_ID, OTHER_ADMINS, LOGS_CHANNEL
from db import update_user_data, get_user_count, get_group_count
from db import filters_collection, dm_filters_collection, get_dm_settings
import re
import time

def register_start_handlers(bot):
    
    # Helper function for inline keyboard
    def make_inline_keyboard(button_rows):
        ik = types.InlineKeyboardMarkup()
        for row in button_rows:
            ik.row(*row)
        return ik

    # Helper function for reply keyboard
    def make_reply_keyboard(rows):
        rk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for row in rows:
            rk.row(*[types.KeyboardButton(text) for text in row])
        return rk

    # Logs function
    def log_message(log_type: str, message: str, user_id: int = None, chat_id: int = None, 
                    username: str = None, first_name: str = None, chat_title: str = None, 
                    extra_data: str = ""):
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            log_text = f"""🪵 <b>LOG TYPE:</b> {log_type}
⏰ <b>TIME:</b> <code>{timestamp}</code>"""

            if user_id:
                log_text += f"\n👤 <b>USER ID:</b> <code>{user_id}</code>"
            
            if first_name:
                log_text += f"\n👨‍💼 <b>NAME:</b> {first_name}"
            
            if username:
                log_text += f"\n📎 <b>USERNAME:</b> @{username}" if username else "\n📎 <b>USERNAME:</b> No username"
            
            if chat_id:
                if chat_id == user_id:
                    log_text += f"\n💬 <b>CHAT:</b> Private Chat"
                else:
                    log_text += f"\n💬 <b>CHAT ID:</b> <code>{chat_id}</code>"
            
            if chat_title:
                log_text += f"\n🏷️ <b>GROUP:</b> {chat_title}"
            
            if message:
                log_text += f"\n📝 <b>MESSAGE:</b> {message}"
            
            if extra_data:
                log_text += f"\n📊 <b>EXTRA:</b> {extra_data}"

            bot.send_message(LOGS_CHANNEL, log_text, parse_mode="HTML")
            
        except Exception as e:
            print(f"Log message failed: {e}")

    # Anime keyboard handler private
    def anime_keyboard_handler_private(message):
        ANIME_KEYBOARD_LETTERS = [
            ["0","1","2","3","4","5","6","7","8","9"],
            ["A","B","C","D","E","F","G","H","I","J","K","L","M"],
            ["N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
            ["Other"]
        ]
        rk = make_reply_keyboard(ANIME_KEYBOARD_LETTERS)
        bot.send_message(message.chat.id, "🔍 Select a letter to browse anime filters:", reply_markup=rk)

    # /start command
    @bot.message_handler(commands=["start"])
    def start_handler(message):
        try:
            parts = message.text.split()
            if len(parts) > 1 and parts[1] == "anime_keyboard":
                anime_keyboard_handler_private(message)
                return
        except:
            pass

        name = message.from_user.first_name if message.from_user else "User"
        user_id = message.from_user.id if message.from_user else message.chat.id
        chat_id = message.chat.id

        update_user_data(user_id, chat_id, bot.token)

        # LOG NEW USER/GROUP
        if message.chat.type == "private":
            log_message("NEW_USER", f"User started the bot", 
                        user_id, chat_id,
                        message.from_user.username if message.from_user else None,
                        name, None)
        else:
            log_message("NEW_GROUP", f"Bot added to group", 
                        user_id, chat_id,
                        message.from_user.username if message.from_user else None,
                        name,
                        message.chat.title if message.chat.title else None)

        caption = f"""👋 𝐇𝐞𝐲, {name}!
🆔 𝐘𝐨𝐮𝐫 𝐈𝐃: <code>{user_id}</code>

<blockquote>» ᴛʜᴀɴᴋ ʏᴏᴜ! ꜰᴏʀ ᴜꜱɪɴɢ ᴍᴇ. ɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ᴀɴɪᴍᴇꜱ ꜰɪʟᴇꜱ. ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ꜰɪʟᴇꜱ ᴠɪᴀ ᴛʜɪꜱ ᴄʜᴀɴɴᴇʟ.

○ 𝐇ɪɴᴅɪ 𝐃ᴜ𝐛 𝐀ɴɪᴍᴇ : <a href="{UPDATE_CHANNEL}">𝐀ɴɪᴍᴇ 𝐅ʀᴇɴᴢʏ</a>
○ 𝐅ʀᴇɴᴢʏ 𝐌ᴀɴɢᴀ : <a href="https://t.me/Frenzy_Manga">𝐌ᴀɴɢᴀ</a>
○ 𝐀ɴɪᴍᴇ ᴍᴏᴠɪᴇs 𝐀ɴ𝐝 𝐒ᴇʀɪᴇꜱ : <a href="https://t.me/Anime_Movies_in_Hindi_Dub_Sub">𝐌ᴏᴠɪᴇs & 𝐒ᴇʀɪᴇs</a>
○ 𝐇ᴀɴɪᴍᴇ 𝐂ʜᴀɴɴᴇ𝐋 : <a href="https://t.me/Hentaii_verse">𝐇ᴇɴᴛᴀɪ 𝐕ᴇʀsᴇ</a>
○ 𝐀ɴɪᴍᴇ 𝐍ᴇᴡs : <a href="https://t.me/Hindi_Dubbed_Anime_News_India">𝐍ᴇᴡ𝐬</a>

💡 ᴛɪᴘ: ᴛᴀᴘ 'ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅꜱ' ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴀʟʟ ꜰᴇᴀᴛᴜʀᴇꜱ 🛠️</blockquote>"""

        buttons = [
            [types.InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [types.InlineKeyboardButton("ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help")],
            [
                types.InlineKeyboardButton("Group", url=SUPPORT_GROUP),
                types.InlineKeyboardButton("Movies", url=MOVIES_CHANNEL)
            ],
            [types.InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=UPDATE_CHANNEL)]
        ]

        try:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=START_IMAGE,
                caption=caption,
                reply_markup=make_inline_keyboard(buttons),
                message_effect_id="5104841245755180586",
                parse_mode="HTML"
            )
        except Exception as e:
            bot.send_message(message.chat.id, caption, parse_mode="HTML", reply_markup=make_inline_keyboard(buttons))

    # /cmd command
    @bot.message_handler(commands=["cmd"])
    def cmd_handler(message):
        name = message.from_user.first_name if message.from_user else "User"
        user_id = message.from_user.id if message.from_user else message.chat.id

        # LOG COMMAND USAGE
        log_message("COMMAND_USED", f"/cmd - Command list accessed", 
                    user_id, message.chat.id,
                    message.from_user.username if message.from_user else None,
                    name,
                    message.chat.title if message.chat.title else None)

        caption = f"""👋 𝐇𝐞𝐲, {name}!
🆔 𝐘𝐨𝐮𝐫 𝐈𝐃: <code>{user_id}</code>

<blockquote>»ᴄᴍᴅ ᴄᴏᴍᴍᴀɴᴅ
ᴄᴏᴍᴘʟᴇᴛᴇ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ ɢᴜɪᴅᴇ

<b>ᴡʜᴀᴛ ɪᴛ ᴄᴏɴᴛᴀɪɴꜱ:</b>
• ᴀʟʟ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ ᴄᴀᴛᴇɢᴏʀɪᴢᴇᴅ
• ᴅᴇᴛᴀɪʟᴇᴅ ᴜꜱᴀɴɢᴇ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ
• ʙᴜᴛᴛᴏɴ-ʙᴀꜱᴇᴅ ɴᴀᴠɪɢᴀᴛɪᴏɴ
• ꜱᴜʙ-ᴄᴀᴛᴇɢᴏʀɪᴇꜱ ꜰᴏʀ ᴇᴀꜱʏ ᴀᴄᴄᴇꜱꜱ

<b>ᴡʜʏ ɪᴛ ᴡᴀꜱ ᴄʀᴇᴀᴛᴇᴅ:</b>
ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴄᴏᴍᴘʟᴇᴛᴇ ᴀɴᴅ ᴀᴅᴍɪɴ-ꜰʀɪᴇɴᴅʟʏ ɢᴜɪᴅᴇ ꜰᴏʀ ᴀʟʟ ʙᴏᴛ ꜰᴇᴀᴛᴜʀᴇꜱ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅꜱ</blockquote>"""

        buttons = [
            [
                types.InlineKeyboardButton("ꜰɪʟᴛᴇʀ", callback_data="ffilter_help"),
                types.InlineKeyboardButton("ᴅᴍꜰɪʟᴛᴇʀ", callback_data="dmffilter_help"),
                types.InlineKeyboardButton("fstatus", callback_data="fstatus_help"),
            ],
            [
                types.InlineKeyboardButton("ꜱᴛᴀᴛꜱ", callback_data="sstats_help"),
                types.InlineKeyboardButton("ʙʀᴏᴀᴅᴄᴀꜱᴛ!!", callback_data="bbroadcast_help"),
                types.InlineKeyboardButton("ᴘɪɴɢ", callback_data="pping_help"),
            ],
            [
                types.InlineKeyboardButton("fstats", callback_data="fstats_help")
            ],
        ]

        try:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=CMD_IMAGE,
                caption=caption,
                reply_markup=make_inline_keyboard(buttons),
                parse_mode="HTML"
            )
        except Exception as e:
            bot.send_message(message.chat.id, caption, parse_mode="HTML", reply_markup=make_inline_keyboard(buttons))

    # /ping command
    @bot.message_handler(commands=["ping"])
    def ping_command(message):
        # LOG COMMAND USAGE
        log_message("COMMAND_USED", f"/ping - Bot status checked", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username if message.from_user else None,
                    message.from_user.first_name if message.from_user else None,
                    message.chat.title if message.chat.title else None)
        
        try:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=PING_IMAGE,
                caption="""🌸 <b>Pong!</b> 🌸

✅ Bot is alive and working!
⚡ Response: Instant
💖 Thank you for checking!""",
                parse_mode="HTML",
                reply_to_message_id=message.message_id
            )
        except Exception:
            bot.reply_to(message, "Pong! Bot is alive.")

    # /stats command
    @bot.message_handler(commands=["stats"])
    def stats_handler(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "🔒 This command is for admins only to view stats!")
            return
        
        # LOG ADMIN COMMAND
        log_message("ADMIN_COMMAND", f"/stats - Bot statistics checked", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username, message.from_user.first_name,
                    message.chat.title if message.chat.title else None)
        
        user_count = get_user_count(bot.token)
        group_count = get_group_count(bot.token)
        
        stats_msg = f"""<blockquote>📊 <b>Bot Statistics</b>

👤 <b>Users:</b> <code>{user_count}</code>
👥 <b>Groups:</b> <code>{group_count}</code>
🧠 <b>Total Filters:</b> <code>{filters_collection.count_documents({})}</code>
🔧 <b>DM Only Filters:</b> <code>{dm_filters_collection.count_documents({})}</code>

👮 <b>Admins:</b>
"""
        for admin_id in [ADMIN_ID] + OTHER_ADMINS:
            stats_msg += f"- <code>{admin_id}</code>\n"
        stats_msg += "\n🟢 <b>Bot Status:</b> Active</blockquote>"
        bot.reply_to(message, stats_msg)

    # /broadcast command
    @bot.message_handler(commands=["broadcast"])
    def broadcast_handler(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "🔒 This command is for admins only to broadcast!")
            return
        if not message.reply_to_message:
            bot.reply_to(message, "❌ Please reply to a message with /broadcast")
            return

        from db import users_collection, groups_collection
        
        def send_copy_to_chat(target_chat_id: int, src_msg):
            try:
                if src_msg.content_type == "text":
                    bot.send_message(target_chat_id, src_msg.text)
                elif src_msg.content_type == "photo":
                    file_id = src_msg.photo[-1].file_id
                    caption = src_msg.caption or ""
                    bot.send_photo(target_chat_id, file_id, caption=caption)
                else:
                    bot.forward_message(target_chat_id, src_msg.chat.id, src_msg.message_id)
                return True
            except Exception as e:
                print(f"send_copy_to_chat failed: {e}")
                return False

        total_users = get_user_count(bot.token)
        total_groups = get_group_count(bot.token)
        total = total_users + total_groups

        progress_msg = bot.reply_to(message, f"📡 <b>Broadcast Started</b>\n\n👤 Users: <code>{total_users}</code>\n👥 Groups: <code>{total_groups}</code>\n\n⏳ Sending to {total} chats...")
        success = 0
        failed_users = 0
        failed_groups = 0

        for user in users_collection.find({"bot_token": bot.token}):
            try:
                ok = send_copy_to_chat(int(user["user_id"]), message.reply_to_message)
                if ok:
                    success += 1
                else:
                    failed_users += 1
            except Exception:
                failed_users += 1
            time.sleep(0.1)

        for group in groups_collection.find({"bot_token": bot.token}):
            try:
                ok = send_copy_to_chat(int(group["chat_id"]), message.reply_to_message)
                if ok:
                    success += 1
                else:
                    failed_groups += 1
            except Exception:
                failed_groups += 1
            time.sleep(0.1)

        result_msg = (
            f"✅ <b>Broadcast Completed!</b>\n\n"
            f"📊 Total: <code>{total}</code>\n"
            f"✔️ Success: <code>{success}</code>\n"
            f"❌ Failed: <code>{failed_users + failed_groups}</code>\n\n"
            f"Failed users: <code>{failed_users}</code>\n"
            f"Failed groups: <code>{failed_groups}</code>"
        )
        
        # LOG BROADCAST
        log_message("ADMIN_COMMAND", f"/broadcast - Sent to {total} chats", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username, message.from_user.first_name,
                    message.chat.title if message.chat.title else None,
                    f"Success: {success}, Failed: {failed_users + failed_groups}")
        
        try:
            bot.edit_message_text(result_msg, progress_msg.chat.id, progress_msg.message_id)
        except Exception:
            bot.reply_to(message, result_msg)

    # /abroadcast command (admin only broadcast)
    @bot.message_handler(commands=["abroadcast"])
    def admin_broadcast_handler(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "🔒 This command is for admins only!")
            return
        if not message.reply_to_message:
            bot.reply_to(message, "❌ Please reply to a message with /abroadcast")
            return

        def send_copy_to_chat(target_chat_id: int, src_msg):
            try:
                if src_msg.content_type == "text":
                    bot.send_message(target_chat_id, src_msg.text)
                elif src_msg.content_type == "photo":
                    file_id = src_msg.photo[-1].file_id
                    caption = src_msg.caption or ""
                    bot.send_photo(target_chat_id, file_id, caption=caption)
                else:
                    bot.forward_message(target_chat_id, src_msg.chat.id, src_msg.message_id)
                return True
            except Exception as e:
                print(f"send_copy_to_chat failed: {e}")
                return False

        # Get all admins list
        all_admins = [ADMIN_ID] + OTHER_ADMINS
        total_admins = len(all_admins)

        progress_msg = bot.reply_to(message, f"📡 <b>Admin Broadcast Started</b>\n\n👮 Admins: <code>{total_admins}</code>\n\n⏳ Sending to {total_admins} admins...")
        success = 0
        failed = 0

        # Broadcast only to admins (DM only)
        for admin_id in all_admins:
            try:
                ok = send_copy_to_chat(int(admin_id), message.reply_to_message)
                if ok:
                    success += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
            time.sleep(0.1)

        result_msg = (
            f"✅ <b>Admin Broadcast Completed!</b>\n\n"
            f"📊 Total Admins: <code>{total_admins}</code>\n"
            f"✔️ Success: <code>{success}</code>\n"
            f"❌ Failed: <code>{failed}</code>"
        )
        
        # LOG ADMIN BROADCAST
        log_message("ADMIN_COMMAND", f"/abroadcast - Sent to {total_admins} admins", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username, message.from_user.first_name,
                    message.chat.title if message.chat.title else None,
                    f"Success: {success}, Failed: {failed}")
        
        try:
            bot.edit_message_text(result_msg, progress_msg.chat.id, progress_msg.message_id)
        except Exception:
            bot.reply_to(message, result_msg)

    # Callback query handler
    @bot.callback_query_handler(func=lambda call: True)
    def callback_dispatcher(call):
        data = call.data or ""

        # HELP callback
        if data == "help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote>➪ ɪ ᴀᴍ ᴛʜᴇ ꜰᴀꜱᴛᴇꜱᴛ ᴀɴɪꜰɪʟᴛᴇʀ ʙᴏᴛ ᴛᴏ ꜰɪɴᴅ ʜɪɴᴅɪ ᴅᴜʙʙᴇᴅ ᴀɴɪᴍᴇꜱ, ᴍᴏᴠɪᴇꜱ & ꜱᴇʀɪᴇꜱ.
➪ ᴊᴜꜱᴛ ᴛʏᴘᴇ ᴛʜᴇ ɴᴀᴍᴇ — ʏᴏᴜ'ʟʟ ɢᴇᴛ ɪɴꜱᴛᴀɴᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋꜱ.
🔍 ᴍᴀᴋᴇ ꜱᴜʀᴇ ɴᴀᴍᴇ ɪꜱ ᴄᴏʀʀᴇᴄᴛ & ʜɪɴᴅɪ ᴅᴜʙʙᴇᴅ ᴇxɪꜱᴛꜱ.
➪ ꜰᴏʀ ᴍᴏʀᴇ ʜᴇʟᴘ, ᴊᴏɪɴ ᴛʜᴇ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ʙᴇʟᴏᴡ.

◈ ◈ ᴛɪᴘ: ɪꜰ ʏᴏᴜ ᴛʏᴘᴇ #ᴀɴɪᴍᴇ ɪɴ ᴅᴍ ᴏʀ ɢʀᴏᴜᴘ, ʏᴏᴜ'ʟʟ ɢᴇᴛ ᴀ ᴋᴇʏʙᴏᴀʀᴅ.
ᴊᴜꜱᴛ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ꜰɪʀꜱᴛ ᴡᴏʀᴅ ᴏꜰ ʏᴏᴜʀ ᴅᴇꜱɪʀᴇᴅ ᴀɴɪᴍᴇ.
ɪꜰ ɴᴏᴛ ꜰᴏᴜɴᴅ, ᴛᴀᴘ ᴏɴ (ᴏᴛʜᴇʀ).</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(
                types.InlineKeyboardButton("💞Support Group ", url=SUPPORT_GROUP),
                types.InlineKeyboardButton("👨‍💻 Developer ", url="https://t.me/Notxkrishna")
            )
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_start"))
            
            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(HELP_IMAGE),
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id
                    )
                    bot.edit_message_caption(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        caption=help_text,
                        reply_markup=kb,
                        parse_mode="HTML"
                    )
                else:
                    bot.edit_message_text(
                        help_text,
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=kb,
                        message_effect_id="5104841245755180586",
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open help.", show_alert=False)
            return

        # BACK TO START callback
        if data == "back_to_start":
            name = call.from_user.first_name if call.from_user else "User"
            user_id = call.from_user.id if call.from_user else call.message.chat.id

            caption = f"""👋 𝐇𝐞𝐲, {name}!
🆔 𝐘𝐨𝐮𝐫 𝐈𝐃: <code>{user_id}</code>

<blockquote>» ᴛʜᴀɴᴋ ʏᴏᴜ! ꜰᴏʀ ᴜꜱɪɴɢ ᴍᴇ. ɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ᴀɴɪᴍᴇꜱ ꜰɪʟᴇꜱ. ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ꜰɪʟᴇꜱ ᴠɪᴀ ᴛʜɪꜱ ᴄʜᴀɴɴᴇʟ.

○ 𝐇ɪɴᴅɪ 𝐃ᴜ𝐛 𝐀ɴɪᴍᴇ : <a href="{UPDATE_CHANNEL}">𝐀ɴɪᴍᴇ 𝐅ʀᴇɴᴢʏ</a>
○ 𝐅ʀᴇɴᴢʏ 𝐌ᴀɴɢᴀ : <a href="https://t.me/Frenzy_Manga">𝐌ᴀɴɢᴀ</a>
○ 𝐀ɴɪᴍᴇ ᴍᴏᴠɪᴇs 𝐀ɴ𝐝 𝐒ᴇʀɪᴇꜱ : <a href="https://t.me/Anime_Movies_in_Hindi_Dub_Sub">𝐌ᴏᴠɪᴇs & 𝐒ᴇʀɪᴇs</a>
○ 𝐇ᴀɴɪᴍᴇ 𝐂ʜᴀɴɴᴇ𝐋 : <a href="https://t.me/Hentaii_verse">𝐇ᴇɴᴛᴀɪ 𝐕ᴇʀsᴇ</a>
○ 𝐀ɴɪᴍᴇ 𝐍ᴇᴡs : <a href="https://t.me/Hindi_Dubbed_Anime_News_India">𝐍ᴇᴡ𝐬</a>

💡 ᴛɪᴘ: ᴛᴀᴘ 'ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅꜱ' ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴀʟʟ ꜰᴇᴀᴛᴜʀᴇꜱ 🛠️</blockquote>"""

            buttons = [
                [types.InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
                [types.InlineKeyboardButton("ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help")],
                [
                    types.InlineKeyboardButton("Group", url=SUPPORT_GROUP),
                    types.InlineKeyboardButton("Movies", url=MOVIES_CHANNEL)
                ],
                [types.InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=UPDATE_CHANNEL)]
            ]
            
            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(START_IMAGE),
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=make_inline_keyboard(buttons)
                    )
                    bot.edit_message_caption(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        caption=caption,
                        reply_markup=make_inline_keyboard(buttons),
                        parse_mode="HTML"
                    )
                else:
                    bot.edit_message_text(
                        caption,
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=make_inline_keyboard(buttons),
                        message_effect_id="5104841245755180586",
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"back_to_start edit failed: {e}")
                try:
                    bot.edit_message_text(
                        caption,
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=make_inline_keyboard(buttons),                
                        parse_mode="HTML"
                    )
                    bot.answer_callback_query(call.id)
                except Exception as e2:
                    print(f"back_to_start: fallback edit_text failed: {e2}")
                    bot.answer_callback_query(call.id, "Unable to go back to start.", show_alert=False)
            return

        # Add more callback handlers here for ffilter_help, dmffilter_help, etc.

        bot.answer_callback_query(call.id, "")

    # #Anime handler
    @bot.message_handler(func=lambda m: bool(re.fullmatch(r"#Anime", m.text or "", flags=re.IGNORECASE)))
    def anime_keyboard_handler(message):
        if message.chat.type == "private":
            ANIME_KEYBOARD_LETTERS = [
                ["0","1","2","3","4","5","6","7","8","9"],
                ["A","B","C","D","E","F","G","H","I","J","K","L","M"],
                ["N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
                ["Other"]
            ]
            rk = make_reply_keyboard(ANIME_KEYBOARD_LETTERS)
            bot.reply_to(message, "🔍 Select a letter to browse anime filters:", reply_markup=rk)
        else:
            ik = types.InlineKeyboardMarkup()
            ik.add(types.InlineKeyboardButton("Click Here", url=f"https://t.me/{BOT_USERNAME}?start=anime_keyboard"))
            bot.reply_to(message, "Please click the button below to browse anime filters in DM:", reply_markup=ik)
