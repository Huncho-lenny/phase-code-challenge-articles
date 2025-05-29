import pytest
from lib.models.magazine import Magazine
from lib.db.seed import seed_database

@pytest.fixture
def setup_db():
    seed_database()

def test_magazine_creation(setup_db):
    magazine = Magazine("Test Mag", "Test Category")
    magazine.save()
    assert magazine.id is not None

def test_find_by_name(setup_db):
    magazine = Magazine.find_by_name("Tech Today")
    assert magazine is not None
    assert magazine.name == "Tech Today"

def test_magazine_articles(setup_db):
    magazine = Magazine.find_by_name("Tech Today")
    articles = magazine.articles()
    assert len(articles) >= 1