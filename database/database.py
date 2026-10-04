import sqlite3


DATABASE_NAME = "BM.db"


def connect_db():
    return sqlite3.connect(DATABASE_NAME)


def create_db():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS booking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
        )
    """)

    connection.commit()
    connection.close()


def add_booking(name, phone, date, time):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO booking
        (name, phone, date, time, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        phone,
        date,
        time,
        "pending"
    ))

    connection.commit()
    connection.close()


def booking_exists(date, time):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1
        FROM booking
        WHERE date = ? AND time = ?
        AND status != 'deleted'
        LIMIT 1
    """, (date, time))

    exists = cursor.fetchone() is not None

    connection.close()

    return exists


def get_bookings():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM booking
        WHERE status != 'deleted'
        ORDER BY date, time
    """)

    bookings = cursor.fetchall()

    connection.close()

    return bookings


def confirm_booking(booking_id):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE booking
        SET status = 'confirmed'
        WHERE id = ?
    """, (booking_id,))

    connection.commit()
    connection.close()


def delete_booking(booking_id):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM booking
        WHERE id = ?
    """, (booking_id,))

    connection.commit()
    connection.close()


if __name__ == "__main__":

    create_db()

    print("Database Created")