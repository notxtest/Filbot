from telebot import types
from config import ADMIN_ID, OTHER_ADMINS, LOGS_CHANNEL
from db import get_dm_settings, update_dm_settings, get_all_dm_filters, get_dm_filter_by_id
from db import delete_dm_filter, short_display
import re

def register_dmfilters_handlers(bot):
    
    # Helper function for inline keyboard
    def make_inline_keyboard(button_rows):
        ik = types.InlineKeyboardMarkup()
        for row in button_rows:
            ik.row(*row)
        return ik

    # Logs function
    def log_message(log_type: str, message: str, user_id: int = None, chat_id: int = None, 
                    username: str = None, first_name: str = None, chat_title: str = None, 
                    extra_data: str = ""):
        try:
            import time
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

    # /openfilter command
    @bot.message_handler(commands=["openfilter"])
    def open_dm_filter(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Only admins can use this command!")
            return
        
        update_dm_settings({"dm_filters_enabled": True})
        
        # LOG ADMIN ACTION
        log_message("ADMIN_COMMAND", f"/openfilter - DM Filters Enabled", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username, message.from_user.first_name,
                    message.chat.title if message.chat.title else None)
        
        bot.reply_to(message, "✅ <b>DM Only Filters Enabled Globally</b>")

    # /closefilter command
    @bot.message_handler(commands=["closefilter"])
    def close_dm_filter(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Only admins can use this command!")
            return
        
        update_dm_settings({"dm_filters_enabled": False})
        
        # LOG ADMIN ACTION
        log_message("ADMIN_COMMAND", f"/closefilter - DM Filters Disabled", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username, message.from_user.first_name,
                    message.chat.title if message.chat.title else None)
        
        bot.reply_to(message, "❌ <b>DM Only Filters Disabled Globally</b>")

    # /enablefilter command
    @bot.message_handler(commands=["enablefilter"])
    def enable_dm_creation(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Only admins can use this command!")
            return
        
        update_dm_settings({"creation_mode": True})
        
        # LOG ADMIN ACTION
        log_message("ADMIN_COMMAND", f"/enablefilter - Creation Mode Enabled", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username, message.from_user.first_name,
                    message.chat.title if message.chat.title else None)
        
        bot.reply_to(message, "🔧 <b>DM Only Creation Mode Enabled</b>")

    # /disablefilter command
    @bot.message_handler(commands=["disablefilter"])
    def disable_dm_creation(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Only admins can use this command!")
            return
        
        update_dm_settings({"creation_mode": False})
        
        # LOG ADMIN ACTION
        log_message("ADMIN_COMMAND", f"/disablefilter - Creation Mode Disabled", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username, message.from_user.first_name,
                    message.chat.title if message.chat.title else None)
        
        bot.reply_to(message, "⚙️ <b>DM Only Creation Mode Disabled</b>")

    # /openglobalgroup command
    @bot.message_handler(commands=["openglobalgroup"])
    def open_global_groups(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Only admins can use this command!")
            return
        
        update_dm_settings({"global_groups_enabled": True})
        
        # LOG ADMIN ACTION
        log_message("ADMIN_COMMAND", f"/openglobalgroup - Global Groups Enabled", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username, message.from_user.first_name,
                    message.chat.title if message.chat.title else None)
        
        bot.reply_to(message, "🌐 <b>DM Filters Enabled in All Groups</b>")

    # /closeglobalgroup command
    @bot.message_handler(commands=["closeglobalgroup"])
    def close_global_groups(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Only admins can use this command!")
            return
        
        update_dm_settings({"global_groups_enabled": False})
        
        # LOG ADMIN ACTION
        log_message("ADMIN_COMMAND", f"/closeglobalgroup - Global Groups Disabled", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username, message.from_user.first_name,
                    message.chat.title if message.chat.title else None)
        
        bot.reply_to(message, "🔒 <b>DM Filters Disabled in All Groups</b>")

    # /opengroup command
    @bot.message_handler(commands=["opengroup"])
    def open_specific_group(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Only admins can use this command!")
            return
        
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Usage: /opengroup <group_id>")
            return
        
        try:
            group_id = int(parts[1])
        except ValueError:
            bot.reply_to(message, "❌ Invalid group ID!")
            return
        
        settings = get_dm_settings()
        enabled_groups = settings.get("enabled_groups", [])
        disabled_groups = settings.get("disabled_groups", [])
        
        # Remove from disabled groups if present
        if group_id in disabled_groups:
            disabled_groups.remove(group_id)
        
        # Add to enabled groups if not present
        if group_id not in enabled_groups:
            enabled_groups.append(group_id)
        
        update_dm_settings({
            "enabled_groups": enabled_groups,
            "disabled_groups": disabled_groups
        })
        
        # LOG ADMIN ACTION
        log_message("ADMIN_COMMAND", f"/opengroup - Enabled DM Filters for Group {group_id}", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username, message.from_user.first_name,
                    message.chat.title if message.chat.title else None)
        
        bot.reply_to(message, f"✅ <b>DM Filters Enabled for Group</b>\n\nGroup ID: <code>{group_id}</code>")

    # /closegroup command
    @bot.message_handler(commands=["closegroup"])
    def close_specific_group(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Only admins can use this command!")
            return
        
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Usage: /closegroup <group_id>")
            return
        
        try:
            group_id = int(parts[1])
        except ValueError:
            bot.reply_to(message, "❌ Invalid group ID!")
            return
        
        settings = get_dm_settings()
        enabled_groups = settings.get("enabled_groups", [])
        disabled_groups = settings.get("disabled_groups", [])
        
        # Remove from enabled groups if present
        if group_id in enabled_groups:
            enabled_groups.remove(group_id)
        
        # Add to disabled groups if not present
        if group_id not in disabled_groups:
            disabled_groups.append(group_id)
        
        update_dm_settings({
            "enabled_groups": enabled_groups,
            "disabled_groups": disabled_groups
        })
        
        # LOG ADMIN ACTION
        log_message("ADMIN_COMMAND", f"/closegroup - Disabled DM Filters for Group {group_id}", 
                    message.from_user.id, message.chat.id,
                    message.from_user.username, message.from_user.first_name,
                    message.chat.title if message.chat.title else None)
        
        bot.reply_to(message, f"❌ <b>DM Filters Disabled for Group</b>\n\nGroup ID: <code>{group_id}</code>")

    # /closeid command
    @bot.message_handler(commands=["closeid"])
    def show_closed_groups(message):
        """Show list of groups where DM filters are disabled"""
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Only admins can use this command!")
            return
        
        settings = get_dm_settings()
        disabled_groups = settings.get("disabled_groups", [])
        
        if not disabled_groups:
            bot.reply_to(message, "📭 No groups have DM filters disabled!")
            return
        
        # Try to get group names
        groups_info = []
        for group_id in disabled_groups:
            try:
                chat = bot.get_chat(group_id)
                group_name = chat.title or "Unknown Group"
                groups_info.append(f"• {group_name} - <code>{group_id}</code>")
            except Exception:
                groups_info.append(f"• Unknown Group - <code>{group_id}</code>")
        
        groups_list = "\n".join(groups_info)
        response = f"🔒 <b>Groups with DM Filters Disabled</b>\n\n{groups_list}\n\nTotal: <code>{len(disabled_groups)}</code> groups"
        
        bot.reply_to(message, response)

    # /bfilters command
    @bot.message_handler(commands=["bfilters"])
    def list_dm_filters(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "🔒 This command is for admins only!")
            return

        all_dm_filters = get_all_dm_filters()
        if not all_dm_filters:
            bot.reply_to(message, "📭 No DM only filters found!")
            return

        parts = message.text.split()
        if len(parts) > 1 and parts[1].lower() == "full":
            all_keys = "\n".join([f"- <code>{f.get('keyword','(no-keyword)')}</code>" for f in all_dm_filters])
            max_chunk = 3800
            if len(all_keys) > max_chunk:
                for i in range(0, len(all_keys), max_chunk):
                    bot.reply_to(message, all_keys[i:i+max_chunk])
            else:
                bot.reply_to(message, f"📋 <b>DM Only Filters</b>:\n{all_keys}")
            return

        page_size = 10
        total_pages = (len(all_dm_filters) + page_size - 1) // page_size
        rows = []
        for fdata in all_dm_filters[:page_size]:
            display = short_display(fdata.get("keyword", ""), limit=50)
            # Use dmfilter_ prefix for DM filters
            rows.append([types.InlineKeyboardButton(display, callback_data=f"dmfilter_{str(fdata.get('_id'))}")])
        
        if total_pages > 1:
            rows.append([types.InlineKeyboardButton("Next ➡️", callback_data="dmfilters_page_1")])
        
        # Use show_dmfull_list for DM filters
        rows.append([types.InlineKeyboardButton("📜 Show Full List", callback_data="show_dmfull_list")])
        bot.reply_to(message, f"📋 DM Only Filters (Page 1/{total_pages}):", reply_markup=make_inline_keyboard(rows))

    # /fstatus command
    @bot.message_handler(commands=["fstatus"])
    def dm_filters_status(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "🔒 This command is for admins only!")
            return
        
        settings = get_dm_settings()
        from db import dm_filters_collection
        dm_filters_count = dm_filters_collection.count_documents({})
        
        status_msg = f"""🔧 <b>DM Filters Status</b>

📊 DM Only Filters: <code>{dm_filters_count}</code>

⚙️ <b>Settings:</b>
• Global DM Filters: <code>{'✅ Enabled' if settings['dm_filters_enabled'] else '❌ Disabled'}</code>
• Creation Mode: <code>{'🔧 DM Only' if settings['creation_mode'] else '⚙️ Normal'}</code>
• Global Groups: <code>{'🌐 All Groups' if settings['global_groups_enabled'] else '🔒 Disabled'}</code>
• Enabled Groups: <code>{len(settings.get('enabled_groups', []))}</code>
• Disabled Groups: <code>{len(settings.get('disabled_groups', []))}</code>"""

        bot.reply_to(message, status_msg)

    # /bstop command - delete dm filter
    @bot.message_handler(commands=["bstop"])
    def bstop_filter(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Sorry, you're not allowed to Stop filters!\n🚫 Only <b>Admins</b> and <b>Authorized Users</b> can use this command.")
            return

        parts = message.text.split(None, 1)
        if len(parts) < 2:
            bot.reply_to(message, "❌ Usage: /bstop keyword")
            return
        keyword = parts[1].strip().lower()
        
        # Try to delete from DM filters
        deleted_dm = delete_dm_filter(keyword)
        
        if deleted_dm:
            # LOG DM FILTER DELETED
            log_message("DM_FILTER_DELETED", f"DM Filter: {keyword}", 
                        message.from_user.id, message.chat.id,
                        message.from_user.username, message.from_user.first_name,
                        message.chat.title if message.chat.title else None)
            
            bot.reply_to(message, f"🗑️ <b>DM Filters</b> removed: <code>{keyword}</code>")
        else:
            bot.reply_to(message, f"⚠️ No DM filter found with keyword: <code>{keyword}</code>")

    # DM Filter callback handler
    @bot.callback_query_handler(func=lambda call: call.data.startswith('dmfilter_'))
    def dm_filter_callback(call):
        """Handle DM filter selection from /bfilters"""
        filter_id = call.data.replace('dmfilter_', '')
        fdata = get_dm_filter_by_id(filter_id)
        
        if not fdata:
            bot.answer_callback_query(call.id, "DM Filter not found!", show_alert=True)
            return
        
        chat_id = call.message.chat.id
        try:
            if fdata["type"] == "text":
                bot.send_message(chat_id, fdata["data"])
            elif fdata["type"] == "photo":
                bot.send_photo(chat_id, fdata["file_id"], caption=fdata.get("caption", ""))
        except Exception:
            bot.answer_callback_query(call.id, "Failed to send DM filter.")
        
        bot.answer_callback_query(call.id)

    # Show DM full list callback
    @bot.callback_query_handler(func=lambda call: call.data == "show_dmfull_list")
    def show_dm_full_list(call):
        """Show full list of DM filters with proper chunking"""
        try:
            all_dm_filters = get_all_dm_filters()
            if not all_dm_filters:
                bot.answer_callback_query(call.id, "📭 No DM filters found!", show_alert=True)
                return
            
            # Create the full list text
            all_keys = "\n".join([f"- <code>{f.get('keyword','(no-keyword)')}</code>" for f in all_dm_filters])
            total_filters = len(all_dm_filters)
            
            # Send with proper chunking
            max_chunk = 3800  # Telegram limit se thoda kam
            header = f"📋 <b>All DM Only Filters</b> (Total: {total_filters}):\n\n"
            
            if len(header + all_keys) <= max_chunk:
                # Ek message mein fit ho jaye toh
                bot.send_message(call.message.chat.id, header + all_keys)
            else:
                # Multiple messages mein send karo
                # Pehle header bhejo
                bot.send_message(call.message.chat.id, header)
                
                # Ab filters ko chunks mein send karo
                current_chunk = ""
                for i, filter_text in enumerate(all_keys.split('\n')):
                    if len(current_chunk + filter_text + '\n') > max_chunk:
                        # Current chunk send karo
                        if current_chunk:
                            bot.send_message(call.message.chat.id, current_chunk)
                        current_chunk = filter_text + '\n'
                    else:
                        current_chunk += filter_text + '\n'
                
                # Last chunk send karo
                if current_chunk:
                    bot.send_message(call.message.chat.id, current_chunk)
            
            bot.answer_callback_query(call.id, f"✅ Sent {total_filters} DM filters!")
            
        except Exception as e:
            print(f"show_dm_full_list failed: {e}")
            try:
                bot.answer_callback_query(call.id, "❌ Failed to send DM filters list.", show_alert=True)
            except:
                pass

    # DM filters pagination callback
    @bot.callback_query_handler(func=lambda call: call.data.startswith("dmfilters_page_"))
    def dm_filters_pagination(call):
        """DM filters pagination"""
        try:
            page = int(call.data.replace("dmfilters_page_", ""))
        except ValueError:
            bot.answer_callback_query(call.id, "Invalid page!")
            return
        
        all_dm_filters = get_all_dm_filters()
        page_size = 10
        total_pages = (len(all_dm_filters) + page_size - 1) // page_size
        start_idx = page * page_size
        end_idx = start_idx + page_size
        
        rows = []
        for fdata in all_dm_filters[start_idx:end_idx]:
            display = short_display(fdata.get("keyword",""), limit=50)
            rows.append([types.InlineKeyboardButton(display, callback_data=f"dmfilter_{str(fdata.get('_id'))}")])
        
        nav = []
        if page > 0:
            nav.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f"dmfilters_page_{page - 1}"))
     
