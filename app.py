import os
print("KEY CHECK:", bool(os.environ.get("GROQ_API_KEY")))
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq

app = FastAPI()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """Ты — собеседник на венгерском языке. Уровень пользователя — A2-B1.
Отвечай по-венгерски, простыми предложениями.
В конце каждого ответа добавь блок:
--- Исправления ---
(если ошибок нет, напиши "Ошибок нет")
(если есть — перечисли ошибки и дай правильный вариант на русском)"""

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.get("/")
def index():
    with open("index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/api/chat")
def chat(req: ChatRequest):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(req.history)
    messages.append({"role": "user", "content": req.message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return {"reply": response.choices[0].message.content}...
