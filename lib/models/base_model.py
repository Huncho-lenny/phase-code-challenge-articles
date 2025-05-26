from lib.db.connection import get_connection

class BaseModel:
    @classmethod
    def _execute(cls, query, params=(), fetch=False):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()
    
    @classmethod
    def _create_instance(cls, row):
        if row:
            instance = cls.__new__(cls)
            # Convert row (tuple) to dict using cursor description if needed
            if isinstance(row, dict):
                instance.__dict__.update(row)
            else:
                # Fallback: assume cls has a _fields attribute listing column names
                if hasattr(cls, '_fields') and len(getattr(cls, '_fields', [])) == len(row):
                    instance.__dict__.update(dict(zip(cls._fields, row)))
                else:
                    raise ValueError("Row is not a dict and _fields attribute is missing or does not match row length in the class.")
            return instance
        return None