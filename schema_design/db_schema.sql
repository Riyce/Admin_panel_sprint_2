-- psql -U postgres /var/lib/postgresql/data/db_schema.sql

-- CREATE DATABASE movies;
\c movies;
CREATE SCHEMA IF NOT EXISTS content;
SET search_path TO content,public;

CREATE TABLE IF NOT EXISTS film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path TEXT,
    rating FLOAT,
    type TEXT not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE INDEX IF NOT EXISTS film_work_idx ON film_work(title);

CREATE TABLE IF NOT EXISTS genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_date DATE,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE INDEX IF NOT EXISTS person_full_name_idx ON person(full_name); 

CREATE TABLE IF NOT EXISTS genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created_at timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON genre_film_work(film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT NOT NULL,
    created_at timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_role_idx ON person_film_work(film_work_id, person_id, role); 
