import os
import json
import openai
import asyncio
import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import PyPDF2
from telegram.ext import CallbackQueryHandler

# Define states explicitly for clarity and order
SELECT_COUNTRY = 0
SELECT_SERVICE = 1
ENTER_SPECIFICITY = 2
ASK_SPECIFICITY = 3

# Load style guide from Markdown
with open("guide.md", "r", encoding="utf-8") as f:
    STYLE_GUIDE_MD = f.read()

services = ["Ride-hailing", "Other"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    countries = [
        ("🇦🇴 AGO", "Angola"),
        ("🇦🇿 AZE", "Azerbaijan"),
        ("🇧🇴 BOL", "Bolivia"),
        ("🇨🇲 CMR", "Cameroon"),
        ("🇨🇴 COL", "Colombia"),
        ("🇨🇮 CIV", "Côte d'Ivoire"),
        ("🇪🇹 ETH", "Ethiopia"),
        ("🇬🇭 GHA", "Ghana"),
        ("🇬🇹 GTM", "Guatemala"),
        ("🇲🇦 MAR", "Morocco"),
        ("🇲🇿 MOZ", "Mozambique"),
        ("🇳🇦 NAM", "Namibia"),
        ("🇳🇵 NPL", "Nepal"),
        ("🇴🇲 OMN", "Oman"),
        ("🇵🇰 PAK", "Pakistan"),
        ("🇵🇪 PER", "Peru"),
        ("🇨🇩 COD", "Democratic Republic of the Congo"),
        ("🇸🇳 SEN", "Senegal"),
        ("🇹🇷 TUR", "Türkiye"),
        ("🇦🇪 UAE", "United Arab Emirates"),
        ("🇿🇲 ZMB", "Zambia")
    ]
    keyboard = []
    row = []
    for emoji_text, data in countries:
        button_text = emoji_text # Use the full emoji and country name
        button = InlineKeyboardButton(button_text, callback_data=data)
        row.append(button)
        if len(row) == 6:
            keyboard.append(row)
            row = []
    # Add any remaining buttons in the last row
    if row:
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("For which country should the prompts be generated?", reply_markup=reply_markup)
    return SELECT_COUNTRY

async def select_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['country'] = query.data
    reply_markup = ReplyKeyboardMarkup([[s] for s in services], one_time_keyboard=True, resize_keyboard=True)
    await query.message.reply_text("Choose a service:", reply_markup=reply_markup)
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
       <role>You are a prompt generator for Google Imagen 4. Always write prompts in English.</role>

<goal>Create high-quality visual prompts in the Super App style, blending documentary realism with urban fashion.</goal>

<input_parameters>
Scene: {scenario}  
Country: {country}
</input_parameters>

<style_guidelines>
  <aesthetic>Documentary realism × urban fashion</aesthetic>
  
  <characters>
    Confident, modern couriers, customers, or drivers — captured mid-action, never posed
  </characters>
  
  <framing>
    Dynamic, unbalanced shots — Dutch tilt, low-angle, off-center crops
  </framing>
  
  <locations>
    Hyperlocal urban settings captured from the side — shops with faded signs, tangled overhead wires, weathered brick walls, sun-washed concrete, chipped paint, and raw street textures with signs of everyday life
  </locations>
  
  <clothing_rules>
    <style>Street fashion — layered, textured, bold accessories (nails for women, rings, headwear)</style>
    <requirements>Clothing must be print-free and free from all traditional/ethnic patterns. Mix sporty and designer global brands.</requirements>
    <forbidden>Traditional African garb, ceremonial or folkloric attire, native/national dress</forbidden>
  </clothing_rules>
  
  <lighting>
    Natural or flash light with visible reflections, shadows, haze, wind, and skin detail
  </lighting>
  
  <naming_rule>
    Do not use the word "taxi"; instead use a specific car model with year (e.g., "Toyota Camry 2022")
  </naming_rule>
</style_guidelines>

<writing_style>
Use descriptive, artistic English. Avoid repetition. Visualize the scene as vividly as possible.
</writing_style>

<output_format>
You must ALWAYS follow this exact output format:

<main_character>Main character and action: [1–2 sentences]</main_character>
<clothing>Clothing/appearance: [2–3 sentences]</clothing>  
<location>Location and surroundings: [2–3 sentences]</location>
<atmosphere>Time and atmosphere: [1–2 sentences]</atmosphere>
<background>Background elements: [1–2 sentences]</background>
<photography>Photography style and angle: [1 sentence]</photography>
</output_format>

<quality_checks>
- Ensure character shows clear nationality specification
- Verify clothing avoids all traditional/ethnic patterns
- Confirm single, precise action (not multiple actions)
- Check location shows urban texture and side-view perspective
- Validate natural lighting without cinematic descriptions
- Ensure background includes other people/activity
</quality_checks>
"""
    else:
        # Default prompt for 'Other' or unspecified services
        system_prompt = f"""
        <role>You are a prompt generator for Google Imagen 4. Always write the general prompt in English.</role>

<primary_task>
Create high-quality visual prompts for image generation in the Super App style, which combines documentary realism.
</primary_task>

<input_variables>
Scenario: {scenario}
Location: {country}
</input_variables>

<reference_guidelines>
Use the 'Super App Visual Guidelines' for all creative decisions.
</reference_guidelines>

<style_principles>
  <aesthetic>Documentary realism × urban fashion</aesthetic>
  
  <characters>
    Confident modern people — couriers, customers, drivers — captured mid-action, never posed
  </characters>
  
  <framing>
    Unbalanced, dynamic angles — Dutch tilt, low-angle, off-center crops
  </framing>
  
  <locations>
    <outdoor>Hyperlocal urban settings</outdoor>
    <indoor>Use only 'Interiors' guidelines if the action takes place indoors</indoor>
  </locations>
  
  <clothing_rules>
    <style>Street fashion — layered, textured, with bold accessories (nails for women, rings, headwear)</style>
    <strict_requirement>Never use local or traditional patterns in clothing</strict_requirement>
    <fabric_rules>Clothing should be without prints — a mix of sporty and designer global brands</fabric_rules>
    <absolute_prohibition>NO USE traditional patterns completely</absolute_prohibition>
    <forbidden_items>
      Traditional African garb, ceremonial African clothing, ethnic dress, folkloric attire, 
      native costume, national dress
    </forbidden_items>
  </clothing_rules>
  
  <lighting>
    Natural or flash light, visible reflections, shadows, haze, wind, skin detail
  </lighting>
</style_principles>

<mandatory_output_format>
You must ALWAYS follow this exact structure:

<main_character>Main character and action: [1–2 sentences]</main_character>
<clothing>Clothing/appearance: [2–3 sentences]</clothing>
<location>Location and surroundings: [2–3 sentences]</location>
<atmosphere>Time and atmosphere: [1–2 sentences]</atmosphere>
<background>Background elements: [1–2 sentences]</background>
<photography>Photography style and angle: [1 sentences]</photography>
</mandatory_output_format>

<quality_control>
Before generating, verify:
- Character nationality is specified
- Single action only (no multiple simultaneous actions)
- No traditional/ethnic clothing patterns anywhere
- Urban setting appropriate for scenario
- Natural lighting without cinematic clichés
- Background activity and street life included
- Appropriate accessories for character gender
</quality_control> 

"""

    messages = [
        {"role": "system", "content": STYLE_GUIDE_MD},
        {"role": "system", "content": system_prompt},
    ]

    # For Ride-hailing and Other services, the user's input is the scenario
    if service and service.lower() in ["ride-hailing", "other"]:
        messages.append({"role": "user", "content": scenario})
    else:
         # Keep original behavior for other services if any are added later
         messages.append({"role": "user", "content": "Generate prompts using the provided style guide and rules."})

    # Generate the prompt using ChatGPT
    client = openai.AsyncOpenAI(timeout=120)
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1",
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

    # Store the conversation history and the generated prompt for services that allow editing
    if service and service.lower() in ["ride-hailing", "other"] and prompts:
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
    # Restart the conversation by going back to the country selection
    await query.message.reply_text("Okay, let's start over. For which country should the prompts be generated?")
    # Also send the inline keyboard for country selection again
    countries = [
        ("🇦🇴 AGO", "Angola"),
        ("🇦🇿 AZE", "Azerbaijan"),
        ("🇧🇴 BOL", "Bolivia"),
        ("🇨🇲 CMR", "Cameroon"),
        ("🇨🇴 COL", "Colombia"),
        ("🇨🇮 CIV", "Côte d'Ivoire"),
        ("🇪🇹 ETH", "Ethiopia"),
        ("🇬🇭 GHA", "Ghana"),
        ("🇬🇹 GTM", "Guatemala"),
        ("🇲🇦 MAR", "Morocco"),
        ("🇲🇿 MOZ", "Mozambique"),
        ("🇳🇦 NAM", "Namibia"),
        ("🇳🇵 NPL", "Nepal"),
        ("🇴🇲 OMN", "Oman"),
        ("🇵🇰 PAK", "Pakistan"),
        ("🇵🇪 PER", "Peru"),
        ("🇨🇩 COD", "Democratic Republic of the Congo"),
        ("🇸🇳 SEN", "Senegal"),
        ("🇹🇷 TUR", "Türkiye"),
        ("🇦🇪 UAE", "United Arab Emirates"),
        ("🇿🇲 ZMB", "Zambia")
    ]
    keyboard = []
    row = []
    for emoji_text, data in countries:
        button_text = emoji_text # Use the full emoji and country name
        button = InlineKeyboardButton(button_text, callback_data=data)
        row.append(button)
        if len(row) == 6:
            keyboard.append(row)
            row = []
    # Add any remaining buttons in the last row
    if row:
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Please select a country:", reply_markup=reply_markup)

    return SELECT_COUNTRY # Stay in this state waiting for a country selection

async def continue_chat_gpt_dialogue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This function will handle the user's text input when they are in the editing dialogue
    user_input = update.message.text

    # Retrieve stored messages and the last generated prompt
    messages = context.user_data.get('chat_gpt_messages', [])
    last_prompt = context.user_data.get('current_prompt')

    if not messages or not last_prompt:
        await update.message.reply_text("Error: Could not find previous prompt or conversation history.")
        return ConversationHandler.END # Exit conversation or handle appropriately

    # Create a new messages list for the API call, focusing on the editing task
    editing_messages = [
        {
            "role": "system",
            "content": f"""
    <role>You are an AI prompt editor</role>
    
    <primary_task>
      Take the user's instruction and modify the provided prompt based on their specific request
    </primary_task>
    
    <output_requirement>
      Only output the revised prompt - no additional commentary or explanation
    </output_requirement>
    
    <mandatory_format>
      You must ALWAYS follow this exact output structure:
      
      <main_character>Main character and action: [1-2 sentences]</main_character>
      <clothing>Clothing/appearance: [2-3 sentences]</clothing>
      <location>Location and surroundings: [2-3 sentences]</location>
      <atmosphere>Time and atmosphere: [1-2 sentences]</atmosphere>
      <background>Background elements: [1-2 sentences]</background>
      <photography>Photography style and angle: [1 sentence]</photography>
    </mandatory_format>
    
    <editing_guidelines>
      <preserve_structure>Maintain the six-part format structure</preserve_structure>
      <respect_constraints>Keep all Super App style guidelines intact unless specifically asked to modify them</respect_constraints>
      <focus_changes>Only modify elements directly addressed in the user's editing instruction</focus_changes>
      <maintain_quality>Ensure revised prompt maintains visual coherence and prompt effectiveness</maintain_quality>
    </editing_guidelines>
            """,
        },
        {
            "role": "user",
            "content": f"""
    <previous_prompt>{last_prompt}</previous_prompt>
    
    <editing_instruction>{user_input}</editing_instruction>
    
    <task>Generate Revised Prompt</task>
    
    <output_format_reminder>
      Must follow exact format:
      Main character and action: [1-2 sentences]  
      Clothing/appearance: [2-3 sentences]  
      Location and surroundings: [2-3 sentences]  
      Time and atmosphere: [1-2 sentences]  
      Background elements: [1-2 sentences]  
      Photography style and angle: [1 sentences]
    </output_format_reminder>
            """,
        },
    ]

    # Optionally, you could include more of the history if needed, but focusing on the last prompt might be better for specific edits.
    # editing_messages = messages + [{"role": "user", "content": user_input}]

    await update.message.reply_text("Generating refined prompt, please wait...")

    # Make new API call with updated messages
    client = openai.AsyncOpenAI(timeout=120)
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1", # Or a more suitable model if needed
            messages=editing_messages
        )
        

        refined_prompt = response.choices[0].message.content

        if refined_prompt:
            # Append the user's input and the AI's response to the main conversation history
            messages.append({"role": "user", "content": user_input})
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
            SELECT_COUNTRY: [CallbackQueryHandler(select_country)],
            SELECT_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_service)],
            ENTER_SPECIFICITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_specificity)],
            ASK_SPECIFICITY: [
                CallbackQueryHandler(handle_edit, pattern='^edit_prompt$'),
                CallbackQueryHandler(handle_new_prompt, pattern='^create_new_prompt$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, continue_chat_gpt_dialogue),
            ],
        },
        fallbacks=[
            CommandHandler("start", start), # Allow /start at any point to restart
            # Add other fallbacks if necessary
        ]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
