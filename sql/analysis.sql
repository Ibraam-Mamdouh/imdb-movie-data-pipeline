use movie_intelligence_db

SELECT COUNT(*) AS movie_count
FROM Movies;

SELECT COUNT(*) AS director_count
FROM Directors;

SELECT COUNT(*) AS actor_count
FROM Actors;

SELECT COUNT(*) AS genre_count
FROM Genres;

SELECT COUNT(*) AS movie_actor_count
FROM Movie_Actors;

SELECT COUNT(*) AS movie_genre_count
FROM Movie_Genres;

SELECT m.*
FROM Movies m
LEFT JOIN Directors d
    ON m.director_id = d.director_id
WHERE d.director_id IS NULL;

SELECT mg.*
FROM Movie_Genres mg
LEFT JOIN Movies m
    ON mg.movie_id = m.movie_id
LEFT JOIN Genres g
    ON mg.genre_id = g.genre_id
WHERE m.movie_id IS NULL
   OR g.genre_id IS NULL;

SELECT ma.*
FROM Movie_Actors ma
LEFT JOIN Movies m
    ON ma.movie_id = m.movie_id
LEFT JOIN Actors a
    ON ma.actor_id = a.actor_id
WHERE m.movie_id IS NULL
   OR a.actor_id IS NULL;

select top 10
		title,
		movie_year,
		rating,
		votes
from Movies
order by rating desc , votes desc;

select d.dir_name As Director,
		count(*) As Movie_count,
		AVG(m.rating) As Average_Rating
from Movies m
left join Directors d
			on m.director_id = d.director_id
group by (d.dir_name)
order by Average_Rating desc ;

select top 10
		a.act_name as actor,
		COUNT(*) as movie_count
from Movie_Actors ma
join Actors a
on ma.actor_id = a.actor_id
group by a.act_name
order by movie_count desc;

select top 10
		g.gen_name as genre,
		COUNT(*) as genre_count
from Movie_Genres as mg
join Genres g
on mg.genre_id = g.genre_id
group by g.gen_name
order by genre_count desc;

