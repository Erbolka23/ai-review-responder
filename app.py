import json
from datetime import datetime
import streamlit as st
from responder import generate_reply, generate_reply_auto

def save_history(business_type, mode, style, review_text, reply):
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "business_type": business_type,
        "mode": mode,
        "style": style,
        "review": review_text,
        "reply": reply,
    }

    with open("history.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


st.set_page_config(page_title="AI Review Responder", page_icon="💬")

st.title("💬 AI Review Responder")
st.caption("Генератор ответов на отзывы для малого бизнеса (MVP)")

with st.sidebar:
    st.header("Настройки")

    business_type = st.text_input(
        "Тип бизнеса",
        placeholder="кофейня / салон красоты / стоматология"
    )

    mode = st.radio("Режим", ["Ручной", "Авто"], horizontal=True)

    style = None
    if mode == "Ручной":
        style = st.selectbox(
            "Стиль",
            ["официальный", "дружелюбный", "короткий"]
        )

    st.divider()
    st.write("Совет: сначала протестируй на 5–10 реальных отзывах.")


review_text = st.text_area(
    "Текст отзыва клиента",
    height=160,
    placeholder="Вставь отзыв сюда..."
)

col1, col2 = st.columns(2)
with col1:
    generate_btn = st.button(
        "Сгенерировать ответ",
        type="primary",
        use_container_width=True
    )
with col2:
    clear_btn = st.button(
        "Очистить",
        use_container_width=True
    )

if clear_btn:
    st.rerun()

if generate_btn:
    if not business_type.strip():
        st.error("Введите тип бизнеса.")
    elif not review_text.strip():
        st.error("Введите текст отзыва.")
    else:
        with st.spinner("Генерирую ответ..."):
            try:
                if mode == "Авто":
                    reply, sentiment = generate_reply_auto(
                        business_type.strip(),
                        review_text.strip()
                    )
                    st.info(f"Тональность определена как: {sentiment}")
                    used_style = "auto"
                else:
                    reply = generate_reply(
                        business_type.strip(),
                        review_text.strip(),
                        style
                    )
                    used_style = style

                save_history(
                    business_type.strip(),
                    mode,
                    used_style,
                    review_text.strip(),
                    reply
                )

                st.success("Готово!")
                st.subheader("Ответ")
                st.write(reply)

                st.download_button(
                    "Скачать ответ в .txt",
                    data=reply,
                    file_name="reply.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

            except Exception as e:
                st.error("Ошибка при обращении к API.")
                st.code(str(e))