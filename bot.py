from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)
from PIL import Image, ImageDraw, ImageFont
import random
import os

TOKEN = "8001601776:AAEdp0gsAl_mjSlZs5yWEvoyFIgFUGo5-fM"

# foydalanuvchi kodlarini saqlash
user_codes = {}

def generate_captcha(user_id):
    code = str(random.randint(10000, 99999))
    user_codes[user_id] = code

    img = Image.new("RGB", (250, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    draw.text((40, 20), code, font=font, fill=(0, 0, 0))

    filename = f"captcha_{user_id}.png"
    img.save(filename)

    return filename, code

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.first_name

    file, code = generate_captcha(user_id)

    update.message.reply_photo(
        photo=open(file, "rb"),
        caption=f"Salom {username} 👋\n\nKodini kiriting:"
    )

    os.remove(file)

def check_code(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_codes:
        update.message.reply_text("Iltimos /start bosing")
        return

    if text == user_codes[user_id]:
        keyboard = ReplyKeyboardMarkup(
            [["1", "2", "3", "4"]],
            resize_keyboard=True
        )
        update.message.reply_text(
            "✅ To‘g‘ri!\n\nTugmalarni tanlang:",
            reply_markup=keyboard
        )
        del user_codes[user_id]
    else:
        update.message.reply_text("❌ Noto‘g‘ri kod. Qayta urinib ko‘ring.")
        file, _ = generate_captcha(user_id)
        update.message.reply_photo(
            photo=open(file, "rb"),
            caption="Yangi kodni kiriting:"
        )
        os.remove(file)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_code))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
