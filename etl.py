import os
import io
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def create_insert_statements(cur, conn):
    """
    Creates each prepared insert statement 
    """
    for query in prepared_statements:
        cur.execute(query)
        conn.commit()
        
def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines = True)


    # insert song record
    song_data = df[['song_id','title','artist_id','year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit = 'ms').to_frame()

    
    # insert time data records
    t['hour'] = t['ts'].dt.hour
    t['day'] = t['ts'].dt.day
    t['week'] = t['ts'].dt.week
    t['month'] = t['ts'].dt.month
    t['year'] = t['ts'].dt.year
    t['weekday'] = t['ts'].dt.weekday
    
    time_df = t

    # text buffer
    s_buf = io.StringIO()
    time_df.to_csv(s_buf)

    # insert into time table
    cur.copy_from(s_buf,time_table_insert)

    # load user table
    user_df = df[['userId',"firstName", "lastName", "gender", "level"]].drop_duplicates(subset='userId')
    
    # text buffer
    user_df.to_csv(s_buf)
    
    # insert into time table
    cur.copy_from(s_buf,user_table_insert)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit = 'ms'), int(row.userId), row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    create_insert_statements(cur,conn)    
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()