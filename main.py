import os
import json
import openai
import asyncio
import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import PyPDF2
from telegram.ext import CallbackQueryHandler

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

    # Define a base scenario based on the service
    base_scenario = f"{service} in {country}"
    if service and service.lower() == "ride-hailing":
        base_scenario = f"Character using going to the car in {country}"
    elif service and service.lower() == "food":
        base_scenario = f"Character receiving a food delivery in {country}"
    elif service and service.lower() == "delivery":
        base_scenario = f"Character sending or receiving a package via delivery service in {country}"
    # Add more specific scenarios for other services if needed

    await update.message.reply_text("Generating prompts, please wait...")

    if service and service.lower() == "ride-hailing":
        system_prompt = f"""
You are a prompt generator for Google Imagen 3.

Your task is to create high-quality visual prompts for image generation in the **Super App style**, which combines documentary realism.

Follow these style principles:
- 'Aesthetic & Principles': Documentary realism × urban fashion  
- 'Characters' confident modern people — couriers, customers, drivers — captured mid-action, never posed  
- 'Framing & Composition' Unbalanced, dynamic angles — Dutch tilt, low-angle, off-center crops  
- 'Locations' Hyperlocal urban settings — kiosks, tangled wires, cracked walls  
- 'Clothing' Street fashion — layered, textured, with bold accessories (nails, rings, headwear)  
- 'Light & Texture' Natural or flash light, visible reflections, shadows, haze, wind, skin detail  

Follow 'Prompt Structure' for creating the prompts:

Now generate 3 diverse prompts for 'Ride-Hail' the following (1 paragraph each):
**Scene:** {scenario}  
**Country:** {country}

Use a new line for each prompt.
"""
    elif service and service.lower() == "food":
        system_prompt = f"""
You are a prompt writer creating vivid, documentary-style photo prompts for a food delivery service in {country}. Generate 5 distinct scenes.

Rules for each prompt:
1. Feature a specific delivery vehicle (motorbike, bicycle, car) clearly visible, either moving or parked, often near a residential or commercial building.
2. A driver/delivery person must be present and briefly visible.
3. The main character should be interacting with the delivery (receiving the food, opening the bag).
4. The setting should focus on urban residential or commercial entryways, sidewalks, doorsteps, or building exteriors.
5. Incorporate local elements specific to {country} that add texture and authenticity (e.g., door details, specific signage, nearby street life) but maintain an urban feel.
6. Describe the main character's casual streetwear style with perhaps one key accessory.
7. Use dynamic angles: low angle, medium shot, wide shot, slightly voyeuristic framing.
8. Emphasize light and mood: daytime sun, evening light from windows or streetlights, capturing the moment of exchange.

Expand the scenario below into 5 unique photo prompts (1 paragraph each).

**Scenario:** Character receiving a food delivery in {country}{f' with specificity: {scenario}' if scenario else ''}

Write only the 5 formatted results. Each must begin on a new line.
"""
    elif service and service.lower() == "delivery":
        system_prompt = f"""
You are a prompt writer creating engaging, street-style photo prompts for a package delivery service in {country}. Generate 5 distinct scenes.

Rules for each prompt:
1. Feature a specific delivery vehicle (van, motorbike, car) clearly visible, either moving or parked, often near a drop-off or pick-up point.
2. A driver/delivery person must be present and briefly visible.
3. The main character should be interacting with a package (sending it, receiving it, carrying it).
4. The setting should be urban, focusing on sidewalks, building entrances, post offices, or street corners.
5. Incorporate local elements specific to {country} that add texture and authenticity (e.g., street ads, specific building materials, relevant signage) but maintain an urban feel.
6. Describe the main character's practical yet stylish streetwear with a functional accessory like a backpack or tote bag.
7. Use dynamic angles: medium shot, wide shot, street-level view, capturing movement.
8. Emphasize light and mood: varying urban light conditions, capturing the action of delivery or collection.

Expand the scenario below into 5 unique photo prompts (1 paragraph each).

**Scenario:** Character interacting with a package delivery service in {country}{f' with specificity: {scenario}' if scenario else ''}

Write only the 5 formatted results. Each must begin on a new line.
"""
    else:
        # Default prompt for 'Other' or unspecified services
        system_prompt = f"""
Create a prompt where the {scenario} takes place in {country}. **Use the 'Super App Visual Guidelines' for this.**
Follow these style principles:
- 'Aesthetic & Principles': Documentary realism × urban fashion  
- 'Characters' confident modern people — couriers, customers, drivers — captured mid-action, never posed  
- 'Framing & Composition' Unbalanced, dynamic angles — Dutch tilt, low-angle, off-center crops  
- 'Locations' Hyperlocal urban settings
- 'Clothing' Street fashion — layered, textured, with bold accessories (nails, rings, headwear)  
- 'Light & Texture' Natural or flash light, visible reflections, shadows, haze, wind, skin detail  
"""

    messages = [
        {"role": "system", "content": STYLE_GUIDE_MD},
        {"role": "system", "content": system_prompt},
    ]

    if service and service.lower() == "other":
        # For the 'Other' service, send the user's specific scenario as the user message
        messages.append({"role": "user", "content": scenario})
    else:
        # For other services, use the generic user message (or you might want to refine this too)
        messages.append({"role": "user", "content": "Generate prompts using the provided style guide and rules."})

    # Generate the prompt using ChatGPT
    client = openai.AsyncOpenAI(timeout=120)
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        prompts = response.choices[0].message.content

        if prompts:
            await update.message.reply_text(prompts)
        else:
            await update.message.reply_text("Could not generate prompt. The API returned an empty response.")

    except Exception as e:
        logging.error(f"Error generating prompt: {e}")
        await update.message.reply_text(f"An error occurred while generating the prompt: {e}")

    # Store the conversation history and the generated prompt if service is 'Other'
    if service and service.lower() == "other" and prompts:
        context.user_data['chat_gpt_messages'] = messages
        context.user_data['current_prompt'] = prompts

    # After generating the prompt, ask the user if they want to edit or create a new one
    keyboard = [[InlineKeyboardButton("Edit", callback_data='edit_prompt'),
                 InlineKeyboardButton("Create New", callback_data='create_new_prompt')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Would you like to edit this prompt or create a new one?", reply_markup=reply_markup)

    return ASK_SPECIFICITY

async def handle_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("What would you like to change?")
    return ASK_SPECIFICITY # Stay in this state to continue the dialogue

async def handle_new_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.message.reply_text("Describe the scenario.")
    return ENTER_SPECIFICITY # Go back to collect the new scenario

async def continue_chat_gpt_dialogue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This function will handle the user's text input when they are in the editing dialogue
    user_input = update.message.text

    # Retrieve stored messages
    messages = context.user_data.get('chat_gpt_messages')
    if not messages:
        await update.message.reply_text("Error: Could not find conversation history.")
        return ConversationHandler.END # Exit conversation or handle appropriately

    # Append user's edit to messages
    messages.append({"role": "user", "content": user_input})

    await update.message.reply_text("Generating refined prompt, please wait...")

    # Make new API call with updated messages
    client = openai.AsyncOpenAI(timeout=120)
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        refined_prompt = response.choices[0].message.content

        if refined_prompt:
            # Append AI response to messages and update stored history/prompt
            messages.append({"role": "assistant", "content": refined_prompt})
            context.user_data['chat_gpt_messages'] = messages
            context.user_data['current_prompt'] = refined_prompt

            await update.message.reply_text(refined_prompt)

            # After sending the refined prompt, show the edit/create new buttons again
            keyboard = [[InlineKeyboardButton("Edit", callback_data='edit_prompt'),
                         InlineKeyboardButton("Create New", callback_data='create_new_prompt')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Would you like to edit this prompt or create a new one?", reply_markup=reply_markup)

        else:
            await update.message.reply_text("Could not refine prompt. The API returned an empty response.")

    except Exception as e:
        logging.error(f"Error refining prompt: {e}")
        await update.message.reply_text(f"An error occurred while refining the prompt: {e}")

    return ASK_SPECIFICITY # Stay in this state

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
            ASK_SPECIFICITY: [
                CallbackQueryHandler(handle_edit, pattern='^edit_prompt$'),
                CallbackQueryHandler(handle_new_prompt, pattern='^create_new_prompt$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, continue_chat_gpt_dialogue),
            ],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
