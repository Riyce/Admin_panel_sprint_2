CREATE DATABASE ugc_data ON CLUSTER company_cluster;

CREATE TABLE IF NOT EXISTS ugc_data.user_movie_progress ON CLUSTER company_cluster (
    user_id    String,
    movie_id   String,
    time       UInt16,
    percent    Float32,
    event_time DateTime
)
ENGINE = ReplacingMergeTree(percent)
PARTITION BY toYYYYMM(event_time)
ORDER BY (user_id, movie_id);