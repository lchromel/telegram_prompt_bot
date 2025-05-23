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
You are a creative prompt generator for image models like Midjourney or Google Imagen.
Your task is to create visually rich, editorial-style image prompts that reflect the following visual style:

Style: Fashion-documentary realism. Think editorial storytelling with real-life textures, cinematic lighting, and expressive human moments.
Tone: Real, confident, never cliché or commercial. No posing. The subject is always caught mid-action or in transition.
Visual Language: Inspired by Magnum Photos and Bottega Veneta campaigns — a mix of fashion, street grit, and layered spontaneity.

Strictly follow this structure in each prompt:
- Describe the camera angle and lens perspective (e.g., low-angle, wide shot, diagonal, through glass)
- Set the exact scene location — use hyperlocal details (e.g. faded murals, plastic chairs, tangled wires)
- Describe the person and their outfit in a stylish way (layered clothes, bold accessories, visible nails, expressive hair)
- Show a natural, moment-in-motion action — not posing. Mid-bite, adjusting, stepping out, gripping, reaching
- Add realistic light and texture (sunlight, flash, haze, reflections, sweat, wind, fabric motion)
- Use cropping, shadows, or reflections to make the shot feel dynamic and cinematic

Now generate 5 diverse prompts for a scene about {service} in {country}
{"Focus on: " + scenario if scenario else ""}
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
