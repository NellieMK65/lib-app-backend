from db import conn, cursor

class Catalogue:
    TABLE_NAME = "catalogues"

    def __init__(self, name, description, image, booking_fee, author, genre_id, date_published):
        self.id = None
        self.name = name
        self.description = description
        self.image = image
        self.booking_fee = booking_fee
        self.author = author
        self.genre_id = genre_id
        self.date_published = date_published
        self.created_at = None
        self.genre = None

    def save(self):
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (name, description, image, booking_fee, author, genre_id, date_published)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (self.name, self.description, self.image, self.booking_fee, self.author, self.genre_id, self.date_published))
        conn.commit()
        self.id = cursor.lastrowid

        return self

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "booking_fee": self.booking_fee,
            "author": self.author,
            "genre": self.genre,
            "date_published": self.date_published,
            "created_at": self.created_at
        }

    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description VARCHAR NOT NULL,
                image VARCHAR NOT NULL,
                booking_fee INTEGER NOT NULL,
                author TEXT NOT NULL,
                genre_id INTEGER NOT NULL REFERENCES genres(id),
                date_published DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        cursor.execute(sql)
        conn.commit()
        print("Catalogue table created successfully")


Catalogue.create_table()
