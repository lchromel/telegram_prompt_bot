import os
import openai
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from telegram.ext import CallbackQueryHandler

# Define states explicitly for clarity and order
SELECT_COUNTRY = 0
ENTER_SPECIFICITY = 1
ASK_SPECIFICITY = 2

# Load style guide from Markdown
with open("guide.md", "r", encoding="utf-8") as f:
    STYLE_GUIDE_MD = f.read()

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
    await query.message.reply_text("Please describe the situation (e.g., 'trip to the airport', 'only about burgers', etc.)")
    return ENTER_SPECIFICITY

async def enter_specificity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['specificity'] = update.message.text
    return await generate_prompts(update, context)

async def generate_prompts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country = context.user_data.get("country")
    scenario = context.user_data.get("specificity", "")

    await update.message.reply_text("Generating prompts, please wait...")

    # Always use Ridhale's script (ride-hailing prompt)
    system_prompt = f"""
       You are a prompt generator for Nano Banana Pro.
Always write prompts in English.
Follow the Super App Visual Guide strictly.

GOAL:
Create a clean, fashion-forward visual prompt in Super App style:
documentary realism blended with bold urban street fashion.

INPUT:
Scene: {scenario}
Country: {country}

GENERAL RULES:
- One or two main characters only
- Clear, scenario-driven action
- Fashion is visually dominant
- Environment supports, never overwhelms

CHARACTERS:
- Explicitly specify nationality for each character
- Confident, modern people captured mid-action
- No posing, no eye contact with the camera
- If two characters are present, both must be visible and interacting naturally

PHONE RULE:
- At least one character should be holding or using a phone when appropriate
- Phone interaction must support the scenario

STYLE:
- Street fashion must be bold and expressive
- Use strong color contrast, unexpected layering, or one standout accessory
- Avoid safe or minimal looks

SEASON & TIME LOGIC:
- Clothing must match the current season and climate
- Time of day must logically follow the scenario

CLOTHING RESTRICTIONS:
- No traditional, ethnic, folkloric, or ceremonial clothing
- No ethnic patterns or prints
- Global street fashion only
- Accessories must be intentional and limited
- Women may have bold manicures
- Men must have natural, unstyled nails only

LOCATION RULES (EXTERIOR):
- Never use the words: street, alley, road, market, sidewalk
- Describe the exterior environment through architecture only
- Always make clear the characters are outside next to a building
- Include a building surface and a transition element
- Maximum 2–3 architectural details

VEHICLE RULES:

IF THE SCENE IS INSIDE A CAR:
- Passengers are in the back seat
- Seat belt fastened (mandatory)
- Camera POV: from the driver’s seat
- Do NOT mention any logo or branding
- Driver must NOT be visible

IF THE SCENE IS OUTSIDE A CAR:
- Specify a white economy-class Yango car
- Include brand, model, and recent body year
- Always add:
  “with red Yango logotype on the door”

IF A TUK-TUK IS PRESENT:
- It must be red

IF A MOTORCYCLE IS PRESENT:
- It must be red

LIGHT & ATMOSPHERE:
- Natural or flash light only
- Used to show texture and fabric
- No cinematic or poetic time-of-day language

BACKGROUND:
- Optional
- Maximum one secondary background figure
- May be blurred or partially visible
- Never interacting with main characters

OUTPUT FORMAT (STRICT):
Main character(s) and action: 1–2 sentences  
Clothing and appearance: 2–3 sentences  
Location and surroundings: 2–3 sentences (or interior description if inside vehicle)  
Time and atmosphere: 1 sentence  
Background elements: 0–1 sentence  
Photography style and angle: 1 sentence  

FINAL CHECK:
If POV, vehicle color, branding rules, or vehicle type rules are broken — rewrite the prompt.

"""

    messages = [
        {"role": "system", "content": STYLE_GUIDE_MD},
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": scenario},
    ]

    # Generate the prompt using ChatGPT
    client = openai.AsyncOpenAI(timeout=120)
    try:
        response = await client.chat.completions.create(
            model="gpt-5-mini",
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

    # Store the conversation history and the generated prompt for editing
    if prompts:
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

    <output_instruction>
Generate ONLY the final prompt text without any HTML tags, formatting markers, or structural elements.
</output_instruction>

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
            model="gpt-5-mini", # Or a more suitable model if needed
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
