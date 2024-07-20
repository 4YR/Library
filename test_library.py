import unittest
import os
from io import StringIO
from unittest.mock import patch
from library import Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        """Creates a library object for use in tests."""
        self.test_file = "test_library.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.library = Library(data_file=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self):
        """Testing adding a new book to the library."""
        self.library.add_book("Test Title", "Test Author", 2024)
        books = self.library.books
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Test Title")
        self.assertEqual(books[0].author, "Test Author")
        self.assertEqual(books[0].year, 2024)

    def test_remove_book(self):
        """Tests the deletion of a book by ID."""
        self.library.add_book("Test Title", "Test Author", 2024)
        book_id = self.library.books[0].id
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books_by_title(self):
        """Tests the deletion of a book by title."""
        self.library.add_book("Unique Title", "Author", 2024)
        results = self.library.search_books(title="Unique Title")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Unique Title")

    def test_search_books_by_author(self):
        """Tests the deletion of a book by author."""
        self.library.add_book("Title", "Unique Author", 2024)
        results = self.library.search_books(author="Unique Author")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Unique Author")

    def test_search_books_by_year(self):
        """Tests the deletion of a book by year."""
        self.library.add_book("Title", "Author", 2024)
        results = self.library.search_books(year=2024)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].year, 2024)

    def test_display_books(self):
        """Test the display_books method by adding a book,
        displaying all books, and checking the output."""
        self.library.add_book("Title", "Author", 2024)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.library.display_books()
            output = fake_out.getvalue().strip()
        self.assertIn("Book(id=", output)

    def test_change_status(self):
        """Tests the change in the status of the book."""
        self.library.add_book("Title", "Author", 2024)
        book_id = self.library.books[0].id
        self.library.change_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_invalid_status(self):
        """Tests the processing of the incorrect status of the book."""
        self.library.add_book("Title", "Author", 2024)
        book_id = self.library.books[0].id
        result = self.library.change_status(book_id, "invalid_status")
        self.assertFalse(result)
        self.assertEqual(self.library.books[0].status, "В наличии")


if __name__ == "__main__":
    unittest.main()
