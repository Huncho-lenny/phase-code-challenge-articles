from lib.models import Author, Magazine, Article
from lib.db.seed import seed_database
from lib.db.connection import get_connection

def run_queries():

    seed_database()
    
    print("=== Running Example Queries ===")
    

    author = Author.find_by_name("John Doe")
    if author:
        print(f"\nArticles by {author.name}:")
        for article in author.articles():
            print(f"- {article['title']}")


    if author:
        print(f"\nMagazines {author.name} has contributed to:")
        for magazine in author.magazines():
            print(f"- {magazine['name']}")

if __name__ == '__main__':
    run_queries()
