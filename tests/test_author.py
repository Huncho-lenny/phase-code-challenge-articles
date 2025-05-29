import pytest
from lib.models.author import Author
from lib.db.seed import seed_database
from lib.db.connection import get_connection

@pytest.fixture
def setup_db():
    seed_database()

def test_author_creation(setup_db):
    author = Author("Test Author")
    author.save()
    assert author.id is not None

def test_find_by_name(setup_db):
    author = Author.find_by_name("Alice Johnson")
    assert author is not None
    assert author.name == "Alice Johnson"

def test_author_articles(setup_db):
    author = Author.find_by_name("Alice Johnson")
    articles = author.articles()
    assert len(articles) >= 1