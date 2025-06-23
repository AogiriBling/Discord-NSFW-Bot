import discord
import asyncio
import random
import aiohttp

TOKEN = "your token"
CHANNEL_ID = 'channel id'
NSFW_TYPES = [
    "cosplay",
    "hentai",
    "ass",
    "pgif",
    "swimsuit",
    "thigh",
    "hass",
    "boobs",
    "hboobs",
    "pussy",
    "paizuri",
    "pantsu",
    "lewdneko",
    "feet",
    "hyuri",
    "hthigh",
    "hmidriff",
    "anal",
    "nakadashi",
    "blowjob",
    "gonewild",
    "hkitsune",
    "tentacle",
    "4k",
    "kanna",
    "hentai_anal",
    "food",
    "neko",
    "holo",
    "pee",
    "kemonomimi",
    "coffee",
    "yaoi", # this is gay shit
    "futa", # this is female transgender shit
    "gah"
]

class NSFWAutoBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        self.loop.create_task(self.auto_send_nsfw())

    async def fetch_nsfw_content(self, content_type):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://nekobot.xyz/api/image?type={content_type}') as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('message')
                return None

    async def auto_send_nsfw(self):
        await self.wait_until_ready()
        channel = self.get_channel(int(CHANNEL_ID))
        
        if not channel:
            print(f"Channel with ID {CHANNEL_ID} not found!")
            return
            
        if not channel.is_nsfw():
            print(f"Channel {channel.name} is not marked as NSFW!")
            return

        while not self.is_closed():
            try:
                content_type = random.choice(NSFW_TYPES)
                content_url = await self.fetch_nsfw_content(content_type)
                
                if content_url:
                    embed = discord.Embed(color=discord.Color.from_rgb(255, 255, 255))
                    embed.set_image(url=content_url)
                    embed.set_footer(text="Discord.gg/freefollow | Bling is Awesome!")
                    
                    await channel.send(embed=embed)
                    print(f"Sent {content_type} content to {channel.name}")
                else:
                    print(f"Failed to fetch {content_type} content")
                
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(30)

intents = discord.Intents.default()
intents.message_content = True

client = NSFWAutoBot(intents=intents)
client.run(TOKEN)