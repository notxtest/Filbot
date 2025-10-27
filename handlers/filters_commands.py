from telebot import types
from config import ADMIN_ID, OTHER_ADMINS, LOGS_CHANNEL
from db import save_filter, delete_filter, get_filter, get_filter_by_id, get_all_filters
from db import update_user_data, short_display
import re

def register_filters_handlers(bot):
    
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

    # /filter command - add filter (admin only)
    @bot.message_handler(commands=["filter"])
    def add_filter_handler(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Sorry, you're not allowed to add filters!\n     🚫 Only <b>Admins</b> and <b>Authorized Users</b> can use this command.")
            return

        if not message.reply_to_message:
            bot.reply_to(message, "❌ Reply to a message to save as filter!")
            return

        parts = message.text.split(None, 1)
        if len(parts) < 2:
            bot.reply_to(message, "❌ Usage: /filter keyword (reply to message)")
            return
        keyword = parts[1].strip()

        reply_msg = message.reply_to_message
        filter_data = {}
        if reply_msg.content_type == "text":
            filter_data = {"type": "text", "data": reply_msg.text}
        elif reply_msg.content_type == "photo":
            file_id = reply_msg.photo[-1].file_id
            filter_data = {"type": "photo", "file_id": file_id, "caption": reply_msg.caption or ""}
        else:
            bot.reply_to(message, "⚠️ Only text and photo filters are supported!")
            return

        # Check if DM only creation mode is enabled
        from db import get_dm_settings
        settings = get_dm_settings()
        if settings["creation_mode"]:
            from db import save_dm_filter
            save_dm_filter(keyword, filter_data)
            
            # LOG DM FILTER ADDED
            log_message("DM_FILTER_ADDED", f"DM Filter: {keyword}", 
                        message.from_user.id, message.chat.id,
                        message.from_user.username, message.from_user.first_name,
                        message.chat.title if message.chat.title else None,
                        f"Type: {filter_data['type']}")
            
            bot.reply_to(message, f"✅ <b>DM Only Filter</b> saved for: <code>{keyword}</code>")
        else:
            save_filter(keyword, filter_data)
            
            # LOG NORMAL FILTER ADDED
            log_message("FILTER_ADDED", f"Normal Filter: {keyword}", 
                        message.from_user.id, message.chat.id,
                        message.from_user.username, message.from_user.first_name,
                        message.chat.title if message.chat.title else None,
                        f"Type: {filter_data['type']}")
            
            bot.reply_to(message, f"✅ <b>Filter saved for:</b> <code>{keyword}</code>")

    # /stop command - delete filter
    @bot.message_handler(commands=["stop"])
    def stop_filter_handler(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "⚠️ Sorry, you're not allowed to Stop filters!\n🚫 Only <b>Admins</b> and <b>Authorized Users</b> can use this command.")
            return

        parts = message.text.split(None, 1)
        if len(parts) < 2:
            bot.reply_to(message, "❌ Usage: /stop keyword")
            return
        keyword = parts[1].strip().lower()
        
        # Try to delete from normal filter 
        deleted_normal = delete_filter(keyword)   
        
        if deleted_normal:
            # LOG FILTER DELETED
            log_message("FILTER_DELETED", f"Normal Filter: {keyword}", 
                        message.from_user.id, message.chat.id,
                        message.from_user.username, message.from_user.first_name,
                        message.chat.title if message.chat.title else None)
            
            bot.reply_to(message, f"🗑️ <b>Normal Filter</b> removed: <code>{keyword}</code>")
        else:
            bot.reply_to(message, f"⚠️ No filter found with keyword: <code>{keyword}</code>")

    # /filters admin command
    @bot.message_handler(commands=["filters"])
    def list_filters_handler(message):
        sender = message.from_user.id if message.from_user else None
        if sender not in [ADMIN_ID] + OTHER_ADMINS:
            bot.reply_to(message, "🔒 This command is for admins only to view stats!")
            return

        all_filters = get_all_filters()
        if not all_filters:
            bot.reply_to(message, "📭 No filters found!")
            return

        parts = message.text.split()
        if len(parts) > 1 and parts[1].lower() == "full":
            all_keys = "\n".join([f"- <code>{f.get('keyword','(no-keyword)')}</code>" for f in all_filters])
            max_chunk = 3800
            if len(all_keys) > max_chunk:
                for i in range(0, len(all_keys), max_chunk):
                    bot.reply_to(message, all_keys[i:i+max_chunk])
            else:
                bot.reply_to(message, f"📋 <b>Available Filters</b>:\n{all_keys}")
            return

        page_size = 10
        total_pages = (len(all_filters) + page_size - 1) // page_size
        rows = []
        for fdata in all_filters[:page_size]:
            display = short_display(fdata.get("keyword", ""), limit=50)
            rows.append([types.InlineKeyboardButton(display, callback_data=f"admin_filter_{str(fdata.get('_id'))}")])
        if total_pages > 1:
            rows.append([types.InlineKeyboardButton("Next ➡️", callback_data="filters_page_1")])
        rows.append([types.InlineKeyboardButton("📜 Show Full List", callback_data="show_full_list")])
        bot.reply_to(message, f"📋 Available Filters (Page 1/{total_pages}):", reply_markup=make_inline_keyboard(rows))

    # Filter callback handler
    @bot.callback_query_handler(func=lambda call: call.data.startswith('admin_filter_'))
    def admin_filter_callback(call):
        filter_id = call.data.replace('admin_filter_', '')
        fdata = get_filter_by_id(filter_id)
        
        if not fdata:
            bot.answer_callback_query(call.id, "Filter not found!", show_alert=True)
            return
        
        if fdata["type"] == "text":
            preview = f"📝 Text Filter: {fdata['data'][:200]}..."
        else:
            preview = f"🖼️ Photo Filter\nCaption: {fdata.get('caption','No caption')[:200]}..."
        bot.answer_callback_query(call.id, preview, show_alert=True)

    # Show full list callback
    @bot.callback_query_handler(func=lambda call: call.data == "show_full_list")
    def show_full_list_callback(call):
        all_filters = get_all_filters()
        all_keys = "\n".join([f"- <code>{f.get('keyword','(no-keyword)')}</code>" for f in all_filters])
        max_chunk = 3800
        try:
            if len(all_keys) > max_chunk:
                for i in range(0, len(all_keys), max_chunk):
                    bot.send_message(call.message.chat.id, all_keys[i:i+max_chunk])
            else:
                bot.send_message(call.message.chat.id, f"📋 <b>All Filters</b>:\n{all_keys}")
        except Exception:
            bot.answer_callback_query(call.id, "Unable to send list.")
        bot.answer_callback_query(call.id)

    # Filters pagination callback
    @bot.callback_query_handler(func=lambda call: call.data.startswith("filters_page_"))
    def filters_pagination_callback(call):
        try:
            page = int(call.data.replace("filters_page_", ""))
        except ValueError:
            bot.answer_callback_query(call.id, "Invalid page!")
            return
        
        all_filters = get_all_filters()
        page_size = 10
        total_pages = (len(all_filters) + page_size - 1) // page_size
        start_idx = page * page_size
        end_idx = start_idx + page_size
        
        rows = []
        for fdata in all_filters[start_idx:end_idx]:
            display = short_display(fdata.get("keyword",""), limit=50)
            rows.append([types.InlineKeyboardButton(display, callback_data=f"admin_filter_{str(fdata.get('_id'))}")])
        
        nav = []
        if page > 0:
            nav.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f"filters_page_{page - 1}"))
        if end_idx < len(all_filters):
            nav.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"filters_page_{page + 1}"))
        if nav:
            rows.append(nav)
        
        rows.append([types.InlineKeyboardButton("📜 Show Full List", callback_data="show_full_list")])
        
        try:
            bot.edit_message_text(f"📋 Available Filters (Page {page + 1}/{total_pages}):", 
                                call.message.chat.id, call.message.message_id, 
                                reply_markup=make_inline_keyboard(rows))
            bot.answer_callback_query(call.id)
        except Exception:
            bot.answer_callback_query(call.id, "Unable to paginate.")

    # Letter selection handler (private)
    @bot.message_handler(func=lambda m: (m.chat.type == "private") and bool(re.fullmatch(r"[0-9A-Za-z]|Other", (m.text or ""), flags=re.IGNORECASE)))
    def letter_selection_handler(message):
        selected_char = (message.text or "").upper().strip()
        update_user_data(message.from_user.id, message.chat.id, bot.token)
        if selected_char == "OTHER":
            regex_filter = {"keyword": {"$regex": "^[^a-zA-Z0-9]"}}
        else:
            regex_filter = {"keyword": {"$regex": f"^{re.escape(selected_char)}", "$options": "i"}}

        # Check DM filter settings for keyboard
        from db import get_dm_settings, dm_filters_collection
        settings = get_dm_settings()
        if settings["dm_filters_enabled"]:
            # If /openfilter is ON, combine both normal and DM filters
            normal_filters = list(get_all_filters())
            normal_filters = [f for f in normal_filters if re.match(f"^{re.escape(selected_char)}", f.get('keyword',''), re.IGNORECASE) or (selected_char == "OTHER" and not re.match(r"^[a-zA-Z0-9]", f.get('keyword','')))]
            dm_filters = list(dm_filters_collection.find(regex_filter).sort("keyword", 1))
            filters_list = normal_filters + dm_filters
            filters_list = sorted(filters_list, key=lambda x: x.get("keyword", ""))
        else:
            # If /closefilter is OFF, show only normal filters
            filters_list = list(get_all_filters())
            filters_list = [f for f in filters_list if re.match(f"^{re.escape(selected_char)}", f.get('keyword',''), re.IGNORECASE) or (selected_char == "OTHER" and not re.match(r"^[a-zA-Z0-9]", f.get('keyword','')))]
        
        if not filters_list:
            bot.reply_to(message, f"No filters found starting with '{selected_char}'", reply_markup=types.ReplyKeyboardRemove())
            return

        rows = []
        row = []
        for fdata in filters_list[:50]:
            display = short_display(fdata.get("keyword",""), limit=40)
            # Check if it's DM filter or normal filter and set callback accordingly
            if settings["dm_filters_enabled"] and dm_filters_collection.find_one({"_id": fdata.get('_id')}):
                # DM filter hai - use dmfilter_ prefix
                btn = types.InlineKeyboardButton(display, callback_data=f"dmfilter_{str(fdata['_id'])}")
            else:
                # Normal filter hai - use filter_ prefix  
                btn = types.InlineKeyboardButton(display, callback_data=f"filter_{str(fdata['_id'])}")
            row.append(btn)
            if len(row) == 2:
                rows.append(row)
                row = []
        if row:
            rows.append(row)

        if len(filters_list) > 50:
            rows.append([types.InlineKeyboardButton("⬅️ Previous", callback_data=f"page_prev_{selected_char}_0"),
                         types.InlineKeyboardButton("Next ➡️", callback_data=f"page_next_{selected_char}_0")])

        rows.append([types.InlineKeyboardButton("🔙 Back", callback_data="back_to_letters")])

        try:
            bot.reply_to(message, "⌛ Loading filters...", reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(message.chat.id, f"🔍 Filters starting with '{selected_char}':", reply_markup=make_inline_keyboard(rows))
        except Exception as e:
            print(f"letter_selection_handler failed: {e}")

    # Filter selection callback
    @bot.callback_query_handler(func=lambda call: call.data.startswith('filter_'))
    def filter_callback(call):
        filter_id = call.data.replace('filter_', '')
        fdata = get_filter_by_id(filter_id)
        
        if not fdata:
            bot.answer_callback_query(call.id, "Filter not found!", show_alert=True)
            return
        
        chat_id = call.message.chat.id
        try:
            if fdata["type"] == "text":
                bot.send_message(chat_id, fdata["data"])
            elif fdata["type"] == "photo":
                bot.send_photo(chat_id, fdata["file_id"], caption=fdata.get("caption", ""))
        except Exception:
            bot.answer_callback_query(call.id, "Failed to send filter.")
        
        bot.answer_callback_query(call.id)

    # Back to letters callback
    @bot.callback_query_handler(func=lambda call: call.data == "back_to_letters")
    def back_to_letters_callback(call):
        ANIME_KEYBOARD_LETTERS = [
            ["0","1","2","3","4","5","6","7","8","9"],
            ["A","B","C","D","E","F","G","H","I","J","K","L","M"],
            ["N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
            ["Other"]
        ]
        
        def make_reply_keyboard(rows):
            rk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for row in rows:
                rk.row(*[types.KeyboardButton(text) for text in row])
            return rk
            
        rk = make_reply_keyboard(ANIME_KEYBOARD_LETTERS)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        try:
            bot.send_message(call.message.chat.id, "🔍 Select a letter to browse anime filters:", reply_markup=rk)
        except Exception:
            bot.answer_callback_query(call.id, "Unable to open letters.")

    # Pagination callbacks
    @bot.callback_query_handler(func=lambda call: call.data.startswith("page_"))
    def page_callback(call):
        page_match = re.match(r"^page_(prev|next)_([A-Z0-9]+)_(\d+)$", call.data)
        if page_match:
            direction, char, current_page = page_match.groups()
            current_page = int(current_page)
            new_page = current_page - 1 if direction == "prev" else current_page + 1
            offset = new_page * 50
            
            if char == "OTHER":
                regex_filter = {"keyword": {"$regex": "^[^a-zA-Z0-9]"}}
            else:
                regex_filter = {"keyword": {"$regex": f"^{re.escape(char)}", "$options": "i"}}
            
            # UPDATED: Check DM filter settings for #anime keyboard
            from db import get_dm_settings, dm_filters_collection
            settings = get_dm_settings()
            if settings["dm_filters_enabled"]:
                # If /openfilter is ON, combine both normal and DM filters
                normal_filters = list(get_all_filters())
                normal_filters = [f for f in normal_filters if re.match(f"^{re.escape(char)}", f.get('keyword',''), re.IGNORECASE) or (char == "OTHER" and not re.match(r"^[a-zA-Z0-9]", f.get('keyword','')))]
                dm_filters = list(dm_filters_collection.find(regex_filter).sort("keyword", 1))
                filters_list = normal_filters + dm_filters
                filters_list = sorted(filters_list, key=lambda x: x.get("keyword", ""))[offset:offset+50]
            else:
                # If /closefilter is OFF, show only normal filters
                filters_list = list(get_all_filters())
                filters_list = [f for f in filters_list if re.match(f"^{re.escape(char)}", f.get('keyword',''), re.IGNORECASE) or (char == "OTHER" and not re.match(r"^[a-zA-Z0-9]", f.get('keyword','')))]
                filters_list = filters_list[offset:offset+50]
                
            if not filters_list:
                bot.answer_callback_query(call.id, "No more filters to show!")
                return
            
            rows = []
            r = []
            for fdata in filters_list:
                display = short_display(fdata.get("keyword", ""), limit=40)
                # Check if it's DM filter or normal filter
                if settings["dm_filters_enabled"] and dm_filters_collection.find_one({"_id": fdata.get('_id')}):
                    btn = types.InlineKeyboardButton(display, callback_data=f"dmfilter_{str(fdata['_id'])}")
                else:
                    btn = types.InlineKeyboardButton(display, callback_data=f"filter_{str(fdata['_id'])}")
                r.append(btn)
                if len(r) == 2:
                    rows.append(r)
                    r = []
            if r:
                rows.append(r)
            
            nav = []
            if offset > 0:
                nav.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f"page_prev_{char}_{new_page}"))
            if len(filters_list) == 50:
                nav.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"page_next_{char}_{new_page}"))
            if nav:
                rows.append(nav)
            
            rows.append([types.InlineKeyboardButton("🔙 Back", callback_data="back_to_letters")])
            
            try:
                bot.edit_message_text(f"🔍 Filters starting with '{char}' (Page {new_page + 1}):", 
                                    call.message.chat.id, call.message.message_id, 
                                    reply_markup=make_inline_keyboard(rows))
                bot.answer_callback_query(call.id)
            except Exception:
                bot.answer_callback_query(call.id, "Unable to update.")

    # Filter responder for exact keyword matches
    @bot.message_handler(func=lambda m: (m.content_type == "text") and (m.chat.type in ("private","group","supergroup")))
    def filter_responder(message):
        try:
            # BUG FIX: Only update groups, NOT users (unless it's private chat)
            if message.chat.type != "private":
                from db import groups_collection
                groups_collection.update_one(
                    {"chat_id": message.chat.id, "bot_token": bot.token},
                    {"$set": {"chat_id": message.chat.id, "bot_token": bot.token}},
                    upsert=True
                )
            else:
                # Private chat mein dono update karo
                update_user_data(message.from_user.id, message.chat.id, bot.token)
        except Exception:
            pass

        text = (message.text or "").lower().strip()
        
        # Check DM only filters first (if enabled)
        from db import get_dm_settings, get_dm_filter, is_dm_filter_enabled_for_group
        settings = get_dm_settings()
        if settings["dm_filters_enabled"]:
            if message.chat.type == "private" or is_dm_filter_enabled_for_group(message.chat.id):
                dm_fdata = get_dm_filter(text)
                if dm_fdata:
                    try:
                        # LOG FILTER USAGE
                        log_message("FILTER_USED", f"DM Filter: {text}", 
                                  message.from_user.id if message.from_user else None,
                                  message.chat.id,
                                  message.from_user.username if message.from_user else None,
                                  message.from_user.first_name if message.from_user else None,
                                  message.chat.title if message.chat.title else None,
                                  f"Type: {dm_fdata['type']}")
                        
                        if dm_fdata["type"] == "text":
                            bot.reply_to(message, dm_fdata["data"])
                        elif dm_fdata["type"] == "photo":
                            bot.reply_photo(message.chat.id, dm_fdata["file_id"], caption=dm_fdata.get("caption",""))
                        return
                    except Exception:
                        print(f"DM filter_responder send failed")
                        return
        
        # Original normal filters logic
        fdata = get_filter(text)
        if fdata:
            try:
                # LOG FILTER USAGE
                log_message("FILTER_USED", f"Normal Filter: {text}", 
                          message.from_user.id if message.from_user else None,
                          message.chat.id,
                          message.from_user.username if message.from_user else None,
                          message.from_user.first_name if message.from_user else None,
                          message.chat.title if message.chat.title else None,
                          f"Type: {fdata['type']}")
                
                if fdata["type"] == "text":
                    bot.reply_to(message, fdata["data"])
                elif fdata["type"] == "photo":
                    bot.reply_photo(message.chat.id, fdata["file_id"], caption=fdata.get("caption",""))
                return
            except Exception:
                print(f"filter_responder send failed")
                return
        
        # Pattern matching for partial keywords
        all_filters = get_all_filters()
        for filter_data in all_filters:
            keyword = filter_data.get("keyword", "").lower()
            if keyword:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text):
                    try:
                        # LOG FILTER USAGE (pattern match)
                        log_message("FILTER_USED", f"Pattern Match: {text} -> {keyword}", 
                                  message.from_user.id if message.from_user else None,
                                  message.chat.id,
                                  message.from_user.username if message.from_user else None,
                                  message.from_user.first_name if message.from_user else None,
                                  message.chat.title if message.chat.title else None,
                                  f"Type: {filter_data['type']}")
                        
                        if filter_data["type"] == "text":
                            bot.reply_to(message, filter_data["data"])
                        elif filter_data["type"] == "photo":
                            bot.reply_photo(message.chat.id, filter_data["file_id"], caption=filter_data.get("caption",""))
                        break
                    except Exception:
                        print(f"filter_responder send failed")
                        break
