import discord
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Convert to int as get_channel expects an int

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await send_msg_daily()
    await client.close()
    os._exit(0)

async def send_msg_daily():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Helu I'm Kangaroo. Nhớ report hàng ngày nhé các bạn!!")
    inactive_users = await check_inactive_users()
    await send_inactive_users(inactive_users)

async def check_inactive_users():
    channel = client.get_channel(CHANNEL_ID)

    active_users = set()
    one_day_ago = datetime.now() - timedelta(days=1) - timedelta(minutes=5)
    async for message in channel.history(after=one_day_ago):
        active_users.add(message.author)
    all_channel_members = set(channel.members)
    inactive_users = all_channel_members - active_users
    return inactive_users

async def send_inactive_users(inactive_users):
    channel = client.get_channel(CHANNEL_ID)
    mentions = ' '.join(user.mention for user in inactive_users)
    # print(mentions)
    await channel.send(f'Này các vị {mentions} chưa report nhé!! Đừng tưởng nhờn với Kangaroo đâu!!')

client.run(BOT_TOKEN)