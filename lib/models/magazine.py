from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id = None):
      self.id = id
      self.name = name
      self.category = category
    
    def save (self):
       conn = get_connection()
       cursor = conn.cursor()

       if self.id:
          cursor.execute(
             "UPDATE magazines SET name = ? category = ? WHERE id = ?",
                (self.name, self.category, self.id)
          )

       else:
          cursor.execute(
              "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
       self.id = cursor.lastrowid

       conn.commit()
       conn.close()

    def articles(self):
        """Returns all articles in this magazine"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE magazine_id = ?",
            (self.id,)
        )
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributing_authors(self):
        """Returns authors with >2 articles (Deliverable requirement)"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT authors.* FROM authors
                JOIN articles ON authors.id=articles.author_id
                WHERE articles.magazine_id=?
                GROUP BY authors.id
                HAVING COUNT(articles.id) > 2""",
                (self.id,)
            )
            return cursor.fetchall()
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        """Finds magazine by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM magazines WHERE id = ?",
            (id,)
        )
        row = cursor.fetchone()
        conn.close()
        return cls(**row) if row else None
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls(**row) if row else None


    @classmethod
    def all(cls):
        """Returns all magazines"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines")
        magazines = [cls(**row) for row in cursor.fetchall()]
        conn.close()
        return magazines

    ...