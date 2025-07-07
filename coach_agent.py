from fastapi import FastAPI, Request
from groqChatbot import get_groq_response
import random

app = FastAPI()

@app.post("/agent/chat")
async def coach_agent(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    print("user:", prompt)

    motivation_prompt = f"L'utilisateur dit : '{prompt}'\n\nTu es un coach motivant. Réponds avec un message très motivant, humain et positif pour encourager l'utilisateur à continuer ses révisions. Sois chaleureux."

    motivation_message = get_groq_response(motivation_prompt)

    print("💬 Motivation CoachAgent :\n\n👨‍🏫 Motivation:\n", motivation_message)

    return {"reply": motivation_message}
## Stockage local des messages générés
MESSAGES = [
    "💪 Continue comme ça, tu es sur la bonne voie !",
    "🚀 Tu progresses chaque jour, ne lâche rien !",
]

@app.get("/coach/motivate")
def motivate():
    prompt = (
        "Generate a short motivational, positive and human message in English for a student "
        "who is doing a quiz or studying. Keep it short and encouraging."
    )

    try:
        new_message = get_groq_response(prompt).strip()

        if new_message and new_message not in MESSAGES:
            MESSAGES.append(new_message)
            print("🆕 Nouveau message ajouté :", new_message)

        return {"message": new_message}  # ✅ on renvoie toujours le nouveau

    except Exception as e:
        print("❌ Erreur get_groq_response:", str(e))
        return {"message": random.choice(MESSAGES)}  # fallback local