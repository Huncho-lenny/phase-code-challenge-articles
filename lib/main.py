#!/usr/bin/env python
from lib.db.connection import get_connection
from lib.models import Author, Article, Magazine
from lib.db.seed import seed_database
from lib.db.schema import create_tables

def initialize_database():
    """Initialize database schema and seed data"""
    with get_connection() as conn:
        create_tables(conn)
        seed_database(conn)

def example_usage():
    """Demonstrate core functionality"""
    # Create test data
    author1 = Author("Jane Austen").save()
    author2 = Author("Charles Dickens").save()
    
    magazine1 = Magazine("Literary Review", "Classics").save()
    magazine2 = Magazine("Modern Writers", "Contemporary").save()

    # Add articles
    author1.add_article(magazine1, "Pride and Prejudice Analysis")
    author1.add_article(magazine2, "Modern Classics")
    author2.add_article(magazine1, "Great Expectations Review")

    # Query examples
    print("\nAll articles by Jane Austen:")
    for article in author1.articles():
        print(f"- {article.title}")

    print("\nMagazines Charles Dickens writes for:")
    for magazine in author2.magazines():
        print(f"- {magazine.name} ({magazine.category})")

    print("\nContributors to Literary Review:")
    magazine = Magazine.find_by_name("Literary Review")
    for author in magazine.contributors():
        print(f"- {author.name}")

def main():
    initialize_database()
    example_usage()

if __name__ == "__main__":
    main()