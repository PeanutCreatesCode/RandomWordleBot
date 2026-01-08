import discord
from discord.ext import tasks
import random
import os
from datetime import time
from english_words import get_english_words_set

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
global current_word
# Liste von 5-Buchstaben-Wörtern (erweitere diese Liste nach Bedarf)
english_words_set = get_english_words_set(['gcide'], alpha=True)
english_words_list = list(english_words_set)
FIVE_LETTER_WORDS = []
for word in english_words_set:
    if len(word) == 5:
        FIVE_LETTER_WORDS.append(word)
# FIVE_LETTER_WORDS = [
#     "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult", "after",
#     "again", "agent", "agree", "ahead", "alarm", "album", "alert", "alike", "alive",
#     "allow", "alone", "along", "alter", "among", "anger", "angle", "angry", "apart",
#     "apple", "apply", "arena", "argue", "arise", "array", "aside", "asset", "audio",
#     "avoid", "award", "aware", "badly", "baker", "bases", "basic", "basis", "beach",
#     "began", "begin", "being", "below", "bench", "billy", "birth", "black", "blame",
#     "blind", "block", "blood", "board", "boost", "booth", "bound", "brain", "brand",
#     "bread", "break", "breed", "brief", "bring", "broad", "broke", "brown", "build",
#     "built", "buyer", "cable", "calif", "carry", "catch", "cause", "chain", "chair",
#     "chart", "chase", "cheap", "check", "chest", "chief", "child", "china", "chose",
#     "civil", "claim", "class", "clean", "clear", "click", "clock", "close", "coach",
#     "coast", "could", "count", "court", "cover", "craft", "crash", "crazy", "cream",
#     "crime", "cross", "crowd", "crown", "crude", "cycle", "daily", "dance", "dated",
#     "dealt", "death", "debut", "delay", "depth", "doing", "doubt", "dozen", "draft",
#     "drama", "drank", "drawn", "dream", "dress", "drill", "drink", "drive", "drove",
#     "dying", "eager", "early", "earth", "eight", "elite", "empty", "enemy", "enjoy",
#     "enter", "entry", "equal", "error", "event", "every", "exact", "exist", "extra",
#     "faith", "false", "fault", "fiber", "field", "fifth", "fifty", "fight", "final",
#     "first", "flash", "fleet", "floor", "fluid", "focus", "force", "forth", "forty",
#     "forum", "found", "frame", "frank", "fraud", "fresh", "front", "fruit", "fully",
#     "funny", "giant", "given", "glass", "globe", "going", "grace", "grade", "grand",
#     "grant", "grass", "great", "green", "gross", "group", "grown", "guard", "guess",
#     "guest", "guide", "happy", "harry", "heart", "heavy", "hence", "henry", "horse",
#     "hotel", "house", "human", "ideal", "image", "index", "inner", "input", "issue",
#     "japan", "jimmy", "joint", "jones", "judge", "known", "label", "large", "laser",
#     "later", "laugh", "layer", "learn", "lease", "least", "leave", "legal", "lemon",
#     "level", "lewis", "light", "limit", "links", "lives", "local", "logic", "loose",
#     "lower", "lucky", "lunch", "lying", "magic", "major", "maker", "march", "maria",
#     "match", "maybe", "mayor", "meant", "media", "metal", "might", "minor", "minus",
#     "mixed", "model", "money", "month", "moral", "motor", "mount", "mouse", "mouth",
#     "movie", "music", "needs", "never", "newly", "night", "noise", "north", "noted",
#     "novel", "nurse", "occur", "ocean", "offer", "often", "order", "other", "ought",
#     "paint", "panel", "paper", "party", "peace", "peter", "phase", "phone", "photo",
#     "piece", "pilot", "pitch", "place", "plain", "plane", "plant", "plate", "point",
#     "pound", "power", "press", "price", "pride", "prime", "print", "prior", "prize",
#     "proof", "proud", "prove", "queen", "quick", "quiet", "quite", "radio", "raise",
#     "range", "rapid", "ratio", "reach", "ready", "refer", "right", "river", "robin",
#     "roger", "roman", "rough", "round", "route", "royal", "rural", "scale", "scene",
#     "scope", "score", "sense", "serve", "seven", "shall", "shape", "share", "sharp",
#     "sheet", "shelf", "shell", "shift", "shine", "shirt", "shock", "shoot", "short",
#     "shown", "sight", "since", "sixth", "sixty", "sized", "skill", "sleep", "slide",
#     "small", "smart", "smile", "smith", "smoke", "solid", "solve", "sorry", "sound",
#     "south", "space", "spare", "speak", "speed", "spend", "spent", "split", "spoke",
#     "sport", "staff", "stage", "stake", "stand", "start", "state", "steam", "steel",
#     "stick", "still", "stock", "stone", "stood", "store", "storm", "story", "strip",
#     "stuck", "study", "stuff", "style", "sugar", "suite", "sunny", "super", "sweet",
#     "table", "taken", "taste", "taxes", "teach", "terry", "texas", "thank", "theft",
#     "their", "theme", "there", "these", "thick", "thing", "think", "third", "those",
#     "three", "threw", "throw", "tight", "times", "title", "today", "topic", "total",
#     "touch", "tough", "tower", "track", "trade", "train", "treat", "trend", "trial",
#     "tribe", "trick", "tried", "tries", "troop", "truck", "truly", "trust", "truth",
#     "twice", "under", "undue", "union", "unity", "until", "upper", "upset", "urban",
#     "usage", "usual", "valid", "value", "video", "virus", "visit", "vital", "vocal",
#     "voice", "waste", "watch", "water", "wheel", "where", "which", "while", "white",
#     "whole", "whose", "woman", "women", "world", "worry", "worse", "worst", "worth",
#     "would", "wound", "write", "wrong", "wrote", "young", "youth"
# ]

# Channel ID wo der Bot posten soll
CHANNEL_ID = None  # Wird später gesetzt

@client.event
async def on_ready():
    print(f'{client.user} ist eingeloggt!')
    if not daily_word.is_running():
        daily_word.start()

@tasks.loop(time=time(hour=22, minute=55))  # Täglich um 23:55 Berlin Time (CET)
async def daily_word():
    """Postet täglich ein zufälliges 5-Buchstaben-Wort"""
    
    
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
    if message.content.startswith('!testword') and message.author.guild_permissions.administrator:
        global current_word
        word = random.choice(FIVE_LETTER_WORDS)
        current_word = word  # Speichere auch das Testwort
        await message.channel.send(f"@here\n\n🎯 **Test-Wort**: `{word.upper()}`")

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
