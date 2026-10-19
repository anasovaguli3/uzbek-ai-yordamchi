"""O'zbekcha AI yordamchi — Telegram bot versiyasi."""

import logging
import os

import anthropic
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# .env faylidan ANTHROPIC_API_KEY va TELEGRAM_BOT_TOKEN ni o'qiydi
load_dotenv()

MODEL = "claude-opus-5-5"
SYSTEM = (
    "Sen o'zbek tilida gaplashadigan foydali yordamchisan. "
    "Har doim o'zbek tilida (lotin yozuvida), aniq va qisqa javob ber. "
    "Javoblaring Telegram'da o'qiladi, shuning uchun markdown jadvallardan foydalanma."
)
MAX_XABAR = 20  # har bir foydalanuvchi uchun eslab qolinadigan xabarlar soni
TELEGRAM_LIMIT = 4096  # Telegram bitta xabarga ruxsat beradigan belgilar soni

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

client = anthropic.AsyncAnthropic()
tarixlar: dict[int, list[dict]] = {}  # chat_id -> suhbat tarixi


async def javob_ol(chat_id: int, savol: str) -> str:
    tarix = tarixlar.setdefault(chat_id, [])
    tarix.append({"role": "user", "content": savol})

    try:
        response = await client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM,
            messages=tarix,
            # Model rad etsa, server avtomatik boshqa modelga o'tkazadi
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
    except Exception:
        tarix.pop()  # muvaffaqiyatsiz savolni tarixda qoldirmaymiz
        raise

    if response.stop_reason == "refusal":
        tarix.pop()
        return "Kechirasiz, bu savolga javob bera olmayman."

    javob = "".join(b.text for b in response.content if b.type == "text")
    tarix.append({"role": "assistant", "content": javob})

    # Tarix juda uzayib ketmasin: eng eski savol-javob juftlarini o'chiramiz
    while len(tarix) > MAX_XABAR:
        del tarix[:2]
    return javob


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! Men o'zbek tilida gaplashadigan AI yordamchiman.\n"
        "Istalgan savolingizni yozing.\n\n"
        "/yangi — suhbatni boshidan boshlash"
    )


async def yangi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tarixlar.pop(update.effective_chat.id, None)
    await update.message.reply_text("Yangi suhbat boshlandi. Savolingizni yozing.")


async def xabar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_chat_action(chat_id, ChatAction.TYPING)

    try:
        javob = await javob_ol(chat_id, update.message.text)
    except anthropic.AuthenticationError:
        logging.error("Anthropic API kaliti noto'g'ri")
        javob = "Server sozlamalarida xato bor. Keyinroq urinib ko'ring."
    except anthropic.RateLimitError:
        javob = "Hozir so'rovlar juda ko'p. Bir daqiqadan keyin urinib ko'ring."
    except anthropic.APIConnectionError:
        javob = "AI serveriga ulanib bo'lmadi. Qayta urinib ko'ring."
    except anthropic.APIStatusError as e:
        logging.error("API xatosi %s: %s", e.status_code, e.message)
        javob = "Xatolik yuz berdi. Qayta urinib ko'ring."

    # Uzun javoblarni bir nechta xabarga bo'lib yuboramiz
    for i in range(0, len(javob), TELEGRAM_LIMIT):
        await update.message.reply_text(javob[i : i + TELEGRAM_LIMIT])


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit(".env faylida TELEGRAM_BOT_TOKEN yo'q")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("yangi", yangi))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xabar))

    logging.info("Bot ishga tushdi")
    app.run_polling()


if __name__ == "__main__":
    main()
