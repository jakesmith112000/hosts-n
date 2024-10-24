import telebot
import re
import random
import string

API_TOKEN = '7987008476:AAEwU9EiLyRiTX5ctpiy1nBIvxFzNne29KU'  # Replace with your actual Telegram bot token
bot = telebot.TeleBot(API_TOKEN)

# List of admin user IDs
ADMINS = [1396561970, 1971995086, 5084753170]

# Regex patterns for both options
pattern1 = r'^\d{2}/\d{2}/\d{4}$'  # For a single date input
pattern2 = r'^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}\n\d{2}/\d{2}/\d{4}$'  # For the alphanumeric code + date input

def generate_random_numbers(count):
    """Generate a string of random digits of specified count."""
    return ''.join(random.choices(string.digits, k=count))

def generate_random_letters(count):
    """Generate a string of random uppercase letters of specified count."""
    return ''.join(random.choices(string.ascii_uppercase, k=count))

def generate_ildkru():
    """Generate the ILDKRU01 format with random 4 uppercase letters."""
    return f"IL{generate_random_letters(4)}01"

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Please provide your DD info in one of these formats:\n"
                                      "1. 09/23/2028\n"
                                      "2. G610-5059-3893\n05/23/2026")

# Admin check decorator
def admin_only(func):
    def wrapper(message):
        user_id = message.from_user.id
        if user_id in ADMINS:
            return func(message)
        else:
            bot.reply_to(message, "🚫 You are not authorized to use this bot.")
    return wrapper

@bot.message_handler(func=lambda message: True)
def handle_dd_input(message):
    user_input = message.text.strip()

    # Attempt to match both patterns
    if re.match(pattern2, user_input):
        # Handle alphanumeric code + date (Option 2)
        handle_dd_format2(message, user_input)
    elif re.match(pattern1, user_input):
        # Handle just the date (Option 1)
        handle_dd_format1(message, user_input)
    else:
        # Send error message if input doesn't match either format
        bot.send_message(message.chat.id, "Invalid format! Please make sure the input matches one of the two formats:\n"
                                          "1. 09/23/2028\n"
                                          "2. G610-5059-3893\n05/23/2026")

def handle_dd_format1(message, user_input):
    """Handles the single date input (e.g., 09/23/2028)."""
    try:
        # Convert date format from MM/DD/YYYY to YYYYMMDD
        date_parts = user_input.split('/')
        formatted_date = f"{date_parts[2]}{date_parts[0]}{date_parts[1]}"
        
        # Generate 3 random numbers, 2 random letters, 4 random numbers
        random_part = f"{generate_random_numbers(3)}{generate_random_letters(2)}{generate_random_numbers(4)}"
        
        # Generate ILDKRU01 with random letters
        ildkru = generate_ildkru()
        
        # Construct final output
        final_output = f"{formatted_date}{random_part}"
        
        # Send transformed DD info and ILDKRU string to the user
        bot.send_message(message.chat.id, f"Transformed DD info:\n{final_output}\nILDKRU: {ildkru}")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while processing your input: {e}")

def handle_dd_format2(message, user_input):
    """Handles the alphanumeric code + date input (e.g., G610-5059-3893 and 05/23/2026)."""
    try:
        # Split the input into the alphanumeric code and the date
        code, date = user_input.split('\n')
        
        # Remove dashes from the alphanumeric code
        sanitized_code = code.replace("-", "")
        
        # Convert date format from MM/DD/YYYY to YYYYMMDD
        date_parts = date.split('/')
        formatted_date = f"{date_parts[2]}{date_parts[0]}{date_parts[1]}"
        
        # Generate 3 random numbers, 2 random letters, 4 random numbers
        random_part = f"{generate_random_numbers(3)}{generate_random_letters(2)}{generate_random_numbers(4)}"
        
        # Generate ILDKRU01 with random letters
        ildkru = generate_ildkru()
        
        # Construct final output
        final_output = f"{sanitized_code}\n{formatted_date}{random_part}"
        
        # Send transformed DD info and ILDKRU string to the user
        bot.send_message(message.chat.id, f"Transformed DD info:\n{final_output}\n {ildkru}")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while processing your input: {e}")

# Start polling
bot.polling()
