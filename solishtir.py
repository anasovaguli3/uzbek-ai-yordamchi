"""Lokal modellarni o'zbekcha savollarda solishtirish."""

import time

import ollama

MODELLAR = ["gemma3:4b", "qwen3:8b"]
SYSTEM = (
    "Sen o'zbek tilida gaplashadigan foydali yordamchisan. "
    "Har doim o'zbek tilida (lotin yozuvida), aniq va qisqa javob ber."
)
SAVOLLAR = [
    "Salom! O'zing haqingda 2 gapda aytib ber.",
    "Python'da list va dict o'rtasidagi farq nima? Qisqa tushuntir.",
    "Toshkentda kuzda qayerlarga borish mumkin? 3 ta joy ayt.",
    "Quyidagi matn asosida 2 ta test savoli tuz (javob variantlari bilan): "
    "Amir Temur 1336-yilda Kesh yaqinidagi Xo'ja Ilg'or qishlog'ida tug'ilgan. "
    "U Samarqandni o'z davlatining poytaxtiga aylantirgan.",
]

for model in MODELLAR:
    print("=" * 70)
    print(f"MODEL: {model}")
    jami = 0.0
    for savol in SAVOLLAR:
        boshlash = time.time()
        javob = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": savol},
            ],
            think=False if model.startswith("qwen3") else None,
        )
        vaqt = time.time() - boshlash
        jami += vaqt
        print(f"\n--- Savol: {savol[:60]}...")
        print(f"[{vaqt:.1f} s]")
        print(javob.message.content.strip())
    print(f"\nJami vaqt: {jami:.1f} s")
