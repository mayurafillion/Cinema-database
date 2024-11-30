import sqlite3

# Connect to the existing SQLite database
conn = sqlite3.connect('cinema.db')
cursor = conn.cursor()


def print_table(rows, headers):
    col_widths = [max(len(str(value)) for value in col) for col in zip(*rows, headers)]

    # Print headers
    header_row = " | ".join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))
    print("-" * len(header_row))
    print(header_row)
    print("-" * len(header_row))

    # Print rows
    for row in rows:
        print(" | ".join(f"{str(value):<{col_widths[i]}}" for i, value in enumerate(row)))
    print("-" * len(header_row))


def management_interface():
    while True:
        print("\n--- Management Interface ---")
        print("1. User Management")
        print("2. Showtime Management")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user_management()
        elif choice == '2':
            showtime_management()
        elif choice == '3':
            print("Exiting management interface.")
            break
        else:
            print("Invalid choice. Please select again.")


def user_management():
    while True:
        print("\n--- User Management ---")
        print("1. Users Management")
        print("2. Bookings Management")
        print("3. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            usersMenu()
        elif choice == '2':
            bookingsMenu()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select again.")


def usersMenu():
    while True:
        print("\n--- Users Management ---")
        print("1. View")
        print("2. Add")
        print("3. Delete")
        print("4. Go back to User Management Menu")
        usersChoice = input("Enter your choice: ")

        if usersChoice == '1':
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            headers = ["UserID", "Username", "Email"]
            print("\n--- Users ---")
            if users:
                print_table(users, headers)
            else:
                print("No users found.")

        elif usersChoice == '2':
            username = input("Enter username: ")
            email = input("Enter email: ")
            cursor.execute("INSERT INTO users (user_name, email) VALUES (?, ?)", (username, email))
            conn.commit()
            print(f"User {username} added successfully.")

        elif usersChoice == '3':
            user_id = input("Enter the UserID to delete: ")
            cursor.execute("DELETE FROM users WHERE userID = ?", (user_id,))
            conn.commit()
            print(f"User {user_id} deleted successfully.")

        elif usersChoice == '4':
            break

        else:
            print("Invalid choice. Please select again.")


def bookingsMenu():
    while True:
        print("\n--- Bookings Management ---")
        print("1. View All Bookings")
        print("2. View Bookings for a Specific User")
        print("3. Add")
        print("4. Delete")
        print("5. Go back to User Management Menu")
        bookingsChoice = input("Enter your choice: ")

        if bookingsChoice == '1':
            cursor.execute("""
                SELECT b.bookingID, u.user_name, m.movie_title, s.start_time, b.num_seats
                FROM bookings b
                JOIN users u ON b.userID = u.userID
                JOIN showtimes s ON b.showtimeID = s.showtimeID
                JOIN movies m ON s.movieID = m.movieID
            """)
            bookings = cursor.fetchall()
            headers = ["BookingID", "User", "Movie", "Start Time", "Seats"]
            print("\n--- Bookings ---")
            if bookings:
                print_table(bookings, headers)
            else:
                print("No bookings found.")

        elif bookingsChoice == '2':
            user_id = input("Enter the UserID: ")
            cursor.execute("SELECT user_name FROM users WHERE userID = ?", (user_id,))
            user_data = cursor.fetchone()

            if user_data:
                username = user_data[0]
                cursor.execute("""
                    SELECT b.bookingID, m.movie_title, s.start_time, b.num_seats
                    FROM bookings b
                    JOIN showtimes s ON b.showtimeID = s.showtimeID
                    JOIN movies m ON s.movieID = m.movieID
                    WHERE b.userID = ?
                """, (user_id,))
                bookings = cursor.fetchall()
                headers = ["BookingID", "Movie", "Start Time", "Seats"]
                if bookings:
                    print(f"\n--- Bookings for User {user_id} : {username} ---")
                    print_table(bookings, headers)
                else:
                    print(f"No bookings found for User {user_id} : {username}.")
            else:
                print(f"No user found with UserID {user_id}.")

        elif bookingsChoice == '3':
            user_id = input("Enter UserID: ")
            cursor.execute("SELECT user_name FROM users WHERE userID = ?", (user_id,))
            user_data = cursor.fetchone()
            if not user_data:
                print(f"No user found with UserID {user_id}. Please add the user first.")
                continue
            showtime_id = input("Enter ShowtimeID: ")
            cursor.execute("SELECT * FROM showtimes WHERE showtimeID = ?", (showtime_id,))
            showtime_data = cursor.fetchone()
            if not showtime_data:
                print(f"No showtime found with ShowtimeID {showtime_id}.")
                continue
            num_seats = input("Enter number of seats: ")
            cursor.execute("""
                INSERT INTO bookings (userID, showtimeID, num_seats)
                VALUES (?, ?, ?)
            """, (user_id, showtime_id, num_seats))
            conn.commit()
            print("Booking added successfully.")

        elif bookingsChoice == '4':
            booking_id = input("Enter the BookingID to delete: ")
            cursor.execute("DELETE FROM bookings WHERE bookingID = ?", (booking_id,))
            conn.commit()
            print(f"BookingID {booking_id} deleted successfully.")

        elif bookingsChoice == '5':
            break

        else:
            print("Invalid choice. Please select again.")


def showtime_management():
    while True:
        print("\n--- Showtime Management ---")
        print("1. Cinemas management")
        print("2. Theaters management")
        print("3. Movies management")
        print("4. Showtimes management")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            cinemasMenu()

        elif choice == '2':
            theatersMenu()

        elif choice == '3':
            moviesMenu()

        elif choice == '4':
            showtimesMenu()

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please select again.")


def cinemasMenu():
    while True:
        print("\n--- Cinemas Management ---")
        print("1. View")
        print("2. Add")
        print("3. Delete")
        print("4. Back to Showtime Management Menu")
        cinema_choice = input("Enter your choice: ")

        if cinema_choice == '1':
            cursor.execute("SELECT * FROM cinemas")
            cinemas = cursor.fetchall()
            headers = ["CinemaID", "Cinema Name", "Location"]
            print("\n--- Cinemas ---")
            if cinemas:
                print_table(cinemas, headers)
            else:
                print("No cinemas found.")
        elif cinema_choice == '2':
            cinema_name = input("Enter cinema name: ")
            location = input("Enter location: ")
            cursor.execute("INSERT INTO cinemas (cinema_name, location) VALUES (?, ?)", (cinema_name, location))
            conn.commit()
            print("Cinema added successfully.")
        elif cinema_choice == '3':
            cinemaID = input("Enter CinemaID: ")
            cursor.execute("DELETE FROM cinemas WHERE id = ?", (cinemaID,))
            conn.commit()
            print("Cinema deleted successfully.")
        elif cinema_choice == '4':
            break
        else:
            print("Invalid choice. Please select again.")


def theatersMenu():
    while True:
        print("\n--- Theaters Management ---")
        print("1. View")
        print("2. Add")
        print("3. Delete")
        print("4. Back to Showtime Management Menu")
        theater_choice = input("Enter your choice: ")

        if theater_choice == '1':
            cursor.execute("SELECT * FROM theaters")
            theaters = cursor.fetchall()
            headers = ["TheaterID", "CinemaID", "Theater Name", "Screen Type", "Capacity"]
            print("\n--- Theaters ---")
            if theaters:
                print_table(theaters, headers)
            else:
                print("No theaters found.")
        elif theater_choice == '2':
            cinemaID = input("Enter CinemaID: ")
            theater_name = input("Enter theater name: ")
            screentype = input("Enter screen type: ")
            capacity = input("Enter capacity: ")

            cursor.execute("""
                INSERT INTO theaters (cinemaID, screentype, capacity, theater_name)
                VALUES (?, ?, ?, ?)
            """, (cinemaID, screentype, capacity, theater_name))
            conn.commit()
            print("Theater added successfully.")
        elif theater_choice == '3':
            theaterID = input("Enter TheaterID: ")
            cursor.execute("DELETE FROM theaters WHERE id = ?", (theaterID,))
            conn.commit()
            print("Theater deleted successfully.")
        elif theater_choice == '4':
            break
        else:
            print("Invalid choice. Please select again.")


def moviesMenu():
    while True:
        print("\n--- Movies Management ---")
        print("1. View")
        print("2. Add")
        print("3. Delete")
        print("4. Back to Showtime Management Menu")
        movie_choice = input("Enter your choice: ")

        if movie_choice == '1':
            cursor.execute("SELECT * FROM movies")
            movies = cursor.fetchall()
            headers = ["MovieID", "Title", "Genre", "Runtime", "Release Date"]
            print("\n--- Movies ---")
            if movies:
                print_table(movies, headers)
            else:
                print("No movies found.")
        elif movie_choice == '2':
            movie_title = input("Enter movie title: ")
            genre = input("Enter genre: ")
            runtime = input("Enter runtime (in minutes): ")
            release_date = input("Enter release date (YYYY-MM-DD): ")
            cursor.execute("""
                INSERT INTO movies (movie_title, genre, runtime, release_date)
                VALUES (?, ?, ?, ?)
            """, (movie_title, genre, runtime, release_date))
            conn.commit()
            print("Movie added successfully.")
        elif movie_choice == '3':
            movieID = input("Enter MovieID: ")
            cursor.execute("DELETE FROM movies WHERE id = ?", (movieID,))
            conn.commit()
            print("Movie deleted successfully.")
        elif movie_choice == '4':
            break
        else:
            print("Invalid choice. Please select again.")


def showtimesMenu():
    while True:
        print("\n--- Showtimes Management ---")
        print("1. View")
        print("2. Add")
        print("3. Delete")
        print("4. Back to Showtime Management Menu")
        showtime_choice = input("Enter your choice: ")

        if showtime_choice == '1':
            cursor.execute("""
                SELECT s.showtimeID, m.movie_title, t.theater_name, s.start_time
                FROM showtimes s
                JOIN movies m ON s.movieID = m.movieID
                JOIN theaters t ON s.theaterID = t.theaterID
            """)
            showtimes = cursor.fetchall()
            headers = ["ShowtimeID", "Movie", "Theater", "Start Time"]
            print("\n--- Showtimes ---")
            if showtimes:
                print_table(showtimes, headers)
            else:
                print("No showtimes found.")
        elif showtime_choice == '2':
            MovieID = input("Enter MovieID: ")
            TheaterID = input("Enter TheaterID: ")
            start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
            cursor.execute("""
                INSERT INTO showtimes (movieID, theaterID, start_time)
                VALUES (?, ?, ?)
            """, (MovieID, TheaterID, start_time))
            conn.commit()
            print("Showtime scheduled successfully.")
        elif showtime_choice == '3':
            showtimeID = input("Enter ShowtimeID: ")
            cursor.execute("DELETE FROM showtimes WHERE id = ?", (showtimeID,))
            conn.commit()
            print("Showtime deleted successfully.")
        elif showtime_choice == '4':
            break
        else:
            print("Invalid choice. Please select again.")


if __name__ == "__main__":
    management_interface()
    conn.close()
