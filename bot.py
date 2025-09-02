import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 🔑 Твой токен
TOKEN = "8259877162:AAHQmYUve6jS4ipGZa6HxYFr9cqxFgVD3Os"

# Загружаем конфиг
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

CITIES = config["cities"]
PRODUCTS = config["products"]
PAYMENT_DETAILS = config["payment_details"]
OPERATOR_CONTACT = config["operator_contact"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(city, callback_data=f"city:{city}")] for city in CITIES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите город:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("city:"):
        city = query.data.split(":")[1]
        keyboard = [[InlineKeyboardButton(product, callback_data=f"product:{product}")] for product in PRODUCTS]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"🏙 Вы выбрали город: {city}\nТеперь выберите товар:", reply_markup=reply_markup)

    elif query.data.startswith("product:"):
        product = query.data.split(":")[1]
        text = (
            f"✅ Вы выбрали: {product}\n\n"
            f"💳 Реквизиты для оплаты:\n{PAYMENT_DETAILS}\n\n"
            f"📞 Контакт оператора: {OPERATOR_CONTACT}"
        )
        await query.edit_message_text(text=text)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
