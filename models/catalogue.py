from db import conn, cursor
from models.genre import Genre

class Catalogue:
    TABLE_NAME = "catalogues"

    def __init__(self, name, description, image, booking_fee, author, genre_id, date_published, is_booked = False):
        self.id = None
        self.name = name
        self.description = description
        self.image = image
        self.booking_fee = booking_fee
        self.author = author
        self.genre_id = genre_id
        self.date_published = date_published
        self.is_booked = is_booked
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

    def update(self):
        sql = f"""
            UPDATE {self.TABLE_NAME}
            SET name = ?, description = ?, image = ?, booking_fee = ?, author = ?, genre_id = ?, date_published = ?, is_booked = ?
            WHERE id = ?
        """
        cursor.execute(sql, (self.name, self.description, self.image, self.booking_fee, self.author, self.genre_id, self.date_published, self.is_booked, self.id))
        conn.commit()

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
            "is_booked": self.is_booked,
            "created_at": self.created_at
        }

    @classmethod
    def find_one(cls, id):
        sql = """
            SELECT catalogues.*, genres.* FROM catalogues
            LEFT JOIN genres ON catalogues.genre_id = genres.id
            WHERE catalogues.id = ?
        """

        row = cursor.execute(sql, (id,)).fetchone()

        return cls.row_to_instance(row)

    @classmethod
    def find_all(cls):
        sql = """
            SELECT catalogues.*, genres.* FROM catalogues
            LEFT JOIN genres ON catalogues.genre_id = genres.id
            ORDER BY catalogues.created_at ASC
        """

        rows = cursor.execute(sql).fetchall()

        return [
            cls.row_to_instance(row).to_dict() for row in rows
        ]

    @classmethod
    def row_to_instance(cls, row):
        if row == None:
            return None

        is_booked = False

        if row[9] == 1:
            is_booked = True

        catalogue = cls(row[1], row[2], row[3], row[4], row[5], row[6], row[7], is_booked)
        catalogue.id = row[0]
        catalogue.created_at = row[8]

        genre = Genre(row[11])
        genre.id = row[10]

        catalogue.genre = genre.to_dict()

        return catalogue

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

    # run this only once
    @classmethod
    def alter_table(cls):
        sql = f"""ALTER TABLE {cls.TABLE_NAME} ADD COLUMN is_booked BOOLEAN DEFAULT false"""
        cursor.execute(sql)
        conn.commit()
        print("Table altered")

Catalogue.create_table()
