import pandas as pd
import random

"""
This function returns songs and their track_name, artist, year and genre.
"""

def filtered_songs():
    all_songs = pd.read_csv("./data/songs.csv")
    all_songs = all_songs.filter(["track_name", "artist", "year", "genre"])
    return all_songs

# Function to load all songs from CSV, including feedback columns
def get_all_songs():
    # Read the song data including likes and dislikes
    all_songs = pd.read_csv("./data/tcc_ceds_music.csv")
    
    # Ensure likes and dislikes columns exist, if not create them
    if 'likes' not in all_songs.columns:
        all_songs['likes'] = 0
    if 'dislikes' not in all_songs.columns:
        all_songs['dislikes'] = 0
    
    return all_songs

# Function to recommend songs based on user feedback (likes/dislikes)
def recommend(input_songs):
    # Load all songs
    songs = get_all_songs()
    
    # Remove songs with count = 1 (filtering as before)
    songs = songs.groupby('genre').filter(lambda x: len(x) > 0)
    
    # Create playlist based on song track names and genre
    playlist = dict(zip(songs['track_name'], songs['genre']))
    
    # Create a frequency dictionary of genres
    freq = {}
    for item in songs['genre']:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1

    # Create a list of all songs from the input genre, excluding already selected ones
    selected_list = []
    output = []
    
    for input in input_songs:
        if input in playlist.keys():
            for key, value in playlist.items():
                if playlist[input] == value:
                    selected_list.append(key)
            selected_list.remove(input)
    
    # Filter out disliked songs and prioritize liked songs
    selected_list = [song for song in selected_list if songs[songs['track_name'] == song]['dislikes'].iloc[0] == 0]
    
    # Sort by the number of likes, with highest liked songs first
    selected_list = sorted(selected_list, key=lambda song: songs[songs['track_name'] == song]['likes'].iloc[0], reverse=True)
    
    if len(selected_list) >= 10:
        output = random.sample(selected_list, 10)
    else:
        extra_songs = 10 - len(selected_list)
        song_names = songs['track_name'].to_list()
        song_names_filtered = [x for x in song_names if x not in selected_list]
        selected_list.extend(random.sample(song_names_filtered, extra_songs))
        output = selected_list.copy()
    
    return output
