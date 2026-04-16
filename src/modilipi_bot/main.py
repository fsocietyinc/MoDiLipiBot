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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    message = update.message
    if message is None:
        return

    user = update.effective_user
    if user is None:
        return  

    await message.reply_html(
        rf"नमस्कार {user.mention_html()}, कृपया तुमचा मोडीमधे हवा असणार मजकूर देवनागरीत लिहून पाठवा.",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""

    message = update.message
    if message is None:
        return

    await message.reply_text(
        "Send me text in Devanagari script, and I'll convert it to Modi Lipi and send it as an image!\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message"
    )


async def translated_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None or message.text is None:
        return

    translated_text = transliterate.process("Devanagari", "Modi", message.text)
    img = convert(
        quote=translated_text,
        fg="white",
        image=str(BASE_DIR / "assets" / "background_image" / "background1.png"),
        border_color="white",
        font_size=70,
        width=1200,
        height=670,
    )

    # Send the translated text first
    await message.reply_text(f"Modi Lipi: ```\n{translated_text}\n```", parse_mode="MarkdownV2")

    # Save the image as a PNG file
    img_path = BASE_DIR / "assets" / "generated_image" / "quote.png"
    img.save(str(img_path))
    await message.reply_photo(photo=open(str(img_path), "rb"))


def main() -> None:
    """Start the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, translated_text)
    )

    # Run the bot until the user presses Ctrl-C

    application.run_polling()


if __name__ == "__main__":
    main()
