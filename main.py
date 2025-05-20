import os
import json
import openai
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

# Add a helper to call OpenAI (new v1.x async API)
async def get_chatgpt_prompts(service, country, specificity, style_guide):
    system_prompt = f"""
    Ты — генератор промтов для фотосессий. Используй следующий стиль:
    Основные принципы: {', '.join(style_guide['style']['core_principles'])}
    Композиция: углы — {', '.join(style_guide['style']['composition']['angles'])}; свет — {', '.join(style_guide['style']['composition']['lighting'])}; детали — {', '.join(style_guide['style']['composition']['details'])}
    Форматы: крупный план — {style_guide['style']['formats']['close_up']}; средний — {style_guide['style']['formats']['medium']}; широкий — {style_guide['style']['formats']['wide']}
    """
    user_prompt = f"Сгенерируй 5 промтов для сервиса '{service}' в стране '{country}'" + (f" со спецификой: {specificity}" if specificity else "") + ". Каждый промт — отдельной строкой."
    client = openai.AsyncOpenAI()
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500,
        n=1,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

# Update generate_prompts to use ChatGPT
async def generate_prompts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = context.user_data['service']
    country = context.user_data['country']
    specificity = context.user_data.get('specificity')
    # Get prompts from ChatGPT
    prompts = await get_chatgpt_prompts(service, country, specificity, STYLE_GUIDE)
    response = "Вот 5 промтов:\n" + prompts
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
