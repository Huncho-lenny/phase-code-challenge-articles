from .base_model import BaseModel

class Article(BaseModel):
    def __init__(self, title, author_id, magazine_id):
        self._validate(title)
        self.title = title.strip()
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.id = None

    def _validate(self, title):
        if not isinstance(title, str) or len(title.strip()) < 5:
            raise ValueError("Title must be at least 5 characters")

    def save(self):
        query = """
            INSERT INTO articles (title, author_id, magazine_id)
            VALUES (?, ?, ?)
            RETURNING id
        """
        result = self._execute(
            query, 
            (self.title, self.author_id, self.magazine_id),
            fetch=True
        )
        self.id = result[0][0]
        return self

    @classmethod
    def find_by_author(cls, author_id):
        query = "SELECT * FROM articles WHERE author_id = ?"
        results = cls._execute(query, (author_id,), fetch=True)
        return [cls._create_instance(row) for row in results]