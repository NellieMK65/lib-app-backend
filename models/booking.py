from db import conn, cursor

class Booking:

    TABLE_NAME = "bookings"

    def __init__(self, booking_from, booking_to, booking_fee, catalogue_id, user_id):
        self.id = None
        self.booking_from = booking_from
        self.booking_to = booking_to
        self.booking_fee = booking_fee
        self.catalogue_id = catalogue_id
        self.user_id = user_id

    def save(self):
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (booking_from, booking_to, booking_fee, catalogue_id, user_id)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (self.booking_from, self.booking_to, self.booking_fee, self.catalogue_id, self.user_id))
        conn.commit()
        self.id = cursor.lastrowid

        return self


    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_from DATE NOT NULL,
                booking_to DATE NOT NULL,
                booking_fee INTEGER NOT NULL,
                catalogue_id INTEGER NOT NULL REFERENCES catalogues (id),
                user_id INTEGER NOT NULL REFERENCES users (id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        cursor.execute(sql)
        conn.commit()
        print("Bookings table created")

Booking.create_table()
