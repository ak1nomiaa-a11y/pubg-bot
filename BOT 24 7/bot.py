import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==================== НАСТРОЙКИ ====================
TOKEN = "8219793147:AAEyRYKOXXAmHpiAj3RK7tWM-CFYkDTbITM"
ADMIN_ID = 8679498618
ADMIN_USERNAME = "@zvqni"
WEBAPP_URL = "https://ak1nomiaa-a11y.github.io/uc-shopp/"

# Реквизиты оплаты
CARD_NUMBER = "2200 7020 3568 7222"
PHONE_NUMBER = "+79637013160"

# Товары
PRODUCTS = [
    (60, 110), (120, 220), (180, 330), (325, 460), (385, 570),
    (660, 900), (720, 1010), (985, 1360), (1800, 2155),
    (3850, 4200), (8100, 8060)
]

# ==================== ЛОГИ ====================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==================== КЛАВИАТУРЫ ====================
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛒 Открыть магазин", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("📦 Каталог", callback_data="catalog")],
        [InlineKeyboardButton("🆘 Поддержка", callback_data="support")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_catalog_keyboard():
    buttons = []
    for uc, price in PRODUCTS:
        buttons.append([InlineKeyboardButton(f"💰 {uc} UC - {price}₽", callback_data=f"buy_{uc}")])
    buttons.append([InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(buttons)

# ==================== КОМАНДЫ ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🎮 Привет, {user.first_name}!\n\n"
        f"Добро пожаловать в магазин PUBG Mobile UC!\n"
        f"💰 Безопасно | ⚡ Моментально | 👨‍💻 24/7\n\n"
        f"Выберите действие:",
        reply_markup=get_main_keyboard()
    )

async def catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📦 *Наши товары:*\n\n"
    for uc, price in PRODUCTS:
        text += f"💎 {uc} UC — {price} ₽\n"
    text += f"\n💳 Купить: `/buy <uc>`\nПример: `/buy 325`"
    await update.message.reply_text(text, parse_mode="Markdown")

async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Используй: `/buy 325`", parse_mode="Markdown")
        return
    
    try:
        uc = int(context.args[0])
        price = next((p for u, p in PRODUCTS if u == uc), None)
        if not price:
            await update.message.reply_text("❌ Товар не найден")
            return
        
        await update.message.reply_text(
            f"✅ *{uc} UC* — {price} ₽\n\n"
            f"💳 Карта: `{CARD_NUMBER}`\n"
            f"📱 СБП: `{PHONE_NUMBER}`\n\n"
            f"📌 После оплаты напиши {ADMIN_USERNAME} и пришли скриншот чека!",
            parse_mode="Markdown"
        )
    except ValueError:
        await update.message.reply_text("❌ Введи число")

async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👨‍💻 Поддержка: {ADMIN_USERNAME}\n"
        f"📩 Отвечаем 24/7!"
    )

# ==================== КНОПКИ ====================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "catalog":
        await query.edit_message_text(
            "📋 *Выбери товар:*",
            reply_markup=get_catalog_keyboard(),
            parse_mode="Markdown"
        )
    elif data == "support":
        text = f"👨‍💻 *Поддержка*\n\n📩 {ADMIN_USERNAME}\n\nПо всем вопросам пиши!"
        kb = [[InlineKeyboardButton("✏️ Написать", url=f"https://t.me/{ADMIN_USERNAME[1:]}")],
              [InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    
    elif data == "back_to_main":
        await query.edit_message_text(
            "🎮 *Главное меню*",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    
    elif data.startswith("buy_"):
        uc = int(data.split("_")[1])
        price = next((p for u, p in PRODUCTS if u == uc), None)
        if price:
            text = (
                f"✅ *{uc} UC* — {price} ₽\n\n"
                f"💳 Карта: `{CARD_NUMBER}`\n"
                f"📱 СБП: `{PHONE_NUMBER}`\n\n"
                f"📌 *Как получить:*\n"
                f"1️⃣ Переведи {price}₽\n"
                f"2️⃣ Сделай скриншот\n"
                f"3️⃣ Напиши {ADMIN_USERNAME}\n\n"
                f"✨ UC выдадут сразу после проверки!"
            )
            kb = [[InlineKeyboardButton("📩 Написать админу", url=f"https://t.me/{ADMIN_USERNAME[1:]}")],
                  [InlineKeyboardButton("◀️ Назад", callback_data="catalog")]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# ==================== ЗАПУСК ====================
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("catalog", catalog_command))
    app.add_handler(CommandHandler("buy", buy_command))
    app.add_handler(CommandHandler("support", support_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🚀 БОТ ЗАПУЩЕН!")
    print("📱 @deyzich_shop0_bot")
    print("⚡ Нажми Ctrl+C для остановки\n")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()