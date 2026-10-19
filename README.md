# O'zbekcha AI yordamchi

Claude API asosida o'zbek tilida gaplashadigan AI yordamchi.

## Imkoniyatlar
- O'zbek tilida suhbat
- Suhbat tarixini eslab qoladi
- Xatoliklarni tushunarli xabar bilan ko'rsatadi

## O'rnatish

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

`.env.example` faylini `.env` deb nusxalang va unga kalitlaringizni yozing:
- `ANTHROPIC_API_KEY` — [console.anthropic.com](https://console.anthropic.com) dan
- `TELEGRAM_BOT_TOKEN` — Telegram'da [@BotFather](https://t.me/BotFather) dan

## Ishga tushirish

Telegram bot:
```bash
python bot.py
```

Terminal chat:
```bash
python chat.py
```

## Bot buyruqlari
- `/start` — salomlashish
- `/yangi` — suhbatni boshidan boshlash

## Reja
- [x] Terminal chat (1-versiya)
- [x] Telegram bot
- [ ] Veb interfeys (Streamlit)
- [ ] Demo GIF
