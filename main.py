
import os
import json
import openai
import asyncio
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import PyPDF2

# States
SELECT_SERVICE, SELECT_COUNTRY, ASK_SPECIFICITY, ENTER_SPECIFICITY = range(4)

# Load style guide from PDF
with open("guide.pdf", "rb") as f:
    pdf_reader = PyPDF2.PdfReader(f)
    STYLE_GUIDE_PDF = ""
    for page in pdf_reader.pages:
        STYLE_GUIDE_PDF += page.extract_text()

services = ["Taxi", "Food", "Delivery"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([[s] for s in services], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Choose a service:", reply_markup=reply_markup)
    return SELECT_SERVICE

async def select_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['service'] = update.message.text
    await update.message.reply_text("For which country should the prompts be generated?")
    return SELECT_COUNTRY

async def select_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['country'] = update.message.text
    reply_markup = ReplyKeyboardMarkup([["Specify scenario"], ["No specifics"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Would you like to specify a scenario?", reply_markup=reply_markup)
    return ASK_SPECIFICITY

async def ask_specificity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Specify scenario":
        await update.message.reply_text("Please describe the specific scenario.")
        return ENTER_SPECIFICITY
    else:
        return await generate_prompts(update, context)

async def enter_specificity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['specificity'] = update.message.text
    return await generate_prompts(update, context)

async def generate_prompts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = context.user_data.get("service")
    country = context.user_data.get("country")
    scenario = context.user_data.get("specificity", "")

    system_prompt = f"""
You are a Midjourney/Google Imagine prompt generator. Use the style described below:
{STYLE_GUIDE_PDF}

Always follow these rules:
1. Describe the main character with stylish, localized clothing and strong accessories.
2. Focus on real, hyperlocal streets or interiors — never generic.
3. Use detailed actions, fashion attitude, confident or emotionally grounded energy.
4. Vary camera angles: low, high, tilted, cropped, through glass.
5. Use real lighting: flash, sunlight, haze. Avoid filters or artificial softness.

Generate 5 unique English prompts for the {service} service in {country}.
{"The scene should involve: " + scenario if scenario else ""}
Each prompt must include:
- A vivid, well-styled character
- An action that fits the scene
- A specific urban or interior environment
- Realistic lighting and visual mood
- Variations in framing or composition
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Generate prompts."}
        ]
    )

    prompts = response["choices"][0]["message"]["content"]
    await update.message.reply_text(prompts)
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_service)],
            SELECT_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_country)],
            ASK_SPECIFICITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_specificity)],
            ENTER_SPECIFICITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_specificity)],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
