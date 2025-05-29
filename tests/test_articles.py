import pytest
from lib.models.article import Article
from lib.db.seed import seed_database

@pytest.fixture
def setup_db():
    seed_database()

def test_article_creation(setup_db):
    article = Article("Test Article", 1, 1)
    article.save()
    assert article.id is not None

def test_find_by_title(setup_db):
    article = Article.find_by_title("AI Transforming the World")
    assert article is not None
    assert article.title == "AI Transforming the World"

def test_article_relationships(setup_db):
    article = Article.find_by_title("AI Transforming the World")
    assert article.author() is not None
    assert article.magazine() is not None