from responder import generate_reply

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Пустой ввод недопустим. Попробуйте снова.\n")

def main():
    print("=== AI Review Responder ===\n")

    while True:
        business = get_non_empty_input("Тип бизнеса: ")
        review = get_non_empty_input("Текст отзыва: ")
        style = get_non_empty_input("Стиль (официальный / дружелюбный / короткий): ")

        print("\nГенерация ответа...\n")

        try:
            reply = generate_reply(business, review, style)

            print("\n==============================")
            print("СГЕНЕРИРОВАННЫЙ ОТВЕТ:\n")
            print(reply)
            print("==============================\n")

        except Exception as e:
            print("Ошибка при обращении к API:", e)

        again = input("Сгенерировать ещё один ответ? (y/n): ").lower()
        if again != "y":
            print("Завершение работы.")
            break


if __name__ == "__main__":
    main()