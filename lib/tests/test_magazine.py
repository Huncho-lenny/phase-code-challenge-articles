import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.connection import get_connection

class TestMagazine:
    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Clean database state before each test"""
        conn = get_connection()
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM magazines")
        conn.execute("DELETE FROM authors")
        conn.commit()
        conn.close()

    @pytest.fixture
    def sample_magazine(self):
        return Magazine("Tech Today", "Technology").save()

    @pytest.fixture
    def sample_author(self):
        return Author("John Techwriter").save()

    def test_magazine_creation(self):
        magazine = Magazine("Science Weekly", "Science")
        assert magazine.name == "Science Weekly"
        assert magazine.category == "Science"
        assert magazine.id is None

    def test_save_magazine(self):
        magazine = Magazine("Business Digest", "Business").save()
        assert magazine.id is not None
        assert isinstance(magazine.id, int)

    def test_find_by_id(self, sample_magazine):
        found = Magazine.find_by_id(sample_magazine.id)
        assert found.id == sample_magazine.id
        assert found.name == sample_magazine.name

    def test_find_by_category(self):
        Magazine("AI Monthly", "Technology").save()
        Magazine("DevOps Weekly", "Technology").save()
        
        tech_mags = Magazine.find_by_category("Technology")
        assert len(tech_mags) == 2
        assert {m.name for m in tech_mags} == {"AI Monthly", "DevOps Weekly"}

    def test_articles_relationship(self, sample_magazine, sample_author):
        sample_author.add_article(sample_magazine, "Python in 2025")
        sample_author.add_article(sample_magazine, "AI Trends")
        
        articles = sample_magazine.articles()
        assert len(articles) == 2
        assert all(isinstance(a, Article) for a in articles)
        assert {a.title for a in articles} == {"Python in 2025", "AI Trends"}

    def test_contributors(self, sample_magazine):
        author1 = Author("Alice Coder").save()
        author2 = Author("Bob Developer").save()
        
        author1.add_article(sample_magazine, "Code Quality")
        author2.add_article(sample_magazine, "System Design")
        author1.add_article(sample_magazine, "Testing Strategies")
        
        contributors = sample_magazine.contributors()
        assert len(contributors) == 2
        assert {c.name for c in contributors} == {"Alice Coder", "Bob Developer"}

    def test_article_titles(self, sample_magazine, sample_author):
        sample_author.add_article(sample_magazine, "Cloud Computing")
        sample_author.add_article(sample_magazine, "Kubernetes Deep Dive")
        
        titles = sample_magazine.article_titles()
        assert len(titles) == 2
        assert "Cloud Computing" in titles
        assert "Kubernetes Deep Dive" in titles

    def test_contributing_authors(self):
        magazine = Magazine("Dev Journal", "Development").save()
        author1 = Author("Senior Dev").save()
        author2 = Author("Junior Dev").save()
        
        # Author1: 3 articles
        author1.add_article(magazine, "Architecture Patterns")
        author1.add_article(magazine, "Scaling Systems")
        author1.add_article(magazine, "Database Optimization")
        
        # Author2: 1 article
        author2.add_article(magazine, "Learning Python")
        
        contributors = magazine.contributing_authors()
        assert len(contributors) == 1
        assert contributors[0].name == "Senior Dev"
        assert contributors[0].id == author1.id

    def test_top_publisher(self):
        mag1 = Magazine("Popular Tech", "General").save()
        mag2 = Magazine("Niche News", "Specialized").save()
        
        # Add 3 articles to mag1, 2 to mag2
        author = Author("Staff Writer").save()
        author.add_article(mag1, "Article 1")
        author.add_article(mag1, "Article 2")
        author.add_article(mag1, "Article 3")
        author.add_article(mag2, "Article A")
        author.add_article(mag2, "Article B")
        
        top_mag = Magazine.top_publisher()
        assert top_mag.id == mag1.id
        assert top_mag.name == "Popular Tech"

    def test_invalid_category(self):
        with pytest.raises(ValueError):
            Magazine("Test Mag", "")  # Empty category
        with pytest.raises(ValueError):
            Magazine("Test Mag", 123)  # Non-string category