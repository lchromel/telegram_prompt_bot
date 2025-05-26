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
You are a creative prompt writer working in the style of a documentary-meets-fashion campaign. Expand the following simple scene description into 5 rich, cinematic photo-like prompts.

Rules for each output:
1. The main mode of transport (e.g. tuk tuk, car, motorbike) MUST appear clearly in every prompt — either in action or parked.
2. The vehicle should always have a visible driver (briefly described, e.g. in the mirror, behind the wheel, etc).
3. Use candid, unstaged framing — no posing or looking at the camera.
4. Vary the angles: Dutch tilt, low, medium, wide, over-the-shoulder.
5. Describe the main character's clothing and appearance with layered, bold streetwear. Include at least one accessory (bag, jewelry, sunglasses, etc).
6. Include real local textures and background elements from the given country (e.g. wires, murals, crates, fruit vendors, dust, etc).
7. Convey time of day, light source, and mood — emphasize flash, dusk light, shadows, sun glare, etc.
8. The photo should feel like a "caught moment", full of energy or subtle emotion.

Expand the scene below into 5 diverse cinematic scene descriptions (1 paragraph each). Each should include vehicle + driver + character in action.  

**Short scene:** {service} 
**Country:** {country}

Write 5 results as separate paragraphs. Each must begin on a new line.
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
        .read_timeout(120)\
        .write_timeout(120)\
        .connect_timeout(120)\
        .pool_timeout(120)\
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
