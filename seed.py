import json
from models import Author, Quote

def load_data():
    with open('authors.json', 'r', encoding='utf-8') as f:
        authors_data = json.load(f)
        for auth in authors_data:
            existing_author = Author.objects(fullname=auth['fullname']).first()
            if not existing_author:
                Author(
                    fullname=auth['fullname'],
                    born_date=auth['born_date'],
                    born_location=auth['born_location'],
                    description=auth['description']
                ).save()
                print(f"Додано автора: {auth['fullname']}")
            else:
                print(f"Автор вже існує: {auth['fullname']} (пропущено)")

    with open('quotes.json', 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
        for q in quotes_data:
            author = Author.objects(fullname=q['author']).first()
            if author:
                existing_quote = Quote.objects(author=author, quote=q['quote']).first()
                if not existing_quote:
                    Quote(
                        tags=q['tags'],
                        author=author,
                        quote=q['quote']
                    ).save()
                    print(f"Додано цитату для: {q['author']}")
                else:
                    print(f"Цитата для {q['author']} вже є в базі (пропущено)")

if __name__ == '__main__':
    load_data()