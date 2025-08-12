import os
import json
import openai
import asyncio
import logging
import signal
import sys
from aiohttp import web
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from telegram.error import Conflict, NetworkError, TimedOut
import PyPDF2
from telegram.ext import CallbackQueryHandler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global variable to track if the bot is running
bot_running = False

async def generate_image_with_gpt(prompt: str) -> str:
    """
    Generate an image via OpenAI Images API (gpt-image-1) and return the URL.
    """
    client = openai.AsyncOpenAI(timeout=180)
    result = await client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )
    return result.data[0].url


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
        You are a prompt generator for Google Imagen 4.
Always the general promt in English. 
Your task is to create high-quality visual prompts for image generation in the **Super App style**, which combines documentary realism.

        Follow these style principles:
- 'Aesthetic & Principles'– Documentary realism × urban fashion  
- 'Characters' confident modern people — couriers, customers, drivers — captured mid-action, never posed  
- 'Framing & Composition' Unbalanced, dynamic angles — Dutch tilt, low-angle, off-center crops  
- 'Locations' Hyperlocal urban settings — kiosks, tangled wires, bricks walls, sun-washed, raw  
- **Use 'Clothing' Street fashion — layered, textured, with bold accessories (nails for woman, rings, headwear) **Never use local or traditional patterns in clothing**. Clothing should be without prints — a mix of sporty and designer global brands. NO USE traditional patterns completely. Awoid: traditional African garb, ceremonial African clothing, ethnic dress, folkloric attire, native costume, national dress ** 
- 'Light & Texture' — Natural or flash light, visible reflections, shadows, haze, wind, skin detail  
don't use the word taxi, change it to the name of the car with the year
Follow 'Prompt Structure' for creating the prompt:

Now generate prompt for 'Ride-Hail':
**Scene:** {scenario}  
**Country:** {country}

Follow these structure:
Main character and action
Clothing/appearance
Location and surroundings
Time and atmosphere
Background elements
Photography style and angle

"""
    else:
        # Default prompt for 'Other' or unspecified services
        system_prompt = f"""
        You are a prompt generator for Google Imagen 3.
Always the general promt in English. 
Your task is to create high-quality visual prompts for image generation in the **Super App style**, which combines documentary realism.
Create a prompt where the {scenario} takes place in {country}. **Use the 'Super App Visual Guidelines' for this.**
Follow these style principles:
- 'Aesthetic & Principles'— Documentary realism × urban fashion  
- **'Characters' confident modern people — couriers, customers, drivers — captured mid-action, never posed**  
- 'Framing & Composition' Unbalanced, dynamic angles — Dutch tilt, low-angle, off-center crops  
- 'Locations' Hyperlocal urban settings. **Use only 'Interiors' if the action takes place indoors**
- **Use 'Clothing' Street fashion — layered, textured, with bold accessories (nails for woman, rings, headwear) **Never use local or traditional patterns in clothing**. Clothing should be without prints — a mix of sporty and designer global brands. NO USE traditional patterns completely. Awoid: traditional African garb, ceremonial African clothing, ethnic dress, folkloric attire, native costume, national dress ** 
- 'Light & Texture' Natural or flash light, visible reflections, shadows, haze, wind, skin detail  

Follow these structure:
Main character and action
Clothing/appearance
Location and surroundings
Time and atmosphere
Background elements
Photography style and angle

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
            model="gpt-5",
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
        {"role": "system", "content": "You are an AI prompt editor. Take the user's instruction and modify the following prompt based on their request. Only output the revised prompt."},
        {"role": "user", "content": f"Previous Prompt: {last_prompt}\n\nEditing Instruction: {user_input}\n\nGenerate Revised Prompt:"}
    ]

    # Optionally, you could include more of the history if needed, but focusing on the last prompt might be better for specific edits.
    # editing_messages = messages + [{"role": "user", "content": user_input}]

    await update.message.reply_text("Generating refined prompt, please wait...")

    # Make new API call with updated messages
    client = openai.AsyncOpenAI(timeout=120)
    try:
        response = await client.chat.completions.create(
            model="gpt-5", # Or a more suitable model if needed
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


async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /img <prompt> — generate image with GPT-5 Image model and return a URL.
    """
    if not context.args:
        await update.message.reply_text("Usage: /img <prompt>")
        return
    prompt = " ".join(context.args)
    try:
        url = await generate_image_with_gpt(prompt)
        await update.message.reply_text(url)
    except Exception as e:
        logging.exception("Image generation failed")
        await update.message.reply_text(f"Image generation failed: {e}")

async def health_check(request):
    """Health check endpoint for Railway."""
    return web.Response(text="Bot is running!", status=200)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)
    
    # Handle specific conflict error
    if isinstance(context.error, Conflict):
        logger.error("Bot conflict detected. This usually means multiple bot instances are running.")
        # Don't restart here, let the main function handle it
    elif isinstance(context.error, (NetworkError, TimedOut)):
        logger.error("Network error occurred, will retry automatically")
    else:
        logger.error(f"Update {update} caused error {context.error}")

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global bot_running
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    bot_running = False
    sys.exit(0)

async def main():
    global bot_running
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Get bot token
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        return
    
    # Check if we should use webhook (for production environments)
    use_webhook = os.getenv("USE_WEBHOOK", "false").lower() == "true"
    port = int(os.getenv("PORT", 8080))
    
    # Build application with proper error handling
    app = ApplicationBuilder()\
        .token(token)\
        .read_timeout(120)\
        .write_timeout(120)\
        .connect_timeout(120)\
        .pool_timeout(120)\
        .build()

    # Add error handler
    app.add_error_handler(error_handler)

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
    app.add_handler(CommandHandler('img', img))
    
    # Start the bot with proper error handling
    bot_running = True
    logger.info("Starting bot...")
    
    try:
        await app.initialize()
        await app.start()
        
        if use_webhook:
            # Use webhook for production (Railway)
            webhook_url = os.getenv("WEBHOOK_URL")
            if not webhook_url:
                logger.error("WEBHOOK_URL environment variable not set for webhook mode")
                return
                
            await app.updater.start_webhook(
                listen="0.0.0.0",
                port=port,
                url_path=token,
                webhook_url=f"{webhook_url}/{token}",
                drop_pending_updates=True
            )
            logger.info(f"Bot started with webhook on port {port}")
        else:
            # Use polling for development
            await app.updater.start_polling(
                drop_pending_updates=True,  # Drop updates that arrived while the bot was offline
                allowed_updates=Update.ALL_TYPES
            )
            logger.info("Bot started with polling")
        
        logger.info("Bot started successfully")
        
        # Set up HTTP server for health checks (Railway requirement)
        if use_webhook:
            # Create aiohttp app for health checks
            http_app = web.Application()
            http_app.router.add_get('/', health_check)
            http_app.router.add_get('/health', health_check)
            
            # Start HTTP server
            runner = web.AppRunner(http_app)
            await runner.setup()
            site = web.TCPSite(runner, '0.0.0.0', port)
            await site.start()
            logger.info(f"HTTP server started on port {port}")
        
        # Keep the bot running
        while bot_running:
            await asyncio.sleep(1)
            
    except Conflict as e:
        logger.error(f"Bot conflict detected: {e}")
        logger.error("This usually means another instance of the bot is already running.")
        logger.error("Please ensure only one instance is running at a time.")
        logger.error("Consider using webhook mode in production by setting USE_WEBHOOK=true")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        logger.info("Shutting down bot...")
        try:
            if use_webhook:
                await app.updater.stop_webhook()
            else:
                await app.updater.stop()
            await app.stop()
            await app.shutdown()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
