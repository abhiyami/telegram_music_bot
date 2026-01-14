import os
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call = PyTgCalls(app)

ydl_opts = {"format": "bestaudio"}

@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("❌ Song ka naam do")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        url = info["entries"][0]["url"]
        title = info["entries"][0]["title"]

    await call.join_group_call(
        message.chat.id,
        AudioPiped(url)
    )
    await message.reply(f"🎶 Playing: {title}")

@app.on_message(filters.command("pause") & filters.group)
async def pause(_, message):
    await call.pause_stream(message.chat.id)
    await message.reply("⏸ Paused")

@app.on_message(filters.command("resume") & filters.group)
async def resume(_, message):
    await call.resume_stream(message.chat.id)
    await message.reply("▶️ Resumed")

@app.on_message(filters.command("skip") & filters.group)
async def skip(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("⏭ Skipped")

app.start()
call.start()
idle()
