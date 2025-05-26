from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.connection import get_db_connection

def main():
    conn = get_db_connection()

    author1 = Author(name="Figwan Ting")
    magazine1 = Magazine(name="Tech Flex", category="Technology")
    article1 = Article(title="The Rise of AI", content="AI is changing everything.", author_id=author1.id, magazine_id=magazine1.id)

    author1.save()
    magazine1.save()
    article1.save()

    print(f"Articles by {author1.name}:")
    for article in author1.articles():
        print(f"- {article.title}")

    conn.close()

if __name__ == "__main__":
    main()
