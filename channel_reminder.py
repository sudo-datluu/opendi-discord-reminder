import discord
import os
import argparse
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await send_msg_daily()
    await client.close()
    os._exit(0)

async def send_msg_daily():
    channel = client.get_channel(DAILY_REPORT_CHANNEL_ID)
    await channel.send("Helu I'm Kangaroo. Nhớ report hàng ngày nhé các bạn!!")
    inactive_users = await check_inactive_users()
    await send_inactive_users(inactive_users)

async def check_inactive_users():
    channels = [client.get_channel(DAILY_REPORT_CHANNEL_ID), client.get_channel(GENERAL_CHANNEL_ID)]
    active_users = set()
    one_day_ago = datetime.now() - timedelta(days=1) - timedelta(minutes=5)

    for channel in channels:
        async for message in channel.history(after=one_day_ago):
            active_users.add(message.author)
    
    all_channel_members = set(channel.members)
    inactive_users = all_channel_members - active_users
    return inactive_users

async def send_inactive_users(inactive_users):
    channel = client.get_channel(DAILY_REPORT_CHANNEL_ID)
    mention_users = [user for user in inactive_users if user.name not in OFF_USERS and not user.bot]
    if mention_users:
        mentions = ' '.join(user.mention for user in mention_users)
        await channel.send(f'Này các vị {mentions} chưa report nhé!! Đừng tưởng nhờn với Kangaroo đâu!!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--test-mode', dest='test_mode', action='store_true')
    parser.set_defaults(test_mode=False)

    args = parser.parse_args()
    
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # Convert to int as get_channel expects an int
    DAILY_REPORT_CHANNEL_ID = int(os.getenv("DAILY_REPORT_CHANNEL_ID")) if not args.test_mode else  int(os.getenv("DAILY_REPORT_TEST_CHANNEL_ID"))
    GENERAL_CHANNEL_ID = int(os.getenv("GENERAL_CHANNEL_ID"))  

    OFF_USERS = ['phoebe0830']
    client.run(BOT_TOKEN)
    