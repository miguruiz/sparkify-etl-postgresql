# Note: All constraints have been removed for debugging purposes.


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
    level VARCHAR NOT NULL
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR PRIMARY KEY, 
    name VARCHAR NOT NULL, 
    location VARCHAR, 
    latitude VARCHAR, 
    longitude VARCHAR
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR PRIMARY KEY, 
    title VARCHAR NOT NULL, 
    artist_id VARCHAR, 
    year INTEGER, 
    duration INTEGER,
    CONSTRAINT fk_artist_id
        FOREIGN KEY(artist_id) 
        REFERENCES artists(artist_id)
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

# PREPARED STATEMENTS
songplays_statement = ("""
    PREPARE songplays_statement (TIMESTAMP, INT, VARCHAR, VARCHAR, VARCHAR, INT, VARCHAR, VARCHAR) AS
    INSERT INTO songplays (start_time,user_id, level, song_id, artist_id, session_id, location, user_agent ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
""")

song_statement = ("""
    PREPARE song_statement (VARCHAR, VARCHAR, VARCHAR, INT, INT) AS
    INSERT INTO songs VALUES ($1, $2, $3, $4, $5) ON CONFLICT DO NOTHING;
""")

artist_statement = ("""
    PREPARE artist_statement (VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR) AS
    INSERT INTO artists VALUES ($1, $2, $3, $4, $5) ON CONFLICT DO NOTHING;
""")

user_statement = ("""
    PREPARE user_statement (INT, VARCHAR, VARCHAR, VARCHAR, VARCHAR) AS
    INSERT INTO users (user_id,first_name, last_name, gender, level ) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (user_id) DO UPDATE SET (level) = ($5);
""")
 


# INSERT RECORDS
songplay_table_insert = ("EXECUTE songplays_statement (%s, %s, %s, %s, %s, %s, %s, %s);")
    
song_table_insert = ("EXECUTE song_statement (%s, %s, %s, %s, %s);")

artist_table_insert = ("EXECUTE artist_statement (%s, %s, %s, %s, %s);")

user_table_insert = ("EXECUTE user_statement (%s, %s, %s, %s, %s);")

time_table_insert = "time"


# FIND SONGS

song_select = ( """
    SELECT s.song_id, a.artist_id 
    FROM songs s
    INNER JOIN artists a
    ON a.artist_id = s.artist_id
    WHERE
        s.title = %s AND
        a.name = %s AND
        s.duration = ROUND(%s)
    """)




# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, artist_table_create, song_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
prepared_statements = [songplays_statement, song_statement, artist_statement, user_statement]
