from .base_model import BaseModel

class Magazine(BaseModel):
    def __init__(self, name, category):
        self._validate(name, category)
        self.name = name.strip()
        self.category = category.strip()
        self.id = None

    def _validate(self, name, category):
        if not isinstance(name, str) or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        if not isinstance(category, str) or len(category.strip()) == 0:
            raise ValueError("Category must be a non-empty string")

    def save(self):
        query = """
            INSERT INTO magazines (name, category) 
            VALUES (?, ?) 
            RETURNING id
        """
        result = self._execute(query, (self.name, self.category), fetch=True)
        self.id = result[0][0]
        return self

    def articles(self):
        query = "SELECT * FROM articles WHERE magazine_id = ?"
        return [self._create_instance(row) for row in self._execute(query, (self.id,), fetch=True)]

    def contributors(self):
        query = """
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """
        return [self._create_instance(row) for row in self._execute(query, (self.id,), fetch=True)]

    @classmethod
    def find_by_category(cls, category):
        query = "SELECT * FROM magazines WHERE category = ?"
        results = cls._execute(query, (category,), fetch=True)
        return [cls._create_instance(row) for row in results]