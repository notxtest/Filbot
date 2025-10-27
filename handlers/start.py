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

    # Callback query handler - COMPLETE WITH ALL CALLBACKS
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

        # BACK TO CMD callback
        if data == "back_to_cmd":
            name = call.from_user.first_name if call.from_user else "User"
            user_id = call.from_user.id if call.from_user else call.message.chat.id

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
                # Try to edit message if it's a photo message
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(CMD_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"back_to_cmd edit failed: {e}")
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
                    print(f"back_to_cmd: fallback edit_text failed: {e2}")
                    bot.answer_callback_query(call.id, "Unable to go back to cmd.", show_alert=False)
            return

        # FILTER HELP callback
        elif data == "ffilter_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote>➪ꜰɪʟᴛᴇʀ
ᴀᴅᴅ ꜰɪʟᴛᴇʀ:
<code>/filter</code> ᴋᴇʏᴡᴏʀᴅ - ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ
ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ꜰɪʟᴛᴇʀꜱ ɪɴ ɢʀᴏᴜᴘ ᴀɴᴅ ᴅᴍ ʙᴏᴛʜ

ꜱᴛᴏᴘ ꜰɪʟᴛᴇʀ:
<code>/stop</code> ᴋᴇʏᴡᴏʀᴅ - ᴅᴇʟᴇᴛᴇ ᴀ ꜰɪʟᴛᴇʀ
ʏᴏᴜ ᴄᴀɴ ꜱᴛᴏᴘ ꜰɪʟᴛᴇʀꜱ ɪɴ ɢʀᴏᴜᴘ ᴀɴᴅ ᴅᴍ ʙᴏᴛʜ

ᴀʟʟ ꜰɪʟᴛᴇʀꜱ:
<code>/filters</code> - ꜱʜᴏᴡ ᴀʟʟ ꜱᴀᴠᴇᴅ ꜰɪʟᴛᴇʀꜱ</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_cmd"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"ffilter_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open ffilter_help.", show_alert=False)
            return

        # DM FILTER HELP callback
        elif data == "dmffilter_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote><b>➪ᴅᴍ ꜰɪʟᴛᴇʀ</b>
ᴅᴍ ᴏɴʟʏ ꜰɪʟᴛᴇʀ ᴀᴅᴅ:
<code>/filter</code> ᴋᴇʏᴡᴏʀᴅ - ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ
ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ɪɴ ɢʀᴏᴜᴘ ᴀɴᴅ ᴅᴍ ʙᴏᴛʜ

ꜱᴛᴏᴘ ᴅᴍ ꜰɪʟᴛᴇʀ:
<code>/bstop</code> ᴋᴇʏᴡᴏʀᴅ - ᴅᴇʟᴇᴛᴇ ᴀ ᴅᴍ ꜰɪʟᴛᴇʀ
ʏᴏᴜ ᴄᴀɴ ꜱᴛᴏᴘ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ɪɴ ɢʀᴏᴜᴘ ᴀɴᴅ ᴅᴍ ʙᴏᴛʜ

ᴀʟʟ ᴅᴍ ꜰɪʟᴛᴇʀꜱ:
<code>/bfilters</code> - ꜱʜᴏᴡ ᴀʟʟ ᴅᴍ ᴏɴʟʏ ꜰɪʟᴛᴇʀꜱ

ɴᴏᴛᴇ:
ᴛᴏ ᴜꜱᴇ ᴅᴍ ꜰɪʟᴛᴇʀꜱ, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ɢᴏ ʙᴀᴄᴋ ᴀɴᴅ ᴄʜᴇᴄᴋ ꜰꜱᴛᴀᴛᴜꜱ ꜰᴏʀ ꜰᴜʟʟ ꜰᴇᴀᴛᴜʀᴇꜱ ᴛᴏ ꜱᴇᴇ ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ᴛʜᴇᴍ ᴀɴᴅ ʜᴏᴡ ᴛᴏ ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪꜱᴀʙʟᴇ ᴛʜᴇᴍ
</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_cmd"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"dmffilter_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open dmffilter_help.", show_alert=False)
            return

        # FSTATUS HELP callback
        elif data == "fstatus_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote><b>➪ꜰꜱᴛᴀᴛᴜꜱ</b>
<code>/fstatus</code>- ꜱʜᴏᴡꜱ ᴄᴏᴍᴘʟᴇᴛᴇ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ʀᴇᴘᴏʀᴇ:
• ɢʟᴏʙᴀʟ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ꜱᴛᴀᴛᴜꜱ (ᴇɴᴀʙʟᴇᴅ/ᴅɪꜱᴀʙʟᴇᴅ)
• ᴄʀᴇᴀᴛɪᴏɴ ᴍᴏᴅᴇ ꜱᴛᴀᴛᴜꜱ (ᴅᴍ ᴏɴʟʏ/ɴᴏʀᴍᴀʟ)
• ɢʟᴏʙᴀʟ ɢʀᴏᴜᴘꜱ ꜱᴛᴀᴛᴜꜱ (ᴇɴᴀʙʟᴇᴅ/ᴅɪꜱᴀʙʟᴇᴅ)
• ᴇɴᴀʙʟᴇᴅ ɢʟᴏᴜᴘꜱ ᴄᴏᴜɴᴛ
• ᴅɪꜱᴀʙʟᴇᴅ ɢʀᴏᴜᴘꜱ ᴄᴏᴜɴᴛ
• ᴅᴍ ᴏɴʟʏ ꜰɪʟᴛᴇʀꜱ ᴄᴏᴜɴᴛ</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_cmd"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"fstatus_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open fstatus_help.", show_alert=False)
            return

        # STATS HELP callback
        elif data == "sstats_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote>➪<b>ꜱᴛᴀᴛꜱ</b>
<code>/stats</code> - ꜱʜᴏᴡꜱ ᴄᴏᴍᴘʟᴇᴛᴇ ʙᴏᴛ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ:
• ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ ᴄᴏᴜɴᴛ
• ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘꜱ ᴄᴏᴜɴᴛ
• ᴛᴏᴛᴀʟ ɴᴏʀᴍᴀʟ ꜰɪʟᴛᴇʀꜱ ᴄᴏᴜɴᴛ
• ᴛᴏᴛᴀʟ ᴅᴍ ᴏɴʟʏ ꜰɪʟᴛᴇʀꜱ ᴄᴏᴜɴᴛ
• ᴀᴅᴍɪɴꜱ ʟɪꜱᴛ
• ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_cmd"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"sstats_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open sstats_help.", show_alert=False)
            return

        # BROADCAST HELP callback
        elif data == "bbroadcast_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote expendable>➪<b>ʙʀᴏᴀᴅᴄᴀꜱᴛ</b>
<code>/broadcast</code>- ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ꜱᴇɴᴅ ɪᴛ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ ᴀɴᴅ ɢʀᴏᴜᴘꜱ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
1. ꜱᴇɴᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ (ᴛᴇxᴛ/ᴘʜᴏᴛᴏ/ᴀɴʏ ᴛʏᴘᴇ)
2. ʀᴇᴘʟʏ ᴛᴏ ɪᴛ ᴡɪᴛʜ /ʙʀᴏᴀᴅᴄᴀꜱᴛ
3. ʙᴏᴛ ᴡɪʟʟ ꜱᴇɴᴅ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ ᴀɴᴅ ɢʀᴏᴜᴘꜱ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ
4. ꜱʜᴏᴡꜱ ᴘʀᴏɢʀᴇꜱꜱ ᴡɪᴛʜ ꜱᴜᴄᴄᴇꜱꜱ/ꜰᴀɪʟᴇᴅ ᴄᴏᴜɴᴛꜱ

➪<b>ᴀʙʀᴏᴀᴅᴄᴀꜱᴛ</b>
<code>/abroadcast</code>- ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ꜱᴇɴᴅ ɪᴛ ᴏɴʟʏ ᴛᴏ ᴀᴅᴍɪɴꜱ ɪɴ ᴅᴍ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
1. ꜱᴇɴᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ (ᴛᴇxᴛ/ᴘʜᴏᴛᴏ/ᴀɴʏ ᴛʏᴘᴇ)
2. ʀᴇᴘʟʏ ᴛᴏ ɪᴛ ᴡɪᴛʜ /ᴀʙʀᴏᴀᴅᴄᴀꜱᴛ
3. ʙᴏᴛ ᴡɪʟʟ ꜱᴇɴᴅ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴏɴʟʏ ᴛᴏ ᴀʟʟ ᴀᴅᴍɪɴꜱ ɪɴ ᴅᴍ
4. ɢʀᴏᴜᴘꜱ ᴀʀᴇ ᴄᴏᴍᴘʟᴇᴛᴇʟʏ ᴇxᴄʟᴜᴅᴇᴅ
5. ꜱʜᴏᴡꜱ ᴘʀᴏɢʀᴇꜱꜱ ᴡɪᴛʜ ꜱᴜᴄᴄᴇꜱꜱ/ꜰᴀɪʟᴇᴅ ᴄᴏᴜɴᴛꜱ</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_cmd"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"bbroadcast_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open bbroadcast_help.", show_alert=False)
            return

        # PING HELP callback
        elif data == "pping_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote>➪<b>ᴘɪɴɢ</b>
<code>/ping</code> - ᴄʜᴇᴄᴋꜱ ʙᴏᴛ'ꜱ ʀᴇꜱᴘᴏɴꜱᴇ ᴛɪᴍᴇ ᴀɴᴅ ꜱᴛᴀᴛᴜꜱ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
• ꜱᴇɴᴅꜱ ᴀ ʀᴇꜱᴘᴏɴꜱᴇ ᴡɪᴛʜ "ᴘᴏɴɢ!"
• ꜱʜᴏᴡꜱ ʙᴏᴛ ɪꜱ ᴀʟɪᴠᴇ ᴀɴᴅ ᴡᴏʀᴋɪɴɢ
• ᴍᴇᴀꜱᴜʀᴇꜱ ʀᴇꜱᴘᴏɴꜱᴇ ᴛɪᴍᴇ
• ᴄᴏɴꜰɪʀᴍꜱ ʙᴏᴛ ᴄᴏɴɴᴇᴄᴛɪᴠɪᴛʏ

ᴏᴜᴛᴘᴜᴛ:
"ᴘᴏɴɢ! ʙᴏᴛ ɪꜱ ᴀʟɪᴠᴇ ᴀɴᴅ ᴡᴏʀᴋɪɴɢ"</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_cmd"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"pping_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open pping_help.", show_alert=False)
            return

        # FSTATS HELP callback
        elif data == "fstats_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote>➪<b>ꜱᴛᴀᴛꜱ</b>
<code>/fstats</code> - ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɢɪᴠᴇꜱ ʏᴏᴜ ᴀʟʟ ᴅᴍ ᴏɴʟʏ ꜰɪʟᴛᴇʀꜱ ꜰᴇᴀᴛᴜʀᴇꜱ ᴀɴᴅ ꜱᴇᴛᴛɪɴɢꜱ. ʙᴇʟᴏᴡ ʏᴏᴜ ᴄᴀɴ ꜱᴇᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴛʜᴇɪʀ ᴜꜱᴇꜱ.</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(
                types.InlineKeyboardButton("enable", callback_data="enable_help"),
                types.InlineKeyboardButton("disable", callback_data="disable_help"),
                types.InlineKeyboardButton("open", callback_data="open_help")
            )
            kb.row(
                types.InlineKeyboardButton("close", callback_data="close_help"),
                types.InlineKeyboardButton("openglobal", callback_data="openglobal_help"),
                types.InlineKeyboardButton("closeglobal", callback_data="closeglobal_help")
            )
            kb.row(
                types.InlineKeyboardButton("opengroup", callback_data="opengroup_help"),
                types.InlineKeyboardButton("closegroup", callback_data="closegroup_help"),
                types.InlineKeyboardButton("closeid", callback_data="closeid_help")
            )
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_cmd"))
            
            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"fstats_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open fstats_help.", show_alert=False)
            return

        # ENABLE HELP callback
        elif data == "enable_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote><b>➪ᴇɴᴀʙʟᴇꜰɪʟᴛᴇʀ</b>
<code>/enablefilter</code>- ᴛᴜʀɴꜱ ᴏɴ ᴅᴍ ᴏɴʟʏ ᴄʀᴇᴀᴛɪᴏɴ ᴍᴏᴅᴇ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
• ᴡʜᴇɴ ᴇɴᴀʙʟᴇᴅ, ᴀʟʟ ɴᴇᴡ ꜰɪʟᴛᴇʀꜱ ᴡɪʟʟ ʙᴇ ꜱᴀᴠᴇᴅ ᴀꜱ ᴅᴍ ᴏɴʟʏ ꜰɪʟᴛᴇʀꜱ
• ɴᴏʀᴍᴀʟ ꜰɪʟᴛᴇʀꜱ ᴡɪʟʟ ɴᴏᴛ ʙᴇ ᴄʀᴇᴀᴛᴇᴅ
• ᴏɴʟʏ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ᴡɪʟʟ ʀᴇꜱᴘᴏɴᴅ ᴛᴏ ᴋᴇʏᴡᴏʀᴅꜱ
• ᴜꜱᴇ /ᴅɪꜱᴀʙʟᴇꜰɪʟᴛᴇʀ ᴛᴏ ᴛᴜʀɴ ᴏꜰꜰ

ᴇꜰꜰᴇᴄᴛ: ᴄᴏɴᴛʀᴏʟꜱ ᴡʜᴇʀᴇ ɴᴇᴡ ꜰɪʟᴛᴇʀꜱ ᴀʀᴇ ꜱᴀᴠᴇᴅ"</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_fstats_help"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"enable_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open enable_help.", show_alert=False)
            return

        # DISABLE HELP callback
        elif data == "disable_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote><b>➪ᴅɪꜱᴀʙʟᴇ ꜰɪʟᴛᴇʀ</b>
<code>/disablefilter</code>- ᴛᴜʀɴꜱ ᴏꜰꜰ ᴅᴍ ᴏɴʟʏ ᴄʀᴇᴀᴛɪᴏɴ ᴍᴏᴅᴇ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
• ꜱᴡɪᴛᴄʜᴇꜱ ᴄʀᴇᴀᴛɪᴏɴ ᴍᴏᴅᴇ ᴛᴏ ɴᴏʀᴍᴀʟ
• ɴᴇᴡ ꜰɪʟᴛᴇʀꜱ ᴡɪʟʟ ʙᴇ ꜱᴀᴠᴇᴅ ᴀꜱ ɴᴏʀᴍᴀʟ ꜰɪʟᴛᴇʀꜱ
• ᴅᴍ ᴏɴʟʏ ꜰɪʟᴛᴇʀ ᴄʀᴇᴀᴛɪᴏɴ ɪꜱ ᴅɪꜱᴀʙʟᴇᴅ

ᴇꜰꜰᴇᴄᴛ: ᴄᴏɴᴛʀᴏʟꜱ ᴡʜᴇʀᴇ ɴᴇᴡ ꜰɪʟᴛᴇʀꜱ ᴀʀᴇ ꜱᴀᴠᴇᴅ"</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_fstats_help"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"disable_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open disable_help.", show_alert=False)
            return

        # OPEN HELP callback
        elif data == "open_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote><b>ᴏᴘᴇɴ ꜰɪʟᴛᴇʀ</b>
<code>/openfilter</code> - ᴇɴᴀʙʟᴇꜱ ɢʟᴏʙᴀʟ ᴅᴍ ᴏɴʟʏ ꜰɪʟᴛᴇʀꜱ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
• ᴛᴜʀɴꜱ ᴏɴ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ɢʟᴏʙᴀʟʟʏ
• ᴅᴍ ꜰɪʟᴛᴇʀꜱ ᴡɪʟʟ ʀᴇꜱᴘᴏɴᴅ ᴛᴏ ᴋᴇʏᴡᴏʀᴅꜱ
• ᴡᴏʀᴋꜱ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛꜱ ᴀɴᴅ ᴇɴᴀʙʟᴇᴅ ɢʀᴏᴜᴘꜱ

ᴇꜰꜰᴇᴄᴛ: ᴄᴏɴᴛʀᴏʟꜱ ᴇɴᴛɪʀᴇ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ꜱʏꜱᴛᴇᴍ"</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_fstats_help"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"open_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open open_help.", show_alert=False)
            return

        # CLOSE HELP callback
        elif data == "close_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote><b>ᴄʟᴏꜱᴇ ꜰɪʟᴛᴇʀ</b>
<code>/closefilter</code>- ᴅɪꜱᴀʙʟᴇꜱ ɢʟᴏʙᴀʟ ᴅᴍ ᴏɴʟʏ ꜰɪʟᴛᴇʀꜱ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
• ᴛᴜʀɴꜱ ᴏꜰꜰ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ɢʟᴏʙᴀʟʟʏ
• ᴅᴍ ꜰɪʟᴛᴇʀꜱ ᴡɪʟʟ ɴᴏᴛ ʀᴇꜱᴘᴏɴᴅ ᴛᴏ ᴋᴇʙᴡᴏʀᴅꜱ
• ᴄᴏᴍᴘʟᴇᴛᴇ ꜱʏꜱᴛᴇᴍ ɪꜱ ᴅɪꜱᴀʙʟᴇᴅ

ᴇꜰꜰᴇᴄᴛ: ᴄᴏᴍᴘʟᴇᴛᴇʟʏ ᴅɪꜱᴀʙʟᴇꜱ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ꜱʏꜱᴛᴇᴍ"</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_fstats_help"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"close_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open close_help.", show_alert=False)
            return

        # OPEN GLOBAL HELP callback
        elif data == "openglobal_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote><b>ᴏᴘᴇɴ ɢʟᴏʙᴀʟ ɢʀᴏᴜᴘ</b>
<code>/openglobalgroup</code>- ᴇɴᴀʙʟᴇꜱ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ɪɴ ᴀʟʟ ɢʀᴏᴜᴘꜱ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
• ᴅᴍ ꜰɪʟᴛᴇʀꜱ ᴡɪʟʟ ᴡᴏʀᴋ ɪɴ ᴇᴠᴇʀʏ ɢʀᴏᴜᴘ
• ᴄᴀɴ ᴅɪꜱᴀʙʟᴇ ꜱᴘᴇᴄɪꜰɪᴄ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ /ᴄʟᴏꜱᴇɢʀᴏᴜᴘ
• ɢʟᴏʙᴀʟ ɢʀᴏᴜᴘ ᴀᴄᴄᴇꜱꜱ ꜰᴏʀ ᴅᴍ ꜰɪʟᴛᴇʀꜱ

ᴇꜰꜰᴇᴄᴛ: ᴇɴᴀʙʟᴇꜱ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ɪɴ ᴀʟʟ ɢʟᴏᴜᴘꜱ"</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_fstats_help"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"openglobal_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open openglobal_help.", show_alert=False)
            return

        # CLOSE GLOBAL HELP callback
        elif data == "closeglobal_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote><b>ᴄʟᴏꜱᴇ ɢʟᴏʙᴀʟ ɢʀᴏᴜᴘ</b>
<code>/closeglobalgroup</code>- ᴅɪꜱᴀʙʟᴇꜱ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ɪɴ ᴀʟʟ ɢʀᴏᴜᴘꜱ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
• ᴅᴍ ꜰɪʟᴛᴇʀꜱ ᴅɪꜱᴀʙʟᴇᴅ ɪɴ ᴀʟʟ ɢʀᴏᴜᴘꜱ
• ᴄᴀɴ ᴇɴᴀʙʟᴇ ꜱᴘᴇᴄɪꜰɪᴄ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ /ᴏᴘᴇɴɢʀᴏᴜᴘ
• ɢʟᴏʙᴀʟ ɢʀᴏᴜᴘ ᴀᴄᴄᴇꜱꜱ ʀᴇᴍᴏᴠᴇᴅ

ᴇꜰꜱᴇᴄᴛ: ᴅɪꜱᴀʙʟᴇꜱ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ɪɴ ᴀʟʟ ɢʀᴏᴜᴘꜱ"</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_fstats_help"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"closeglobal_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open closeglobal_help.", show_alert=False)
            return

        # OPEN GROUP HELP callback
        elif data == "opengroup_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote><b>ᴏᴘᴇɴ ɢʀᴏᴜᴘ</b>
<code>/opengroup</code> ɢʀᴏᴜᴘ_ɪᴅ - ᴇɴᴀʙʟᴇꜱ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ꜰᴏʀ ꜱᴘᴇᴄɪꜰɪᴄ ɢʀᴏᴜᴘ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
• ᴇɴᴀʙʟᴇꜱ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ꜰᴏʀ ᴛʜᴇ ꜱᴘᴇᴄɪꜰɪᴇᴅ ɢʀᴏᴜᴘ ɪᴅ
• ᴇxᴀᴍᴘʟᴇ: /ᴏᴘᴇɴɢʀᴏᴜᴘ -100123456789
• ᴅᴍ ꜰɪʟᴛᴇʀꜱ ᴡɪʟʟ ᴡᴏʀᴋ ɪɴ ᴛʜᴀᴛ ꜱᴘᴇᴄɪꜰɪᴄ ɢʀᴏᴜᴘ

ᴇꜰꜰᴇᴄᴛ: ᴇɴᴀʙʟᴇꜱ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ꜰᴏʀ ᴀ ꜱᴘᴇᴄɪꜰɪᴄ ɢʀᴏᴜᴘ ᴏɴʟʏ"</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_fstats_help"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"opengroup_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open opengroup_help.", show_alert=False)
            return

        # CLOSE GROUP HELP callback
        elif data == "closegroup_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote><b>ᴄʟᴏꜱᴇ ɢʀᴏᴜᴘ</b>
<code>/closegroup</code> ɢʀᴏᴜᴘ_ɪᴅ - ᴅɪꜱᴀʙʟᴇꜱ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ꜰᴏʀ ꜱᴘᴇᴄɪꜰɪᴄ ɢʀᴏᴜᴘ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
• ᴅɪꜱᴀʙʟᴇꜱ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ꜰᴏʀ ᴛʜᴇ ꜱᴘᴇᴄɪꜰɪᴇᴅ ɢʀᴏᴜᴘ ɪᴅ
• ᴇxᴀᴍᴘʟᴇ: /ᴄʟᴏꜱᴇɢʀᴏᴜᴘ -100123456789
• ᴅᴍ ꜰɪʟᴛᴇʀꜱ ᴡɪʟʟ ɴᴏᴛ ᴡᴏʀᴋ ɪɴ ᴛʜᴀᴛ ꜱᴘᴇᴄɪꜰɪᴄ ɢʀᴏᴜᴘ

ᴇꜰꜰᴇᴄᴛ: ᴅɪꜱᴀʙʟᴇꜱ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ꜰᴏʀ ᴀ ꜱᴘᴇᴄɪꜰɪᴄ ɢʀᴏᴜᴘ ᴏɴʟʏ"</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_fstats_help"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"closegroup_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open closegroup_help.", show_alert=False)
            return

        # CLOSEID HELP callback
        elif data == "closeid_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote><b>ᴄʟᴏꜱᴇɪᴅ</b>
<code>/closeid</code> - ꜱʜᴏᴡꜱ ʟɪꜱᴛ ᴏꜰ ɢʀᴏᴜᴘꜱ ᴡʜᴇʀᴇ ᴅᴍ ꜰɪʟᴛᴇʀꜱ ᴀʀᴇ ᴅɪꜱᴀʙʟᴇᴅ

ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:
• ꜱʜᴏᴡꜱ ɢʀᴏᴜᴘ ɴᴀᴍᴇꜱ ᴀɴᴅ ɪᴅꜱ
• ᴅɪꜱᴘʟᴀʏꜱ ᴀʟʟ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ ᴅɪꜱᴀʙʟᴇᴅ ᴅᴍ ꜰɪʟᴛᴇʀꜱ
• ꜱʜᴏᴡꜱ ᴛᴏᴛᴀʟ ᴄᴏᴜɴᴛ ᴏꜰ ᴅɪꜱᴀʙʟᴇᴅ ɢʀᴏᴜᴘꜱ

ᴇꜰꜰᴇᴄᴛ: ᴘʀᴏᴠɪᴅᴇꜱ ᴄᴏᴍᴘʟᴇᴛᴇ ʟɪꜱᴛ ᴏꜰ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ ᴅɪꜱᴀʙʟᴇᴅ ᴅᴍ ꜰɪʟᴛᴇʀꜱ"</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_fstats_help"))

            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"closeid_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open closeid_help.", show_alert=False)
            return

        # BACK TO FSTATS HELP callback
        elif data == "back_to_fstats_help":
            help_text = """💞 Hᴇʏ...!!,

<blockquote>➪<b>ꜱᴛᴀᴛꜱ</b>
<code>/fstats</code> - ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɢɪᴠᴇꜱ ʏᴏᴜ ᴀʟʟ ᴅᴍ ᴏɴʟʏ ꜰɪʟᴛᴇʀꜱ ꜰᴇᴀᴛᴜʀᴇꜱ ᴀɴᴅ ꜱᴇᴛᴛɪɴɢꜱ. ʙᴇʟᴏᴡ ʏᴏᴜ ᴄᴀɴ ꜱᴇᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴛʜᴇɪʀ ᴜꜱᴇꜱ.</blockquote>"""

            kb = types.InlineKeyboardMarkup()
            kb.row(
                types.InlineKeyboardButton("enable", callback_data="enable_help"),
                types.InlineKeyboardButton("disable", callback_data="disable_help"),
                types.InlineKeyboardButton("open", callback_data="open_help")
            )
            kb.row(
                types.InlineKeyboardButton("close", callback_data="close_help"),
                types.InlineKeyboardButton("openglobal", callback_data="openglobal_help"),
                types.InlineKeyboardButton("closeglobal", callback_data="closeglobal_help")
            )
            kb.row(
                types.InlineKeyboardButton("opengroup", callback_data="opengroup_help"),
                types.InlineKeyboardButton("closegroup", callback_data="closegroup_help"),
                types.InlineKeyboardButton("closeid", callback_data="closeid_help")
            )
            kb.row(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_cmd"))
            
            try:
                if call.message.content_type == 'photo':
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(STATS_IMAGE),
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
                        parse_mode="HTML"
                    )
                bot.answer_callback_query(call.id)
            except Exception as e:
                print(f"fstats_help callback edit failed: {e}")
                bot.answer_callback_query(call.id, "Unable to open fstats_help.", show_alert=False)
            return

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
