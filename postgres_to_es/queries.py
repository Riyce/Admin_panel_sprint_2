PERSONS_QUERY = """
    SELECT id, updated_at
    FROM content.person
    WHERE updated_at > %s
    ORDER BY updated_at
"""

GENRE_QUERY = """
    SELECT id, updated_at
    FROM content.genre
    WHERE updated_at > %s
    ORDER BY updated_at
"""

GENRE_FULL_QUERY = """
    SELECT id, name, updated_at
    FROM content.genre
    WHERE updated_at > %s
    ORDER BY updated_at
"""

FILM_WORK_QUERY = """
    SELECT id, updated_at
    FROM content.film_work
    WHERE updated_at > %s
    ORDER BY updated_at
"""

ALL_FILM_WORK_QUERY = """
    SELECT id
    FROM content.film_work
"""

ALL_GENRE_QUERY = """
    SELECT id
    FROM content.genre
"""

ALL_PERSONS_QUERY = """
    SELECT id
    FROM content.person
"""

GENRE_ETL_QUERY = """
    SELECT id, name
    FROM content.genre
    WHERE id IN %s; 
"""

PERSON_ETL_QUERY = """
    SELECT p.id, p.full_name, pfw.film_work_id, pfw.role
    FROM content.person p
    LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
    WHERE p.id IN %s; 
"""

PERSON_FILM_WORK_QUERY = """
    SELECT DISTINCT fw.id
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    WHERE pfw.person_id IN %s
"""

GENRE_FILM_WORK_QUERY = """
    SELECT DISTINCT fw.id
    FROM content.film_work fw
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    WHERE gfw.genre_id IN %s
"""

FW_ETL_QUERY = """
    SELECT
        fw.id,
        fw.rating AS imdb_rating,
        g.name AS genre_name,
        g.id AS g_id,
        fw.title, 
        fw.description, 
        pfw.role, 
        p.id AS p_id, 
        p.full_name as name
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE fw.id IN %s; 
"""

