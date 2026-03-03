from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(business_type: str, review_text: str, style: str) -> str:
    system_prompt = f"""
Ты помощник для малого бизнеса. Пиши ответы на отзывы клиентов на русском.
Тип бизнеса: {business_type}
Стиль: {style}

Правила:
- Вежливо, профессионально
- Если отзыв негативный — извинись и предложи решение/контакт
- Если отзыв позитивный — поблагодари и пригласи снова
- Не выдумывай факты
- 60–120 слов
"""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": review_text},
        ],
        temperature=0.5,
    )
    return resp.choices[0].message.content.strip()
def detect_sentiment(review_text: str) -> str:
    """
    Возвращает: 'positive' | 'neutral' | 'negative'
    """
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Определи тональность отзыва. Ответь строго одним словом: positive, neutral или negative."},
            {"role": "user", "content": review_text},
        ],
        temperature=0.0,
    )

    label = resp.choices[0].message.content.strip().lower()
    if label not in ("positive", "neutral", "negative"):
        return "neutral"
    return label
def generate_reply_auto(business_type: str, review_text: str) -> tuple[str, str]:
    sentiment = detect_sentiment(review_text)

    if sentiment == "negative":
        style = "официальный"
        extra = "Сделай акцент на извинении и решении проблемы."
    elif sentiment == "positive":
        style = "дружелюбный"
        extra = "Сделай акцент на благодарности и приглашении прийти снова."
    else:
        style = "официальный"
        extra = "Ответ нейтральный, вежливый, короткий."

    # Используем ту же generate_reply, но добавляем подсказку в отзыв
    reply = generate_reply(business_type, f"{review_text}\n\nПодсказка: {extra}", style)
    return reply, sentiment