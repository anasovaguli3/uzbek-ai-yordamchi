"""O'zbekcha AI yordamchi — terminalda ishlaydigan chat (1-versiya)."""

import anthropic
from dotenv import load_dotenv

# .env faylidan ANTHROPIC_API_KEY ni o'qiydi
load_dotenv()

MODEL = "claude-opus-5-5"
SYSTEM = (
    "Sen o'zbek tilida gaplashadigan foydali yordamchisan. "
    "Har doim o'zbek tilida (lotin yozuvida), aniq va qisqa javob ber."
)

client = anthropic.Anthropic()
xabarlar = []  # suhbat tarixi: API har safar butun tarixni ko'rishi kerak


def javob_ol(savol: str) -> str:
    xabarlar.append({"role": "user", "content": savol})

    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=xabarlar,
        # Model rad etsa, server avtomatik boshqa modelga o'tkazadi
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )

    if response.stop_reason == "refusal":
        xabarlar.pop()  # rad etilgan savolni tarixdan olib tashlaymiz
        return "Kechirasiz, bu savolga javob bera olmayman."

    javob = "".join(b.text for b in response.content if b.type == "text")
    xabarlar.append({"role": "assistant", "content": response.content})
    return javob


def main():
    print("O'zbekcha AI yordamchi. Chiqish uchun 'chiq' deb yozing.\n")
    while True:
        savol = input("Siz: ").strip()
        if not savol:
            continue
        if savol.lower() in ("chiq", "exit", "quit"):
            print("Xayr!")
            break
        try:
            print(f"\nAI: {javob_ol(savol)}\n")
        except anthropic.AuthenticationError:
            print("API kalit noto'g'ri. .env faylini tekshiring.")
            break
        except anthropic.APIConnectionError:
            print("Internetga ulanib bo'lmadi. Qayta urinib ko'ring.")
            xabarlar.pop()
        except anthropic.APIStatusError as e:
            print(f"API xatosi ({e.status_code}): {e.message}")
            xabarlar.pop()


if __name__ == "__main__":
    main()
