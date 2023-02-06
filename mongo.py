
#importing pymongo
import os
from pymongo import MongoClient
import openai
import asyncio
from config import Config as C
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import CallbackQuery
from pyrogram import enums
from pyrogram.errors import BadRequest
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)
from pyrogram import enums
#connecting to the mongo client
client = MongoClient("mongodb+srv://miladinline:milad64523@cluster0.g7r1i.mongodb.net/?retryWrites=true&w=majority")
logs = -1001829426682
admin= [5361491365]

aienv = os.getenv('OPENAI_KEY')
if aienv == None:
    openai.api_key = input('enter key:')
else:
    openai.api_key = aienv


#accessing the database
#creating database
mydb = client["bot_users"]
users = mydb["users"]

app = Client("bot", C.API_ID, C.API_HASH, C.TOKEN)
@app.on_message(filters.command(["start"]))
async def start(bot, message):
  loop = asyncio.get_event_loop()

  
 
  #adding new user to collaction of users
  if users.find_one({'_id':message.from_user.id}):

     await message.reply(f'''😊 Hi Dear {message.from_user.first_name}
Welcome to MiliChatGPT
Try /help for instructions''',reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton(  # Generates a callback query when pressed
                            "who are you",
                            callback_data="who"
                        )
                        
                    ],
                    [  # Second row
                        InlineKeyboardButton(  # Opens a web URL
                            "help",
                            callback_data="help"
                        )
                        
                    ],
                    [  # Second row
                        InlineKeyboardButton(  # Opens a web URL
                            "donate",
                            url="https://idpay.ir/paymili"
                        ),
                        InlineKeyboardButton(  # Opens the inline interface in the current chat
                            "creator",
                            url="https://t.me/qtmili"
                        )
                    ]
                ]
            )
        )
  else:
    data = {'_id':message.from_user.id,'name' : f'{message.from_user.first_name}','remaining_attempts':0,'status':'allowd'}
    users.insert_one(data)
    new_user = users.find_one({'_id':message.from_user.id})
    add_attept_to_new_user = {'$set': {'remaining_attempts': 15}}
    await message.reply(f'''😊 Hi Dear {message.from_user.first_name}
Welcome to MiliChatGPT
Try /help for instructions\n\ncongrats you got 15 free prompts for starting the bot !''',reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton(  # Generates a callback query when pressed
                            "who are you",
                            callback_data="who"
                        )
                        
                    ],
                    [  # Second row
                        InlineKeyboardButton(  # Opens a web URL
                            "help",
                            callback_data="help"
                        )
                        
                    ],
                    [  # Second row
                        InlineKeyboardButton(  # Opens a web URL
                            "donate",
                            url="https://idpay.ir/paymili"
                        ),
                        InlineKeyboardButton(  # Opens the inline interface in the current chat
                            "creator",
                            url="https://t.me/qtmili"
                        )
                    ]
                    
                ]
            )
        )
    
    users.update_one(new_user,add_attept_to_new_user )
   
        
  
@app.on_message(filters.command(["help"]))
async def help(bot, message):
    await message.reply('''🤓☝️ **help section**\nit's EZ to use the bot you just need to check the example below or check the demo:

**Prompt**
<code>/ask tell me a dad joke about cops</code>''')
  


@app.on_message(filters.command(["list"]))
async def users_list(bot, message):
  user_text = ''
  if message.from_user.id in admin:
    for user in users.find({}):
        
        user_text+=f"name : {user['name']}\nid : {user['_id']}\nremaining prompts : {user['remaining_attempts']}\n\n"
    await message.reply(user_text)   


@app.on_callback_query()
async def cm(c, query):
  if query.data=='help':
    await query.edit_message_text('''**🤓☝️ help section**\nit's EZ to use the bot you just need to check the example below or check the demo:

**Prompt**
<code>/ask tell me a dad joke about cops</code>''',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('< back',callback_data='back')]]))
  elif query.data=='who':  
    await query.edit_message_text('''🤖 Hi, I'm ChatGPT. I'm a natural language processing model that can generate human-like responses to questions. I'm trained on large amounts of conversational data, so I can understand and respond to questions in a conversational way. I'm also able to generate new conversations from scratch. I'm excited to chat with you! \n\n i can do this thinsgs :\n• Generate natural language responses to user input
• Understand and respond to context
• Automate customer service conversations
• Generate personalized content
• Automate FAQs
• Create interactive stories
• Generate product descriptions
• Generate summaries of text
• Automate lead qualification\n\nmade by mili :)''',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('< back',callback_data='back')]]))
  elif query.data=='back':
    await query.edit_message_text(f'''menu : ''',reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton(  # Generates a callback query when pressed
                            "who are you",
                            callback_data="who"
                        )
                        
                    ],
                    [  # Second row
                        InlineKeyboardButton(  # Opens a web URL
                            "help",
                            callback_data="help"
                        )
                        
                    ],
                    [  # Second row
                        InlineKeyboardButton(  # Opens a web URL
                            "donate",
                            url="https://idpay.ir/paymili"
                        ),
                        InlineKeyboardButton(  # Opens the inline interface in the current chat
                            "creator",
                            url="https://t.me/qtmili"
                        )
                    ]
                ]
            )
        )
  elif query.data=='close':
    await query.delete_message_text()      
 






@app.on_message(filters.command(["ban"]))
async def me(bot, message):
  if users.find_one({'_id' : message.from_user.id}):
    ban_it = {'$set': {'status': 'banned'}}
    user_id = users.find_one({'_id':int(message.command[1])})
    users.update_one(user_id,ban_it)
    await message.reply(f"user {user_id['_id']} cant use the bot any more [banned succefully]")


@app.on_message(filters.command(["unban"]))
async def me(bot, message):
  if users.find_one({'_id' : message.from_user.id}):
    unban_it = {'$set': {'status': 'allowd'}}
    user_id = users.find_one({'_id':int(message.command[1])})
    users.update_one(user_id,unban_it)
    await message.reply(f'user {message.command[1]} can now  use the bot [unbanned succefully]')








@app.on_message(filters.command(["me"]))
async def me(bot, message):
  user = users.find_one({'_id' : message.from_user.id})
  if user:
    if user['status']=='allowd':
      users_data = users.find_one({'_id' : message.from_user.id})
      remained_attepts = users_data['remaining_attempts']
      
      profile_text = f'Your Profile:\nname : <code></code>{message.from_user.first_name}\nuser id : <code>{message.from_user.id}</code>\nremaining attempts : <code>{remained_attepts}</code>'
      await message.reply(profile_text)





@app.on_message(filters.command(["ask"]))
async def chat(bot, message):
        user = users.find_one({'_id' : message.from_user.id})
        if user['status']=='allowd':
          
          users_data = users.find_one({'_id' : message.from_user.id})
          remained_attepts = users_data['remaining_attempts']
          
          if remained_attepts!=0:
      
            if len(message.command)==1:
                pass
            else:
                
                # print(message)
                text = ' '.join(message.command[1:])
                await app.forward_messages(logs, message.chat.id, message.id)
                await app.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
                try:
                    answer = await app.send_message(message.chat.id,openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=text,
                        max_tokens=1024,
                        temperature=0.3
                    )["choices"][0]["text"]+f'\n\n<code>Fetch by miliChatGPT \n**remainig attempts**  {remained_attepts}</code>',reply_to_message_id=message.id)
                    await app.forward_messages(logs, message.chat.id, answer.id)
                    
                    reduced_attept = {'$set': {'remaining_attempts': int(users_data['remaining_attempts'])-1}}
                    users.update_one(users_data, reduced_attept)
                    


                 

                except Exception as e:
                    
                    for i in admin:
                        await app.send_message(i,e)
          else:
            await message.reply('You have no more attempts to try :( \n check your profile using /me') 




@app.on_message(filters.command(["add"]))
async def add(bot, message):
  if message.from_user.id in admin:
  
    text = ' '.join(message.command[1:])
    
    if message.command[1]=='all':
      
      for user in users.find({}):
          
          additional_attempt = {'$set': {'remaining_attempts': int(user['remaining_attempts'])+int(message.command[2])}}
          users.update_one(user, additional_attempt)
      await message.reply(f'{additional_attempt} prompts added to all users ')   
    else:
        user_to_add = users.find_one({'_id':int(message.command[1])}) 
        
        attempts_to_add = {'$set':{'remaining_attempts': int(user_to_add['remaining_attempts'])+int(message.command[2])}}
        users.update_one(user_to_add,attempts_to_add)
        await message.reply(f'{message.command[2]} prompts added to {message.command[1]}')
        await app.send_message(int(message.command[1]),f"{message.command[2]} prompts add to your profie by admin")
     





@app.on_message(filters.command(["reset"]))
async def reset(bot, message):
  if message.from_user.id in admin:
    for user in users.find({}):
       
        reset_attemp = {'$set': {'remaining_attempts': 0}}
        users.update_one(user, reset_attemp)
    await message.reply('all users prompts set to 0 now ')
 




@app.on_message(filters.command(["empty"]))
async def empty(bot, message):
  if message.from_user.id in admin:
    for i in users.find({}):
      users.find_one_and_delete(i)
    await message.reply('all users are now removed from db')   
 


  








if __name__ == '__main__':
    print('[BOT] im running ')
    app.run()


























# print('db created')
#creating collections


# #listing collections
# data = {'_id':20938505830912,'user_id':52,'user_name' : 'milad','remaining_attempts':3,'aq' : 21}
# mycol1.insert_one(data)

# # print(mydb.list_collection_names())

# cursor = mycol1.find({})
# for document in cursor:
#             print(document)