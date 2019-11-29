CREATE TABLE users(
    username varchar NOT NULL UNIQUE,
    password varchar NOT NULL
);

CREATE TABLE books(
	isbn varchar,
    title varchar,
    author varchar,
    year int,    
    review_count int,
    average_score float
);

CREATE TABLE reviews(
    isbn varchar primary key,
    username varchar primary key,
    review varchar
);

