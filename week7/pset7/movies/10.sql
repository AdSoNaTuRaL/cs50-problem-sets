SELECT name FROM people p
JOIN directors d ON d.person_id = p.id
JOIN ratings r ON m.id = r.movie_id 
JOIN movies m ON d.movie_id = m.id
WHERE r.rating >= 9.0;