import json
from typing import List, Optional


class Book:
    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        id: int,
        status: str = "В наличии",
    ):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title}, author={self.author}, year={self.year}, status={self.status})"


class Library:
    def __init__(self, data_file: str = "library.json"):
        self.books: List[Book] = []
        self.data_file = data_file
        self.load_data()

    def load_data(self) -> None:
        """Load books from the JSON data file."""
        try:
            with open(self.data_file, "r") as file:
                books_data = json.load(file)
                for book in books_data:
                    self.books.append(Book(**book))
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Ошибка чтения файла данных.")

    def save_data(self) -> None:
        """Save books to the JSON data file."""
        with open(self.data_file, "w") as file:
            json.dump(
                [book.__dict__ for book in self.books],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def add_book(self, title: str, author: str, year: int) -> None:
        """Add a new book to the library."""
        book_id = self.generate_id()
        new_book = Book(title, author, year, book_id)
        self.books.append(new_book)
        self.save_data()

    def generate_id(self) -> int:
        """Generate a unique book ID."""
        if self.books:
            return max(book.id for book in self.books) + 1
        return 1

    def remove_book(self, book_id: int) -> bool:
        """Remove a book from the library by ID."""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_data()
                return True
        return False

    def search_books(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
    ) -> List[Book]:
        """Search for books by title, author, or year."""
        results = [
            book
            for book in self.books
            if (title and title.lower() in book.title.lower())
            or (author and author.lower() in book.author.lower())
            or (year and book.year == year)
        ]
        return results

    def display_books(self) -> None:
        """Display all books in the library."""
        for book in self.books:
            print(book)

    def change_status(self, book_id: int, new_status: str) -> bool:
        """Change the status of a book."""
        if new_status not in ["в наличии", "выдана"]:
            print("Некорректный статус.")
            return False
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_data()
                return True
        return False


def main():
    library = Library()

    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название: ")
            author = input("Введите автора: ")
            year = int(input("Введите год издания: "))
            library.add_book(title, author, year)
            print("Книга добавлена.")

        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            if library.remove_book(book_id):
                print("Книга удалена.")
            else:
                print("Книга с таким ID не найдена.")

        elif choice == "3":
            search_type = input("Искать по (title/author/year): ").strip().lower()
            if search_type == "title":
                title = input("Введите название: ")
                results = library.search_books(title=title)
            elif search_type == "author":
                author = input("Введите автора: ")
                results = library.search_books(author=author)
            elif search_type == "year":
                year = int(input("Введите год издания: "))
                results = library.search_books(year=year)
            else:
                results = []

            if results:
                for book in results:
                    print(book)
            else:
                print("Книги не найдены.")

        elif choice == "4":
            library.display_books()

        elif choice == "5":
            book_id = int(input("Введите ID книги: "))
            new_status = input("Введите новый статус (в наличии/выдана): ")
            if library.change_status(book_id, new_status):
                print("Статус изменен.")
            else:
                print("Ошибка изменения статуса.")

        elif choice == "6":
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
