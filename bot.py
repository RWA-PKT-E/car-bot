import pandas as pd
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load Excel data
data = pd.read_excel("data.xlsx")
print("🧾 Columns found in Excel:", data.columns.tolist())
data.columns = data.columns.str.strip()  # removes leading/trailing spaces

# Search logic
def search_owner(last4):
    normalized_car_numbers = data['Car Number'].astype(str).str.replace(r"\s+", "", regex=True).str.upper()
    matches = data[normalized_car_numbers.str.contains(last4.upper())]

    if not matches.empty:
        responses = []
        for _, row in matches.iterrows():
            name = str(row['Name']).strip()
            phone = str(row['Phone']).split('.')[0].strip()  # removes ".0"
            address = str(row['Address']).split('.')[0].strip()  # removes ".0"

            response = f"🚗 Car Number: {row['Car Number']}\nOwner: {name}\nPhone: {phone}\nAddress: {address}"
            responses.append(response)
        return "\n\n".join(responses)
    else:
        return "❌ No match found containing those digits."

# Start command with a custom keyboard
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Start 🚀"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    welcome_message = (
        "🚗 *Chatbot for Vehicle Identification – RWA Pocket E, Mayur Vihar Phase 2*\n\n"
        "🔍 Send the *last 4 digits* of a Vehicle number to get the owner's info.\n\n"
        "Or press *Start* below to begin.\n\n"
        "👨‍💻 *Developed by* – Anil Rishi Raj"
    )
    
    await update.message.reply_text(welcome_message, parse_mode="Markdown", reply_markup=reply_markup)

# Handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if user_input == "Start 🚀":
        return await start(update, context)

    if user_input.isdigit() and len(user_input) == 4:
        result = search_owner(user_input)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("Please send only the last 4 digits of the car number.")

# Replace with your bot token
TOKEN = "7683161854:AAG0ix3Nm-ZwEgxAe9DQvoNZeXcyYn8yiG4"

# Run the bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Starting bot script...")
print("Bot is running...")
app.run_polling()
