import logging
import os
from pathlib import Path

from aksharamukha import transliterate
from telegram import ForceReply, Update
from telegram import __version__ as TG_VER
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram import BotCommand
from html import escape

from modilipi_bot.quote2image import convert


def get_project_root():
    """Find the project root by searching for pyproject.toml upwards."""
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError("Could not find project root (pyproject.toml not found)")


BASE_DIR = get_project_root()

TOKEN = os.environ["TOKEN"]

try:
    from telegram import __version_info__

except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]


if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )


# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

async def post_init(application: Application) -> None:
    """Set bot commands in Telegram menu."""
    await application.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help message"),
        BotCommand("generate", "Convert Devanagari to Modi Lipi"),
    ])



async def start_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start or /help is issued."""
    message = update.message
    if message is None:
        return

    user = update.effective_user
    greeting = rf"नमस्कार {user.mention_html()}," if user else "नमस्कार,"

    help_text = (
        f"{greeting}\n\n"
        "Send me text in Devanagari script, and I'll convert it to Modi Lipi and send it as an image!\n\n"
        "<b>Commands:</b>\n"
        "/start or /help - Show this help message\n"
        "/generate &lt;text&gt; - Convert the given text to Modi Lipi\n"
        "/generate - Prompt for text to convert\n\n"
        "<i>You can also just send me any Devanagari text directly to convert it.</i>"
    )

    await message.reply_html(help_text)


async def _process_translation(message, text_to_translate: str) -> None:
    translated_text_str = transliterate.process("Devanagari", "Modi", text_to_translate)
    img = convert(
        quote=translated_text_str,
        fg="white",
        image=str(BASE_DIR / "assets" / "background_image" / "background1.png"),
        border_color="white",
        font_size=70,
        width=1200,
        height=670,
    )

    # Send the translated text first, wrapped in HTML code block for easy copying
    safe_text = escape(translated_text_str)
    await message.reply_html(f"<b>Modi Lipi:</b>\n\n<code>{safe_text}</code>")

    # Save the image as a PNG file
    img_path = BASE_DIR / "assets" / "generated_image" / "quote.png"
    img.save(str(img_path))
    await message.reply_photo(photo=open(str(img_path), "rb"))


async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Convert text using /generate."""
    message = update.message
    if message is None:
        return

    if context.args:
        text_to_translate = " ".join(context.args)
        await _process_translation(message, text_to_translate)
    else:
        await message.reply_html(
            "कृपया तुमचा मोडीमधे हवा असणार मजकूर देवनागरीत लिहून पाठवा.",
            reply_markup=ForceReply(selective=True),
        )


async def translated_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process any direct text messages."""
    message = update.message
    if message is None or message.text is None:
        return

    await _process_translation(message, message.text)


def main() -> None:
    """Start the bot."""

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).post_init(post_init).build()

    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("start", start_help_command))
    application.add_handler(CommandHandler("help", start_help_command))
    application.add_handler(CommandHandler("generate", generate_command))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, translated_text)
    )

    # Run the bot until the user presses Ctrl-C

    application.run_polling()


if __name__ == "__main__":
    main()
