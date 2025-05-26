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
You are a creative prompt writer working in the style of a documentary-meets-fashion campaign. Expand the following simple scene description into a rich, cinematic, photo-like visual prompt. Follow these rules:

1. Use candid, unstaged framing. No posing or smiling at the camera.
2. Choose dynamic angles (Dutch tilt, low-angle, medium, wide).
3. Describe the main character’s outfit in detail — urban eclectic streetwear with layers and bold accessories.
4. Mention specific background elements typical for the chosen country (e.g. Colombia: mango carts, street murals, moto taxis, posters).
5. Convey atmosphere: time of day, light (e.g. flash, golden hour), mood, energy.
6. Mention motion or interaction (e.g. stepping out, adjusting a strap, mid-motion).
7. Include at least 1–2 local details or cultural textures.

Now expand the following short scene into a full cinematic photo prompt using this structure.

**Short scene:** {service} 
**Country:** {country}

Write 5 diverse result as a single paragraph. Make it sound like a scene description for a movie still or a Magnum/Bottega-style photograph.
Use a new line for each prompt.
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
