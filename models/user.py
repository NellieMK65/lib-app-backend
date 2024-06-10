from db import conn, cursor

class User:
    TABLE_NAME = "users"

    def __init__(self, name, phone):
        self.id = None
        self.name = name
        self.phone = phone

    def save(self):
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (name, phone)
            VALUES (?, ?)
        """
        cursor.execute(sql, (self.name, self.phone))
        conn.commit()
        self.id = cursor.lastrowid

        return self

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone
        }

    @classmethod
    def find_one_by_phone(cls, phone):
        sql = f"""
            SELECT * FROM {cls.TABLE_NAME}
            WHERE phone = ?
        """

        row = cursor.execute(sql, (phone,)).fetchone()

        return cls.row_to_instance(row)

    @classmethod
    def row_to_instance(cls, row):
        if row == None:
            return None

        user = cls(row[1], row[2])
        user.id = row[0]

        return user

    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE
            )
        """
        cursor.execute(sql)
        conn.commit()
        print("Users table created")

User.create_table()
