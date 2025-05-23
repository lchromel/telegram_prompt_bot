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

# Load style guide from Markdown
with open("guide.md", "r", encoding="utf-8") as f:
    STYLE_GUIDE_MD = f.read()

services = ["Ride-hailing", "Food", "Delivery", "Other"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("For which country should the prompts be generated?")
    return SELECT_COUNTRY

async def select_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['country'] = update.message.text
    reply_markup = ReplyKeyboardMarkup([[s] for s in services], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Choose a service:", reply_markup=reply_markup)
    return SELECT_SERVICE

async def select_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['service'] = update.message.text
    await update.message.reply_text("Please describe the situation (e.g., 'trip to the airport', 'only about burgers', etc.)")
    return ENTER_SPECIFICITY

async def enter_specificity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['specificity'] = update.message.text
    return await generate_prompts(update, context)

async def generate_prompts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = context.user_data.get("service")
    country = context.user_data.get("country")
    scenario = context.user_data.get("specificity", "")

    await update.message.reply_text("Generating prompts, please wait...")

    # Custom rules based on service
    extra_rules = ""
    if service and service.lower() in ["food"]:
        extra_rules += "\n- The scene must always take place indoors, at home."
    if service and service.lower() in ["ride-hailing", "ride-hail", "taxi"]:
        extra_rules += "\n- Use only medium or wide shots."
    # Clothing and outdoor adjustments
    extra_rules += "\n- Clothing should be modern street fashion, not hyperlocal or traditional."
    extra_rules += ("\n- For outdoor scenes, focus on buildings: avoid trees, minimize visible sky, and emphasize walls, entrances, stairwells, and doorways.")

    system_prompt = f"""
You are a Midjourney/Google Imagine prompt generator. Use the style described below:
{STYLE_GUIDE_MD}

Always follow these rules:
1. Describe the main character with stylish, designed clothing and fancy accessories.
2. Focus on real, hyperlocal streets or interiors — never generic.
3. Use detailed actions, fashion attitude, confident or emotionally grounded energy.
4. Vary camera angles: low, high, tilted, cropped, through glass.
5. Use real lighting: flash, sunlight, haze. Avoid filters or artificial softness.
{extra_rules}

Generate 3 unique English prompts for the {service} service in {country} with {scenario}
Each prompt must feature a different framing scale.
Each prompt must include:
- Description of documentary style
- A vivid, street fashion character
- An action that fits the scene
- A specific urban or interior environment
- Realistic lighting and visual mood
- Variations in framing or composition

Adapt the resulting prompt for Google Imagine

"""

    client = openai.AsyncOpenAI(timeout=60)
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Generate prompts."}
        ]
    )
    prompts = response.choices[0].message.content
    await update.message.reply_text(prompts)
    return ConversationHandler.END

def main():
    app = ApplicationBuilder()\
        .token(os.getenv("TELEGRAM_BOT_TOKEN"))\
        .read_timeout(60)\
        .write_timeout(60)\
        .connect_timeout(60)\
        .pool_timeout(60)\
        .build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_country)],
            SELECT_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_service)],
            ENTER_SPECIFICITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_specificity)],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
