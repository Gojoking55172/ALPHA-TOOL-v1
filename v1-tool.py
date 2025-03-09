import os
import time
import discord
import requests
from pystyle import Colors, Colorate

TOKEN_FILE = "tokens.txt"
NITRO_FILE = "Nitroid.txt"

# UI Header
def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(Colorate.Horizontal(Colors.red_to_blue, """
 █████╗ ██╗     ██████╗ ██╗  ██╗ █████╗      ████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██║     ██╔══██╗██║  ██║██╔══██╗     ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
███████║██║     ██████╔╝███████║███████║        ██║   ██║   ██║██║   ██║██║     
██╔══██║██║     ██╔═══╝ ██╔══██║██╔══██║        ██║   ██║   ██║██║   ██║██║     
██║  ██║███████╗██║     ██║  ██║██║  ██║        ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
                        ALPHA STUDIO TOOL 
    """))

# टोकन लोड करना
def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def load_nitro_tokens():
    if os.path.exists(NITRO_FILE):
        with open(NITRO_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

# **1. Token से Discord Server जॉइन करना**
def join_server(invite):
    tokens = load_tokens()
    for token in tokens:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        response = requests.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers)
        if response.status_code == 200:
            print(f"[✔] Token {token[:20]}... ने सर्वर जॉइन किया!")
        else:
            print(f"[X] जॉइन फेल {response.status_code}")

# **2. सभी टोकन को ऑनलाइन करना**
def online_tokens():
    tokens = load_tokens()
    for token in tokens:
        client = discord.Client(intents=discord.Intents.default())

        @client.event
        async def on_ready():
            print(f"[✔] {client.user} ऑनलाइन हो गया!")
        
        try:
            client.run(token, bot=False)
        except:
            print(f"[X] {token[:20]}... फेल हुआ")

# **3. Bot Token से Channel बनाना और Msg भेजना**
def create_channel(bot_token, guild_id, channel_name, message):
    headers = {"Authorization": f"Bot {bot_token}", "Content-Type": "application/json"}
    data = {"name": channel_name, "type": 0}

    response = requests.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=headers, json=data)
    
    if response.status_code == 201:
        channel_id = response.json()["id"]
        print(f"[✔] चैनल {channel_name} बना!")
        
        msg_data = {"content": message}
        requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=msg_data)
        print(f"[✔] Msg भेजा: {message}")
    else:
        print(f"[X] चैनल बनाना फेल {response.status_code}")

# **4. Auto Boost सर्वर**
def auto_boost(server_invite):
    tokens = load_nitro_tokens()
    for token in tokens:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        boost_url = f"https://discord.com/api/v9/invites/{server_invite}"

        response = requests.post(boost_url, headers=headers)
        if response.status_code == 200:
            print(f"[✔] Token {token[:20]}... ने बूस्ट किया!")
        else:
            print(f"[X] बूस्ट फेल {response.status_code}")

# **मेन मेनू**
def main():
    while True:
        banner()
        print(Colorate.Horizontal(Colors.green_to_blue, """
        1. Token से Server Join करें
        2. सभी Token को Online करें
        3. Bot Token से Channel बनाएं
        4. Auto Boost Server
        5. Exit
        """))
        
        choice = input("आपका चयन: ")

        if choice == "1":
            invite = input("Discord Invite लिंक दर्ज करें (discord.gg/xyz): ").split("/")[-1]
            join_server(invite)
        elif choice == "2":
            online_tokens()
        elif choice == "3":
            bot_token = input("Bot Token दर्ज करें: ")
            guild_id = input("Server ID दर्ज करें: ")
            channel_name = input("Channel Name दर्ज करें: ")
            message = input("भेजने के लिए मैसेज दर्ज करें: ")
            create_channel(bot_token, guild_id, channel_name, message)
        elif choice == "4":
            invite = input("Boost के लिए Invite Link दर्ज करें: ").split("/")[-1]
            auto_boost(invite)
        elif choice == "5":
            print("बाहर निकला...")
            break
        else:
            print("❌ गलत इनपुट! फिर से प्रयास करें!")
        time.sleep(2)

if __name__ == "__main__":
    main()
