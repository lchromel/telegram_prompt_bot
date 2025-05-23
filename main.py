import os
import json
import openai
import asyncio
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# States
SELECT_SERVICE, SELECT_COUNTRY, ASK_SPECIFICITY, ENTER_SPECIFICITY = range(4)

# Load style guide from Markdown
with open("guide.md", "r", encoding="utf-8") as f:
    STYLE_GUIDE_MD = f.read()

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
        await update.message.reply_text("Please describe the scenario (e.g., 'trip to the airport' or 'only about burgers')")
        return ENTER_SPECIFICITY
    context.user_data['specificity'] = None
    return await generate_prompts(update, context)

async def enter_specificity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['specificity'] = update.message.text
    return await generate_prompts(update, context)

# Update the system prompt to use the Markdown style guide
async def get_chatgpt_prompts(service, country, specificity, style_guide_md):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    system_prompt = f"""
You are a prompt generator for midjourney or google imagine 3/4. Always generate prompts in English.
Use the following style guide and instructions (in Markdown):

{style_guide_md}

Always consider the target country and scenario when generating prompts.
"""
    user_prompt = f"Generate 5 creative, detailed midjourney prompts for the '{service}' service in {country}." + (f" Scenario: {specificity}." if specificity else "") + " Each prompt should be on a new line."
    client = openai.AsyncOpenAI(api_key=api_key)
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

async def generate_prompts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = context.user_data['service']
    country = context.user_data['country']
    specificity = context.user_data.get('specificity')
    await update.message.reply_text("Generating prompts, please wait...")
    try:
        prompts = await asyncio.wait_for(get_chatgpt_prompts(service, country, specificity, STYLE_GUIDE_MD), timeout=20)
        response = "Here are 5 prompts:\n" + prompts
    except asyncio.TimeoutError:
        response = "Sorry, generation took too long. Please try again."
    except Exception as e:
        logging.exception("Error generating prompts:")
        response = "An error occurred while generating prompts. Please try again later."
    await update.message.reply_text(response)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Conversation ended.")
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
