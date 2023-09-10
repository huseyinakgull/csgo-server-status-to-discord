import discord
import requests
import asyncio

TOKEN = 'BOT_TOKENINIZI_GIRIN'
GUILD_ID = 'SUNUCU_ID'
CHANNEL_ID = 'KANAL_ID'
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

SERVER_IP = "SUNUCU_ADRESI"
SERVER_PORT = 27015
STEAM_API_KEY = "STEAM_WEB_API_KEYINIZ"
APPID = "OYUN_IDSI(CSGO 730)"

baslik = "Marauders Jailbreak Sunucu Panosu"

async def get_server_info(ip, port):
    try:
        url = f"https://api.steampowered.com/IGameServersService/GetServerList/v1/?key={STEAM_API_KEY}&filter=appid\\{APPID}\\addr\\{ip}:{port}"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if data.get("response") and data["response"]["servers"]:
            server_info = data["response"]["servers"][0]
            return server_info
        else:
            return None
    except Exception as e:
        print("Sunucu bilgileri alınamadı:", str(e))
        return None

async def send_server_info():
    await client.wait_until_ready()
    channel = client.get_channel(int(CHANNEL_ID))
    while not client.is_closed():
        server_info = await get_server_info(SERVER_IP, SERVER_PORT)
        if server_info:
            embed = discord.Embed(title=baslik, color=discord.Color.from_rgb(255, 255, 255))
            embed.add_field(name="Sunucu Adresi", value=f"```{SERVER_IP}```", inline=True)
            embed.add_field(name="Sunucu Portu", value=f"```{SERVER_PORT}```", inline=True)
            embed.add_field(name="Sunucu Adı", value=f"```{server_info['name']}```", inline=True)
            embed.add_field(name="Aktif Oyuncu Sayısı", value=f"```{server_info['players']}/{server_info['max_players']}```", inline=True)
            if hasattr(client, 'last_message'):
                await client.last_message.edit(content="", embed=embed)
            else:
                client.last_message = await channel.send(embed=embed)

        await asyncio.sleep(60)
        
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await send_server_info()

client.run(TOKEN)
