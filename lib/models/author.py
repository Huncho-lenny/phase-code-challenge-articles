from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id = None):
      self.id = id
      self.name = name
    
    def save (self):
       conn = get_connection()
       cursor = conn.cursor()

       if self.id:
          cursor.execute(
             "UPDATE authors SET name = ? WHERE id = ?",
                (self.name, self.id)
          )

       else:
          cursor.execute(
              "INSERT INTO authors (name) VALUES (?)",
                (self.name,)
            )
       self.id = cursor.lastrowid

       conn.commit()
       conn.close()

    def articles(self):
       """Returns all articles by this author"""
       conn = get_connection()
       cursor = conn.cursor()
       cursor.execute(
            "SELECT * FROM articles WHERE author_id = ?",
            (self.id,)
        )
       articles = cursor.fetchall()
       conn.close()
       return articles
    
    def magazines(self):
        """Returns unique magazines this author has written for"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?""",
            (self.id,)
        )
        magazines = cursor.fetchall()
        conn.close()
        return magazines
    
    @classmethod
    def find_by_id(cls, id):
        """Finds author by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM authors WHERE id = ?",
            (id,)
        )
        row = cursor.fetchone()
        conn.close()
        return cls(**row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
       conn = get_connection()
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
       row = cursor.fetchone()
       conn.close()
       return cls(**row) if row else None


    @classmethod
    def all(cls):
        """Returns all authors"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        authors = [cls(**row) for row in cursor.fetchall()]
        conn.close()
        return authors
    
          