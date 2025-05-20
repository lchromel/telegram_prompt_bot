import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# States
SELECT_SERVICE, SELECT_COUNTRY, ASK_SPECIFICITY, ENTER_SPECIFICITY = range(4)

# Load style guide
with open("guide.json", "r", encoding="utf-8") as f:
    STYLE_GUIDE = json.load(f)

services = ["Такси", "Еда", "Доставка"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([[s] for s in services], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выбери сервис:", reply_markup=reply_markup)
    return SELECT_SERVICE

async def select_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['service'] = update.message.text
    await update.message.reply_text("Для какой страны делаем промты?")
    return SELECT_COUNTRY

async def select_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['country'] = update.message.text
    reply_markup = ReplyKeyboardMarkup([["Указать специфику"], ["Без специфики"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Хочешь ли указать специфику сценария?", reply_markup=reply_markup)
    return ASK_SPECIFICITY

async def ask_specificity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Указать специфику":
        await update.message.reply_text("Опиши, пожалуйста, специфику (например, 'поездка в аэропорт' или 'только про бургеры')")
        return ENTER_SPECIFICITY
    context.user_data['specificity'] = None
    return await generate_prompts(update, context)

async def enter_specificity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['specificity'] = update.message.text
    return await generate_prompts(update, context)

async def generate_prompts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = context.user_data['service']
    country = context.user_data['country']
    specificity = context.user_data.get('specificity')

    prompts = []
    for i in range(1, 6):
        if specificity:
            text = f"{i}. [{service}] [{country}] — сценарий: {specificity}"
        else:
            text = f"{i}. [{service}] [{country}] — универсальный промт"
        prompts.append(text)

    response = "Вот 5 промтов:\n" + "\n".join(prompts)
    await update.message.reply_text(response)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог завершён.")
    return ConversationHandler.END

def main():
    from telegram.ext import ApplicationBuilder
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_service)],
            SELECT_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_country)],
            ASK_SPECIFICITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_specificity)],
            ENTER_SPECIFICITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_specificity)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
