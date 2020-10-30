# PENDING:
    # Categorical data
    # SERIAL IDs
    # on conflict
    # PREPARED STATEMENTS FOR THE INSERTS


# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id SERIAL PRIMARY KEY, 
    start_time TIMESTAMP, 
    user_id INT, 
    level VARCHAR, 
    song_id VARCHAR, 
    artist_id VARCHAR, 
    session_id INT, 
    location VARCHAR, 
    user_agent VARCHAR
)
""")


user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY, 
    first_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR,
    level VARCHAR
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR PRIMARY KEY, 
    title VARCHAR, 
    artist_id VARCHAR, 
    year INTEGER, 
    duration INTEGER
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR PRIMARY KEY, 
    name VARCHAR, 
    location VARCHAR, 
    latitude VARCHAR, 
    longitude VARCHAR
)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP PRIMARY KEY, 
    hour INTEGER, 
    day INTEGER, 
    week INTEGER, 
    month INTEGER, 
    year INTEGER, 
    weekday INTEGER
)
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (start_time,user_id, level, song_id, artist_id, session_id, location, user_agent ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
""")
    
song_table_insert = ("""
INSERT INTO songs VALUES (%s, %s, %s, %s, %s)ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists VALUES (%s, %s, %s, %s, %s)ON CONFLICT DO NOTHING;
""")


time_table_insert = ("""
INSERT INTO time VALUES (%s, %s, %s, %s, %s, %s, %s)ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, a.artist_id 
FROM songs s
LEFT JOIN artists a
ON a.artist_id = s.artist_id
WHERE
    s.title LIKE %s AND
    a.name LIKE %s AND
    s.duration = %s
""")


# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]