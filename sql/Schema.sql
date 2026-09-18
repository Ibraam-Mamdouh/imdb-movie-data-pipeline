create database movie_intelligence_db

use movie_intelligence_db

create table Directors (
	director_id int primary key,
	dir_name nvarchar(100)
);

create table Movies (
	movie_id int primary key,
	director_id int,
	foreign key (director_id) references Directors(director_id),
	title nvarchar(150),
	movie_year int,
	rating float,
	votes int,
	runtime_minutes int
)

create table Actors (
	actor_id int primary key,
	act_name nvarchar(100)
)

create table Genres(
	genre_id int primary key,
	gen_name nvarchar(100)
)

create table Movie_Genres(
	movie_id int,
	genre_id int
	primary key (movie_id,genre_id)
	foreign key (movie_id) references Movies(movie_id),
	foreign key (genre_id) references Genres(genre_id)
)

create table Movie_Actors(
	movie_id int,
	actor_id int
	primary key (movie_id,actor_id)
	foreign key (movie_id) references Movies(movie_id),
	foreign key (actor_id) references Actors(actor_id)
)