import discord 
from discord.ext import commands 
import logging 
from dotenv import load_dotenv
import os 


load_dotenv()
token = os.getenv('DISCORD_TOKEN')


handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode = 'w')
intents = discord.Intents.default()
intents.message_content= True
intents.members = True


bot = commands.Bot(command_prefix='.',intents=intents)

def load_words(filepath):
    with open (filepath,'r',encoding='utf-8') as f:
        return set(line.strip().lower() for line in f if line.strip())
    
banned_words = load_words('swear_words.txt') | load_words('hindi_galli.txt')

    


@bot.event
async def on_ready():
    print(f'We are ready for launch,{bot.user.name}')

@bot.event
async def on_memeber_join(member):
    await member.send(f"{member.name}Welcome to my bot testing server")

# @bot.event 
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if "muji" in message.content.lower():
#         # await message.delete()
#         await message.channel.send(f"{message.author.mention} testo na bola na")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check each word in the message against the banned set
    words_in_message = message.content.lower().split()
    if any(word in banned_words for word in words_in_message):
        await message.delete()
        await message.channel.send(
            f"{message.author.mention}, watch your language.", delete_after=5 #this works it will delete message and it's own message after 5 sec seound interesting 
        )
        return  # Don't process commands if message was deleted
    
    await bot.process_commands(message)
        


bot.run(token,log_handler= handler,log_level=logging.DEBUG)

