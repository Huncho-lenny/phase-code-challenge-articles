from .base_model import BaseModel

class Author(BaseModel):
    def __init__(self, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Author name must be a non-empty string")
        self.name = name.strip()
        self.id = None

    def save(self):
        if self.id is None:
            query = "INSERT INTO authors (name) VALUES (?) RETURNING id"
            result = self._execute(query, (self.name,), fetch=True)
            self.id = result[0][0]
        return self

    @classmethod
    def find_by_id(cls, author_id):
        query = "SELECT * FROM authors WHERE id = ?"
        result = cls._execute(query, (author_id,), fetch=True)
        return cls._create_instance(result[0]) if result else None

    def articles(self):
        query = """
            SELECT * FROM articles 
            WHERE author_id = ?
            ORDER BY id DESC
        """
        return [self._create_instance(row) for row in self._execute(query, (self.id,), fetch=True)]

    def magazines(self):
        query = """
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """
        return [self._create_instance(row) for row in self._execute(query, (self.id,), fetch=True)]

    def add_article(self, magazine, title):
        from .article import Article  # Avoid circular import
        return Article(title, self.id, magazine.id).save()