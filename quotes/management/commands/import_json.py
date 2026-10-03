import json
from pathlib import Path

from django.core.management.base import BaseCommand

from quotes.models import Author, Quote


class Command(BaseCommand):
    help = "Імпорт авторів і цитат з JSON"

    def handle(self, *args, **kwargs):
        root = Path(__file__).resolve().parents[3]

        authors_file = root / "authors.json"
        quotes_file = root / "quotes.json"

        if not authors_file.exists():
            self.stdout.write(
                self.style.ERROR(f"Не знайдено файл: {authors_file}")
            )
            return

        if not quotes_file.exists():
            self.stdout.write(
                self.style.ERROR(f"Не знайдено файл: {quotes_file}")
            )
            return

        with authors_file.open("r", encoding="utf-8") as file:
            authors = json.load(file)

        with quotes_file.open("r", encoding="utf-8") as file:
            quotes = json.load(file)

        authors_count = 0

        for author_data in authors:
            Author.objects.update_or_create(
                fullname=author_data["fullname"],
                defaults={
                    "born_date": author_data.get("born_date", ""),
                    "born_location": author_data.get("born_location", ""),
                    "description": author_data.get("description", ""),
                },
            )
            authors_count += 1

        quotes_count = 0

        for quote_data in quotes:
            author = Author.objects.filter(
                fullname=quote_data["author"]
            ).first()

            if not author:
                self.stdout.write(
                    self.style.WARNING(
                        f"Автор не знайдений: {quote_data['author']}"
                    )
                )
                continue

            _, created = Quote.objects.get_or_create(
                quote=quote_data["quote"],
                author=author,
                defaults={
                    "tags": quote_data.get("tags", []),
                },
            )

            if created:
                quotes_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Імпорт завершено. "
                f"Авторів оброблено: {authors_count}. "
                f"Нових цитат додано: {quotes_count}."
            )
        )