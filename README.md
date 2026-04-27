# MoDiLipiBot | मोडी लिपी बॉट 

![MoDiLipiBot Example](chitra.PNG)

[👉 **Click here to use the Telegram Bot**](https://t.me/marathiMoDiLiPibot)

---

### मराठी

हा एक टेलिग्राम बॉट आहे जो देवनागरी (मराठी/हिंदी/संस्कृत) मजकूर ऐतिहासिक **मोडी लिपीत** रूपांतरित करतो आणि तो एक सुंदर, उच्च-गुणवत्तेच्या (High-Resolution) चित्राच्या रूपात परत पाठवतो. तुम्ही या बॉटचा वापर करून तुमचे विचार, वाक्ये आणि सुविचार जुन्या मोडी लिपीत जतन करून शेअर करू शकता.

**वैशिष्ट्ये:**
- देवनागरी ते मोडी लिपीत झटपट रूपांतर
- अतिशय सुबक आणि १०८०p (1080p) रिझोल्यूशनमध्ये चित्राची निर्मिती
- सहज कॉपी करता येणारा (1-tap copy) मोडी मजकूर

---

### English

This is a Telegram Bot that seamlessly transliterates Devanagari (Marathi/Hindi/Sanskrit) text into the historical **Modi script**. It then generates and returns a beautiful, high-resolution (1080p) image of the transliterated text. You can use this bot to preserve and share your thoughts, quotes, and sentences in the ancient Modi script.

**Features:**
- Instant transliteration from Devanagari to Modi Script
- Beautiful high-resolution (1920x1080) image generation
- 1-tap easily copyable raw text output

---

### Commands | कमांड्स
- `/start` or `/help` - Show the welcome and help message.
- `/generate <text>` - Instantly convert the given Devanagari text to Modi Lipi.
- `/generate` - Prompt the bot to ask for text.

---

## Setup & Installation | स्थापना

### 1. Create a Telegram Bot
Before running the bot, you need to create one on Telegram and get your Bot Token.
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Start a chat and send the command `/newbot`.
3. Follow the instructions to choose a name and username for your bot.
4. Once created, BotFather will give you an HTTP API Token (e.g., `123456789:ABCdef...`). Keep this token secure!

### 2. Running Locally (with Python)
This project uses `uv` for fast package management.

1. Clone the repository:
   ```bash
   git clone https://github.com/fsocietyinc/MoDiLipiBot.git
   cd MoDiLipiBot
   ```

2. Export your bot token as an environment variable:
   ```bash
   export TOKEN="your_bot_token_here"
   ```

3. Run the bot:
   ```bash
   uv run bot
   ```

### 3. Running with Docker (Recommended)
You can easily deploy the bot 24/7 using Docker Compose.

1. Create a `.env` file in the root directory and add your token:
   ```env
   TOKEN=your_bot_token_here
   ```

2. Start the container in the background:
   ```bash
   docker compose up -d
   ```