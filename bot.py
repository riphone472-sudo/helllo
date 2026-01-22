from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont
import random
import io
import math

bot=TOKEN = "8001601776:AAEdp0gsAl_mjSlZs5yWEvoyFIgFUGo5-fM"

users = {}

def generate_code_image(code: str):
    width, height = 600, 300
    bg_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()

    digit_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    x = 50
    for ch in code:
        angle = random.randint(-45, 45)
        char_img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        font_size_variation = random.randint(70, 90)
        try:
            font_var = ImageFont.truetype("arial.ttf", font_size_variation)
        except:
            font_var = font
        char_draw.text((10, 0), ch, font=font_var, fill=digit_color)
        rotated = char_img.rotate(angle, expand=1)
        img.paste(rotated, (x, random.randint(50, 130)), rotated)
        x += random.randint(80, 100)

    for _ in range(25):
        draw.line(
            (
                random.randint(0, width),
                random.randint(0, height),
                random.randint(0, width),
                random.randint(0, height)
            ),
            fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            width=random.randint(1, 3)
        )

    for _ in range(300):
        draw.point(
            (random.randint(0, width), random.randint(0, height)),
            fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )

    bio = io.BytesIO()
    bio.name = "captcha.png"
    img.save(bio, "PNG")
    bio.seek(0)
    return bio

def get_buttons():
    keyboard = [
        [InlineKeyboardButton("⚜️ОПЕРАТОР ТАШКЕНТ⚜️", url="https://t.me/tw")],
        [InlineKeyboardButton("⚜️ТЕХ Поддержка⚜️", url="https://t.me/evcn")],
        [InlineKeyboardButton("🔱ОПЕРАТОР ПРИГОРОД🔱", url="https://t.me/yzc")],
        [InlineKeyboardButton("🔱ТЕХ Поддержка ПРИГОРОД🔱", url="https://t.me/yzb")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    name = user.first_name or "User"

    code = str(random.randint(10000, 99999))
    users[user_id] = {"verified": False, "code": code, "name": name}

    image = generate_code_image(code)

    message_text = f"Привет, {name}. Пожалуйста, решите капчу с цифрами на этом изображении, чтобы убедиться, что вы человек."

    await update.message.reply_photo(photo=image, caption=message_text)

async def check_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        return

    name = users[user_id]["name"]

    if update.message.text == users[user_id]["code"]:
        users[user_id]["verified"] = True
        message_text = "⚡️Вас приветствует Tesla Shop⚡️\nЕсли вам нужна помощь с покупкой, пожалуйста, свяжитесь с оператором."
        await update.message.reply_text(message_text, reply_markup=get_buttons())
    else:
        new_code = str(random.randint(10000, 99999))
        users[user_id]["code"] = new_code
        image = generate_code_image(new_code)
        message_text = f"Привет, {name}. Пожалуйста, решите капчу с цифрами на этом изображении, чтобы убедиться, что вы человек."
        await update.message.reply_photo(photo=image, caption=message_text)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_code))
    app.run_polling()

if __name__ == "__main__":
    main()
