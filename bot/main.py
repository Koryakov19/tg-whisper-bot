import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
from transcriber.whisper_runner import transcribe
from pydub import AudioSegment

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот, отправь мне голосовое или аудио.")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.voice.file_id)
    ogg_path = f"audio/raw/{update.message.message_id}.ogg"
    wav_path = ogg_path.replace(".ogg", ".wav")

    await file.download_to_drive(ogg_path)
    await update.message.reply_text(f"Сохранил голосовое как {ogg_path}")

    # Преобразуем в WAV
    audio = AudioSegment.from_file(ogg_path)
    audio.export(wav_path, format="wav")

    text = transcribe(wav_path)
    await update.message.reply_text(f"📝 Расшифровка:\n{text}")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.audio.file_id)
    mp3_path = f"audio/raw/{update.message.message_id}.mp3"
    wav_path = mp3_path.replace(".mp3", ".wav")

    await file.download_to_drive(mp3_path)
    await update.message.reply_text(f"Сохранил аудио как {mp3_path}")

    # Преобразуем в WAV
    audio = AudioSegment.from_file(mp3_path)
    audio.export(wav_path, format="wav")

    text = transcribe(wav_path)
    await update.message.reply_text(f"📝 Расшифровка:\n{text}")

def main():
    print("✅ Бот запускается...")
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("❌ BOT_TOKEN не найден в .env")
        return

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.AUDIO | filters.Document.AUDIO, handle_audio))

    print("🤖 Бот работает. Нажми Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()
