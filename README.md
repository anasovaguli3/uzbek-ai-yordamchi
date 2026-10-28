# O'zbekcha AI yordamchi

O'zbek tilida gaplashadigan AI yordamchi — Telegram bot. Ikki rejimda ishlaydi:
- **Lokal (bepul):** [Ollama](https://ollama.com) orqali kompyuteringizdagi model (standart: `qwen3:8b`)
- **Bulut:** Claude API (sifatliroq, pullik)

## Imkoniyatlar
- O'zbek tilida suhbat
- Har bir foydalanuvchi bilan suhbat tarixini alohida eslab qoladi
- Provayderni `.env` orqali bitta qator bilan almashtirish
- Xatoliklarni tushunarli xabar bilan ko'rsatadi

## O'rnatish

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Lokal rejim uchun Ollama'ni o'rnating va modelni yuklang:
```bash
ollama pull qwen3:8b
```

`.env.example` faylini `.env` deb nusxalang va to'ldiring:
- `TELEGRAM_BOT_TOKEN` — Telegram'da [@BotFather](https://t.me/BotFather) dan
- `PROVIDER` — `ollama` yoki `claude`
- `ANTHROPIC_API_KEY` — faqat `claude` rejimi uchun, [console.anthropic.com](https://console.anthropic.com) dan

## Ishga tushirish

```bash
python bot.py
```

## Bot buyruqlari
- `/start` — salomlashish
- `/yangi` — suhbatni boshidan boshlash

## Lokal modellarni solishtirish
`solishtir.py` bir xil o'zbekcha savollarni bir nechta modelga berib, javob va tezlikni chiqaradi.

| Model | O'zbekcha sifat | Tezlik (RTX 4060) |
|---|---|---|
| gemma3:4b | O'rtacha, g'aliz so'zlar | 1–2 s |
| qwen3:8b | Yaxshi, matn asosida test tuzadi | 3–5 s |

Ikkala model ham faktlarni ba'zan to'qib chiqaradi (gallyutsinatsiya) — keyingi bosqichda RAG bilan hal qilinadi.

## Reja
- [x] Terminal chat (Claude)
- [x] Telegram bot
- [x] Lokal model (Ollama) qo'llab-quvvatlash
- [ ] Fayl (PDF/TXT) yuklab, undan savol-javob tuzish
- [ ] Demo GIF
