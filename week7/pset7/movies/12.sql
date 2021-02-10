SELECT m.title FROM movies m
JOIN stars s ON s.movie_id = m.id
JOIN people p ON p.id = s.person_id
WHERE p.id IN
(SELECT id FROM people WHERE name = "Johnny Depp" OR name = "Helena Bonham Carter")
GROUP BY s.movie_id
HAVING COUNT(*) > 1;




