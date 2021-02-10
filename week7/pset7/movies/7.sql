SELECT m.title, r.rating FROM movies m
JOIN ratings r ON r.movie_id = m.id
WHERE m.year = 2010 AND r.rating IS NOT NULL AND r.rating != ""
ORDER BY r.rating DESC, m.title ASC;