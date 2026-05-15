import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==================== НАСТРОЙКИ ====================
TOKEN = "8219793147:AAEyRYKOXXAmHpiAj3RK7tWM-CFYkDTbITM"
ADMIN_USERNAME = "@zvqni"
WEBAPP_URL = "https://ak1nomiaa-a11y.github.io/uc-shopp/"

CARD_NUMBER = "2200 7020 3568 7222"
PHONE_NUMBER = "+79637013160"

PRODUCTS = [
    (60, 110), (120, 220), (180, 330), (325, 460), (385, 570),
    (660, 900), (720, 1010), (985, 1360), (1800, 2155),
    (3850, 4200), (8100, 8060)
]

# ==================== ЛОГИ ====================
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# ==================== КЛАВИАТУРЫ ====================
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛒 Открыть магазин", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("📦 Каталог", callback_data="catalog")],
        [InlineKeyboardButton("🆘 Поддержка", callback_data="support")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_catalog_keyboard():
    buttons = [[InlineKeyboardButton(f"💰 {uc} UC - {price}₽", callback_data=f"buy_{uc}")] for uc, price in PRODUCTS]
    buttons.append([InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(buttons)

# ==================== КОМАНДЫ ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🎮 Добро пожаловать в PUBG Mobile UC Shop!\nВыберите действие:",
        reply_markup=get_main_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "catalog":
        await query.edit_message_text("📋 Выбери товар:", reply_markup=get_catalog_keyboard())
    elif data == "support":
        kb = [[InlineKeyboardButton("✏️ Написать админу", url=f"https://t.me/{ADMIN_USERNAME[1:]}")],
              [InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")]]
        await query.edit_message_text(f"👨‍💻 Поддержка: {ADMIN_USERNAME}", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "back_to_main":
        await query.edit_message_text("🎮 Главное меню:", reply_markup=get_main_keyboard())
    elif data.startswith("buy_"):
        uc = int(data.split("_")[1])
        price = next((p for u, p in PRODUCTS if u == uc), None)
        if price:
            text = (f"✅ {uc} UC - {price}₽\n\n💳 Карта: {CARD_NUMBER}\n📱 СБП: {PHONE_NUMBER}\n\n"
                    f"📌 После оплаты напиши {ADMIN_USERNAME} и пришли скриншот!")
            kb = [[InlineKeyboardButton("📩 Написать админу", url=f"https://t.me/{ADMIN_USERNAME[1:]}")],
                  [InlineKeyboardButton("◀️ Назад", callback_data="catalog")]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))

# ==================== ЗАПУСК ====================
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🚀 БОТ ЗАПУЩЕН НА RENDER!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
