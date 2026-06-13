import os
import redis
from models import Author, Quote
from dotenv import load_dotenv

load_dotenv()

# Підключення до твого створеного хмарного Redis Upstash (з підтримкою SSL/TLS)
r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
    ssl=True  # Захищене з'єднання для Upstash
)

def search_quotes():
    print("🔍 Скрипт пошуку запущено. Доступні команди: name:, tag:, tags:, exit")
    
    while True:
        user_input = input("\nВведіть команду: ").strip()
        
        if user_input.startswith("exit"):
            print("Бувай!")
            break
            
        if ":" not in user_input:
            print("Невірний формат. Використовуйте наприклад: name: Albert Einstein або tag: life")
            continue
            
        command, value = user_input.split(":", 1)
        command = command.strip()
        value = value.strip()

        # Робота з кешем для команд name та tag
        if command in ["name", "tag"]:
            redis_key = f"{command}:{value}"
            try:
                cached_result = r.get(redis_key)
                if cached_result:
                    print(f"⚡ [КЕШ REDIS] Результат миттєво взято з кешу Upstash:")
                    print(cached_result)
                    continue
            except Exception as e:
                print(f"⚠️ Помилка Redis при читанні: {e}")

        result_texts = []

        if command == "name":
            author = Author.objects(fullname__icontains=value).first()
            if author:
                quotes = Quote.objects(author=author)
                result_texts = [q.quote for q in quotes]
                
        elif command == "tag":
            quotes = Quote.objects(tags__icontains=value)
            result_texts = [q.quote for q in quotes]
            
        elif command == "tags":
            tag_list = [t.strip() for t in value.split(",")]
            quotes = Quote.objects(tags__in=tag_list)
            result_texts = [q.quote for q in quotes]

        if result_texts:
            output = "\n---\n".join(result_texts)
            print(output)
            
            if command in ["name", "tag"]:
                try:
                    r.set(redis_key, output, ex=600)
                    print("💾 Результат успішно збережено в кеш Redis на 10 хвилин.")
                except Exception as e:
                    print(f"⚠️ Помилка Redis при записі: {e}")
        else:
            print("Нічого не знайдено.")

if __name__ == '__main__':
    search_quotes()