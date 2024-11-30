PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
-- CREATE TABLE cds(
--       cd_id text primary key not null, --cd unique id
--       title text NOT NULL, --title of CD
--       artist text NOT NULL, --artist whose CD it is or "various artists"
--       producer text default NULL,
--       year integer,
--       contributer text --student number who contirbuted the data
-- );

DROP TABLE IF EXISTS cinemas;
DROP TABLE IF EXISTS theaters;
DROP TABLE IF EXISTS showtimes;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS playing;
DROP TABLE IF EXISTS playingIn;

CREATE TABLE cinemas(
    cinemaID integer primary key autoincrement, --auto incrementing key
    cinema_name text NOT NULL, --name of the cinema 
    location text NOT NULL --cinema location 
);

CREATE TABLE theaters(
    theaterID integer primary key autoincrement, --not incrmenting since there are different cinema which contains theaters
    cinemaID integer not null,
    screentype text NOT NULL, --screen type of a theater 
    capacity integer NOT NULL, --theater capacity (maximum number of seats in the theater)
    theater_name text NOT NULL, --name of the theater
    foreign key (cinemaID) references cinemaID(cinemaID) ON DELETE CASCADE
);

CREATE TABLE showtimes(
    showtimeID integer primary key autoincrement, --auto incrementing key,
    movieID integer not null ,
    theaterID integer NOT NULL,
    start_time text NOT NULL,
    foreign key (movieID) references movies(movieID) ON DELETE CASCADE,
    foreign key (theaterID) references theaters(theaterID) ON DELETE CASCADE
    UNIQUE(theaterID, start_time)
);

CREATE TABLE movies(
    movieID integer primary key autoincrement, --auto incrementing key,
    movie_title text NOT NULL,
    genre text NOT NULL,
    runtime integer NOT NULL,
    release_date text NOT NULL
);


CREATE TABLE users(
    userID integer primary key autoincrement, --auto incrementing key,
    user_name text NOT NULL UNIQUE,
    email text NOT NULL 
);


CREATE TABLE bookings(
    bookingID integer primary key autoincrement, --auto incrementing key,
    userID integer not null, 
    showtimeID integer not null,
    num_seats integer NOT NULL,
    foreign key (userID) references users(userID) ON DELETE CASCADE,
    foreign key (showtimeID) references showtimes(showtimeID) ON DELETE CASCADE
);

-- CREATE TABLE playing(
--     movieID integer not null references movies(movieID) ON DELETE CASCADE,
--     showtimeID integer not null references showtimes(showtimeID) ON DELETE CASCADE,
--     primary key (movieID, showtimeID)
-- );

-- CREATE TABLE playingIn(
--     theaterID integer not null references theaters(theaterID) ON DELETE CASCADE,
--     showtimeID integer not null references showtimes(showtimeID) ON DELETE CASCADE,
--     primary key (theaterID, showtimeID) 
-- );

COMMIT;