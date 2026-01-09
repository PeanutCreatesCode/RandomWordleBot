import discord
from discord.ext import tasks
import random
import os
from datetime import time

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Hole alle 5-Buchstaben-Wörter aus dem english-words Paket
cwd = os.getcwd()
words_file_name = "words.txt"
words_file_path = cwd + "/" + words_file_name
FIVE_LETTER_WORDS = []
with open(words_file_path, 'r') as f:
    FIVE_LETTER_WORDS = [line for line in f]
    

print(f"Wortliste geladen: {len(FIVE_LETTER_WORDS)} Wörter mit 5 Buchstaben")

# Channel ID wo der Bot posten soll
CHANNEL_ID = None  # Wird später gesetzt

# Speichert das aktuelle Wort des Tages
current_word = None  # Hier initialisieren, NICHT mit global!

@client.event
async def on_ready():
    print(f'{client.user} ist eingeloggt!')
    print(f'Verfügbare Wörter: {len(FIVE_LETTER_WORDS)}')
    if not daily_word.is_running():
        daily_word.start()

@tasks.loop(time=time(hour=22, minute=55))  # Täglich um 22:55 UTC (23:55 CET)
async def daily_word():
    """Postet täglich ein zufälliges 5-Buchstaben-Wort"""
    global current_word  # HIER das global statement!
    
    if CHANNEL_ID is None:
        print("Fehler: CHANNEL_ID ist nicht gesetzt!")
        return
    
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        word = random.choice(FIVE_LETTER_WORDS)
        current_word = word  # Speichere das aktuelle Wort
        message = f"@here\n\n🎯 **Wort des Tages**: `{word.upper()}`"
        await channel.send(message)
        print(f"Wort gepostet: {word}")
    else:
        print(f"Channel mit ID {CHANNEL_ID} nicht gefunden!")

@client.event
async def on_message(message):
    global current_word  # HIER das global statement!
    
    # Ignoriere Nachrichten vom Bot selbst
    if message.author == client.user:
        return
    
    # Befehl: Aktuelles Wort wiederholen
    if message.content.startswith('!word'):
        if current_word:
            await message.channel.send(f"🎯 **Aktuelles Wort des Tages**: `{current_word.upper()}`")
        else:
            await message.channel.send("❌ Es wurde noch kein Wort des Tages gepostet!")
    
    # Admin-Befehl zum Testen
    if message.content.startswith('!reroll') and message.author.guild_permissions.administrator:
        word = random.choice(FIVE_LETTER_WORDS)
        current_word = word  # Speichere auch das Testwort
        await message.channel.send(f"@here\n\n🎯 **Neues Wort**: `{word.upper()}`")
    
    # Info-Befehl: Zeigt Anzahl verfügbarer Wörter
    if message.content.startswith('!wordcount'):
        await message.channel.send(f"📊 Es gibt **{len(FIVE_LETTER_WORDS)}** verfügbare 5-Buchstaben-Wörter!")

# Bot starten
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    channel_id_str = os.getenv('DISCORD_CHANNEL_ID')
    
    if not TOKEN:
        print("Fehler: DISCORD_BOT_TOKEN Umgebungsvariable nicht gefunden!")
        exit(1)
    
    if channel_id_str:
        try:
            CHANNEL_ID = int(channel_id_str)
        except ValueError:
            print("Fehler: DISCORD_CHANNEL_ID muss eine Zahl sein!")
            exit(1)
    else:
        print("Fehler: DISCORD_CHANNEL_ID Umgebungsvariable nicht gefunden!")
        exit(1)
    
    client.run(TOKEN)