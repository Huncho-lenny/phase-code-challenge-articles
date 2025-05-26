import pytest
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

class TestAuthor:
    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Reset database state before each test"""
        conn = get_connection()
        # Clear tables in reverse dependency order
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM authors")
        conn.execute("DELETE FROM magazines")
        conn.commit()
        conn.close()

    @pytest.fixture
    def sample_author(self):
        return Author("J.K. Rowling").save()

    @pytest.fixture
    def sample_magazine(self):
        return Magazine("Fantasy World", "Fiction").save()

    def test_author_creation(self):
        author = Author("George Orwell")
        assert author.name == "George Orwell"
        assert author.id is None

    def test_save_author(self):
        author = Author("Agatha Christie").save()
        assert author.id is not None
        assert isinstance(author.id, int)

    def test_find_by_id(self, sample_author):
        found = Author.find_by_id(sample_author.id)
        assert found.id == sample_author.id
        assert found.name == sample_author.name

    def test_find_by_name(self, sample_author):
        found = Author.find_by_name("J.K. Rowling")
        assert found.id == sample_author.id
        assert found.name == sample_author.name

    def test_invalid_name(self):
        with pytest.raises(ValueError):
            Author("")  # Empty name
        with pytest.raises(ValueError):
            Author(123)  # Non-string name

    def test_add_article(self, sample_author, sample_magazine):
        article = sample_author.add_article(sample_magazine, "Magical Creatures")
        assert isinstance(article, Article)
        assert article.author_id == sample_author.id
        assert article.magazine_id == sample_magazine.id

    def test_articles_relationship(self, sample_author, sample_magazine):
        sample_author.add_article(sample_magazine, "The Philosopher's Stone")
        sample_author.add_article(sample_magazine, "Chamber of Secrets")
        
        articles = sample_author.articles()
        assert len(articles) == 2
        assert all(isinstance(a, Article) for a in articles)
        assert {a.title for a in articles} == {
            "The Philosopher's Stone",
            "Chamber of Secrets"
        }

    def test_magazines_relationship(self, sample_author):
        mag1 = Magazine("Fantasy Monthly", "Fiction").save()
        mag2 = Magazine("Best Sellers", "General").save()
        
        sample_author.add_article(mag1, "Fantasy Article")
        sample_author.add_article(mag2, "General Article")
        sample_author.add_article(mag1, "Sequel Article")  # Same magazine
        
        magazines = sample_author.magazines()
        assert len(magazines) == 2  # Should be distinct
        assert {m.name for m in magazines} == {"Fantasy Monthly", "Best Sellers"}

    def test_unique_name_constraint(self):
        Author("Unique Author").save()
        with pytest.raises(Exception):  # Should trigger SQLite integrity error
            Author("Unique Author").save()