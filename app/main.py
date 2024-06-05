import discord
from discord.ext import commands
import os
import asyncio

# Import the text-to-speech library
#from gtts import gTTS
#import subprocess

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
voice_channel = None
text_channel = None


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def join(ctx):
    global voice_channel, text_channel
    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel
        text_channel = ctx.channel
        await voice_channel.connect()

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

##@bot.command()
##async def speak(ctx, *, text: str):
##    if ctx.voice_client:
##        # Convert text to speech
##        tts = gTTS(text=text, lang='en')
##        tts.save("text.mp3")
##
##        # Play the audio file
##        source = discord.FFmpegPCMAudio("text.mp3")
##        ctx.voice_client.play(source, after=lambda e: print(f'Finished playing: {e}'))
##
### Function to handle audio files
##@bot.command()
##async def play_audio(ctx, url: str):
##    if ctx.voice_client:
##        # Download the audio file using an external process
##        subprocess.call(['wget', '-O', 'audio.mp3', url])
##
##        # Play the audio file
##        source = discord.FFmpegPCMAudio("audio.mp3")
##        ctx.voice_client.play(source, after=lambda e: print(f'Finished playing: {e}'))





# To receive text or audio from another process, you might use websockets or another IPC method
# This example uses a simple web server with Flask for demonstration purposes
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start(DISCORD_TOKEN))

@app.post("/send_text")
async def send_text(request: TextRequest):
    global text_channel
    text = request.text
    print(text_channel.type, text_channel.id, text_channel.category)
    # SCRIVERE LE INFORMAZIONI NEL CANALE DI TESTO
    if text_channel and (isinstance(text_channel, discord.TextChannel) or isinstance(text_channel, discord.VoiceChannel)):
        await text_channel.send(text)
        return {"status": "Message sent to text channel"}
    else:
        raise HTTPException(status_code=404, detail="Text channel not found")


@app.post("/play_text")
async def play_text(request: TextRequest):
    text = request.text

    # VALUTARE SUCCESSIVAMENTE IL FUNZIONAMENTO DEL CANALE VOCALE
    #if channel and isinstance(channel, discord.VoiceChannel):
    #    await play_text(channel, text)
    #    return {"status": "Text played"}
    #else:
    #    raise HTTPException(status_code=404, detail="Channel not found or not a voice channel")
    #return 'OK'

#async def play_text(channel, text):
#    if channel.guild.voice_client is None:
#        await channel.connect()
#    # CAMBIARE gTTS CON VOSK
#    tts = gTTS(text=text, lang='en')
#    tts.save("text.mp3")
#    source = discord.FFmpegPCMAudio("text.mp3")
#    channel.guild.voice_client.play(source)

#async def run():
#    print("-----------------------------------" + __name__)
#    print(DISCORD_TOKEN)
#    try:
#        
#        #bot.run(DISCORD_TOKEN)
#        await bot.start(DISCORD_TOKEN)
#    except KeyboardInterrupt:
#        await bot.logout()
#
#
#asyncio.create_task(run())