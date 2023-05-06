import time
from telethon import TelegramClient, events
import asyncio
from time import sleep
from Arab import iqthon
# DATA


# ON WATCH


On_WatchREPLY = {}

@iqthon.on(events.NewMessage(outgoing=True, pattern=r'.اضف رد نيو ?(.*)'))
async def AddReply(event):
    # GET CHAT INFORMATON - MESSAGE
    chat = await event.get_chat()
    
    try:
        if event.is_private != True :
            if event.is_group == True :
                if chat.id not in On_WatchREPLY:
                    On_WatchREPLY[chat.id] = {
                        "id": chat.id,
                        "username": chat.username,
                        "replies": {
                            "reply_1": {
                                "waiting_message": (event.message.message).split('-')[1],
                                "reply_message": (event.message.message).split('-')[2]
                            }
                        }
                    }
                else:
                    replies = On_WatchREPLY[chat.id]["replies"]
                    reply_count = len(replies)+1
                    while f'reply_{reply_count}' in On_WatchREPLY[chat.id]["replies"]:
                        reply_count += 1
                    On_WatchREPLY[chat.id]["replies"][f'reply_{reply_count}'] = {
                        "waiting_message": (event.message.message).split('-')[1],
                        "reply_message": (event.message.message).split('-')[2]
                    }
                    
                order = await event.edit('**تم اضافة الرد**')
            else:
                order = await event.edit('**لا يمكن تنفيذ الامر هنا!**')
        else:
            order = await event.edit('**لا يمكن تنفيذ الامر هنا!**')
    except:
        on_except = await event.edit('**استخدم هذه الصيغة ( .اضف رد نيو - الرسالة - رسالة الرد )**') 
    

# REMOVE ALL REPLIES
@iqthon.on(events.NewMessage(outgoing=True, pattern='.حذف نيوود نيو'))
async def RemoveReply(event):
    # CLEAR ALL On_WatchREPLY GROUPS
    chat = await event.get_chat()
    clear_ = On_WatchREPLY.pop(chat.id)
    order = await event.edit('**تم حذف نيوود نيو**')
    

# SHOW ALL REPLIES
@iqthon.on(events.NewMessage(outgoing=True, pattern='.اضهر ردود نيو'))
async def ShowAllReplies(event):
    # GET ALL REPLIES
    replies = ''
    chat = await event.get_chat()
    
    if len(On_WatchREPLY) == 0:
        on_exit = await event.edit('**لا يوجد ردود!**')
    else:
        if chat.id in On_WatchREPLY:
            if On_WatchREPLY[chat.id]["username"] == None:
                username = On_WatchREPLY[chat.id]["id"]
            else:
                username = On_WatchREPLY[chat.id]["username"]
                    
            replies_ = On_WatchREPLY[chat.id]["replies"]
            for reply in replies_:
                sender_message, reply_message = On_WatchREPLY[chat.id]["replies"][reply]["waiting_message"], On_WatchREPLY[chat.id]["replies"][reply]["reply_message"]
                replies = replies + f'@{username} > {sender_message} > {reply_message}\n'
                    
            on_success = await event.edit(f'**{replies}**')
        else:
            on_exit = await event.edit('**لا يوجد ردود في هذه القناة!**')


# REMOVE SPICEFIC REPLY
@iqthon.on(events.NewMessage(outgoing=True, pattern=r'.حذف نيو ?(.*)'))
async def RemoveReply(event):
    # MESSAGE TO REMOVE
    ToRemove = (event.message.message).replace('.حذف نيو', '')
    chat = await event.get_chat()
    
    if len(On_WatchREPLY) == 0:
        on_exit = await event.edit('**لا يوجد ردود!**')
    else:
        Not_found = True
        
        replies = On_WatchREPLY[chat.id]["replies"]
        for reply in replies:
            reply_ = On_WatchREPLY[chat.id]["replies"][reply]["waiting_message"]
            id = On_WatchREPLY[chat.id]["id"]
               
            if (reply_.lower()).strip() == (ToRemove.lower()).strip():
                Not_found = False
                On_WatchREPLY[chat.id]["replies"].pop(reply)
                on_success = await event.edit('**تم حذف الرد**')
                break

        if Not_found == True:
            on_failed = await event.edit('**الرد لا يوجد في القائمة**')
                
        Not_found = True


# WAIT CHAT ACTIONS
@iqthon.on(events.NewMessage(outgoing=False))
async def ReplyAction(event):
    # GET CHAT INFORMATION
    chat = await event.get_chat()
    
    if event.is_private != True :
        if chat.id in On_WatchREPLY :
            await asyncio.sleep(4)
            replies = On_WatchREPLY[chat.id]["replies"]
            for reply in replies:
                waiting_reply = On_WatchREPLY[chat.id]["replies"][reply]["waiting_message"]
                send_to_reply = On_WatchREPLY[chat.id]["replies"][reply]["reply_message"]
                group_id = On_WatchREPLY[chat.id]["id"]
                
                if (waiting_reply.lower()).strip() in (event.text).lower():
                    os_success = await event.reply(send_to_reply)
                    break




