from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Funcție pentru conexiunea la baza de date
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="HotelManagement"
    )

# ------------------ ROUTE: Pagina principală ------------------

@app.route("/")
def index():
    """Pagina principală."""
    return render_template("index.html")

# ------------------ ROUTE: Hotels ------------------

@app.route("/hotels")
def hotels():
    """Pagina pentru gestionarea hotelurilor."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Hotels")
    hotels = cursor.fetchall()
    connection.close()
    return render_template("hotels.html", hotels=hotels)

@app.route("/add-hotel", methods=["GET", "POST"])
def add_hotel():
    """Adaugă un hotel nou."""
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        rating = request.form["rating"]

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Hotels (name, address, rating) VALUES (%s, %s, %s)",
            (name, address, rating)
        )
        connection.commit()
        connection.close()
        return redirect(url_for("hotels"))

    return render_template("form.html", table="Hotel", action="Add")

@app.route("/edit-hotel/<int:hotel_id>", methods=["GET", "POST"])
def edit_hotel(hotel_id):
    """Editează un hotel existent."""
    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        rating = request.form["rating"]

        cursor.execute(
            "UPDATE Hotels SET name = %s, address = %s, rating = %s WHERE id = %s",
            (name, address, rating, hotel_id)
        )
        connection.commit()
        connection.close()
        return redirect(url_for("hotels"))

    cursor.execute("SELECT * FROM Hotels WHERE id = %s", (hotel_id,))
    hotel = cursor.fetchone()
    connection.close()
    return render_template("form.html", table="Hotel", action="Edit", data=hotel)

@app.route("/delete-hotel/<int:hotel_id>")
def delete_hotel(hotel_id):
    """Șterge un hotel."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Hotels WHERE id = %s", (hotel_id,))
    connection.commit()
    connection.close()
    return redirect(url_for("hotels"))

# ------------------ ROUTE: Rooms ------------------

@app.route("/rooms")
def rooms():
    """Pagina pentru gestionarea camerelor."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Rooms")
    rooms = cursor.fetchall()
    connection.close()
    return render_template("rooms.html", rooms=rooms)

@app.route("/add-room", methods=["GET", "POST"])
def add_room():
    """Adaugă o cameră nouă."""
    if request.method == "POST":
        room_number = request.form["room_number"]
        room_type = request.form["type"]
        price = request.form["price"]

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Rooms (room_number, type, price) VALUES (%s, %s, %s)",
            (room_number, room_type, price)
        )
        connection.commit()
        connection.close()
        return redirect(url_for("rooms"))

    return render_template("form.html", table="Room", action="Add")

@app.route("/edit-room/<int:room_id>", methods=["GET", "POST"])
def edit_room(room_id):
    """Editează o cameră existentă."""
    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        room_number = request.form["room_number"]
        room_type = request.form["type"]
        price = request.form["price"]

        cursor.execute(
            "UPDATE Rooms SET room_number = %s, type = %s, price = %s WHERE id = %s",
            (room_number, room_type, price, room_id)
        )
        connection.commit()
        connection.close()
        return redirect(url_for("rooms"))

    cursor.execute("SELECT * FROM Rooms WHERE id = %s", (room_id,))
    room = cursor.fetchone()
    connection.close()
    return render_template("form.html", table="Room", action="Edit", data=room)

@app.route("/delete-room/<int:room_id>")
def delete_room(room_id):
    """Șterge o cameră."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Rooms WHERE id = %s", (room_id,))
    connection.commit()
    connection.close()
    return redirect(url_for("rooms"))

# ------------------ ROUTE: Bookings ------------------

@app.route("/bookings")
def bookings():
    """Pagina pentru gestionarea rezervărilor."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT hr.id, h.name AS hotel_name, r.room_number AS room_number, 
               hr.availability_status, hr.start_date, hr.end_date
        FROM HotelRoom hr
        JOIN Hotels h ON hr.hotel_id = h.id
        JOIN Rooms r ON hr.room_id = r.id
    """)
    bookings = cursor.fetchall()
    connection.close()
    return render_template("bookings.html", bookings=bookings)

@app.route("/make-reservation", methods=["GET", "POST"])
def make_reservation():
    """Adaugă o rezervare nouă."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name FROM Hotels")
    hotels = cursor.fetchall()

    cursor.execute("SELECT id, room_number FROM Rooms")
    rooms = cursor.fetchall()

    if request.method == "POST":
        hotel_id = request.form["hotel_id"]
        room_id = request.form["room_id"]
        status = request.form["status"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        cursor.execute("""
            INSERT INTO HotelRoom (hotel_id, room_id, availability_status, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (hotel_id, room_id, status, start_date, end_date))
        connection.commit()
        connection.close()
        return redirect(url_for("bookings"))

    connection.close()
    return render_template("booking_form.html", action="Make a Reservation", hotels=hotels, rooms=rooms)

@app.route("/edit-reservation/<int:booking_id>", methods=["GET", "POST"])
def edit_reservation(booking_id):
    """Editează o rezervare existentă."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name FROM Hotels")
    hotels = cursor.fetchall()

    cursor.execute("SELECT id, room_number FROM Rooms")
    rooms = cursor.fetchall()

    if request.method == "POST":
        hotel_id = request.form["hotel_id"]
        room_id = request.form["room_id"]
        status = request.form["status"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        cursor.execute("""
            UPDATE HotelRoom 
            SET hotel_id = %s, room_id = %s, availability_status = %s, start_date = %s, end_date = %s
            WHERE id = %s
        """, (hotel_id, room_id, status, start_date, end_date, booking_id))
        connection.commit()
        connection.close()
        return redirect(url_for("bookings"))

    cursor.execute("SELECT * FROM HotelRoom WHERE id = %s", (booking_id,))
    booking = cursor.fetchone()
    connection.close()
    return render_template("booking_form.html", action="Edit Reservation", hotels=hotels, rooms=rooms, booking=booking)

@app.route("/cancel-reservation/<int:booking_id>")
def cancel_reservation(booking_id):
    """Șterge o rezervare."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM HotelRoom WHERE id = %s", (booking_id,))
    connection.commit()
    connection.close()
    return redirect(url_for("bookings"))

# ------------------ RUN APP ------------------

if __name__ == "__main__":
    app.run(debug=True)
