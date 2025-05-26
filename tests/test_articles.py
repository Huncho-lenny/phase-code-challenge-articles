import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

class TestArticle:
    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Clean database state before each test"""
        conn = get_connection()
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM authors")
        conn.execute("DELETE FROM magazines")
        conn.commit()
        conn.close()

    @pytest.fixture
    def sample_author(self):
        return Author("Technical Writer").save()

    @pytest.fixture
    def sample_magazine(self):
        return Magazine("Code Weekly", "Programming").save()

    @pytest.fixture
    def sample_article(self, sample_author, sample_magazine):
        return Article("Python Best Practices", sample_author.id, sample_magazine.id).save()

    def test_article_creation(self, sample_author, sample_magazine):
        article = Article("New Python Features", sample_author.id, sample_magazine.id)
        assert article.title == "New Python Features"
        assert article.author_id == sample_author.id
        assert article.magazine_id == sample_magazine.id
        assert article.id is None

    def test_save_article(self, sample_article):
        assert sample_article.id is not None
        assert isinstance(sample_article.id, int)

    def test_find_by_id(self, sample_article):
        found = Article.find_by_id(sample_article.id)
        assert found.id == sample_article.id
        assert found.title == sample_article.title

    def test_find_by_title(self):
        Article("Python Decorators", 1, 1).save()
        Article("Python Context Managers", 1, 1).save()
        
        results = Article.find_by_title("Python")
        assert len(results) == 2
        assert {a.title for a in results} == {
            "Python Decorators",
            "Python Context Managers"
        }

    def test_find_by_author(self, sample_author, sample_magazine):
        Article("Article 1", sample_author.id, sample_magazine.id).save()
        Article("Article 2", sample_author.id, sample_magazine.id).save()
        
        other_author = Author("Other Writer").save()
        Article("Other Article", other_author.id, sample_magazine.id).save()
        
        author_articles = Article.find_by_author(sample_author.id)
        assert len(author_articles) == 2
        assert all(a.author_id == sample_author.id for a in author_articles)

    def test_find_by_magazine(self, sample_author, sample_magazine):
        Article("Magazine Article 1", sample_author.id, sample_magazine.id).save()
        Article("Magazine Article 2", sample_author.id, sample_magazine.id).save()
        
        other_mag = Magazine("Other Mag", "General").save()
        Article("Other Article", sample_author.id, other_mag.id).save()
        
        mag_articles = Article.find_by_magazine(sample_magazine.id)
        assert len(mag_articles) == 2
        assert all(a.magazine_id == sample_magazine.id for a in mag_articles)

    def test_author_relationship(self, sample_article, sample_author):
        author = sample_article.author()
        assert isinstance(author, Author)
        assert author.id == sample_author.id
        assert author.name == sample_author.name

    def test_magazine_relationship(self, sample_article, sample_magazine):
        magazine = sample_article.magazine()
        assert isinstance(magazine, Magazine)
        assert magazine.id == sample_magazine.id
        assert magazine.name == sample_magazine.name

    def test_title_validation(self):
        # Test empty title
        with pytest.raises(ValueError):
            Article("", 1, 1)
            
        # Test short title
        with pytest.raises(ValueError):
            Article("Test", 1, 1)
            
        # Test non-string title
        with pytest.raises(ValueError):
            Article(12345, 1, 1)

    def test_foreign_key_constraints(self):
        # Test invalid author_id
        with pytest.raises(Exception):
            Article("Invalid Author", 999, 1).save()
            
        # Test invalid magazine_id
        with pytest.raises(Exception):
            Article("Invalid Magazine", 1, 999).save()