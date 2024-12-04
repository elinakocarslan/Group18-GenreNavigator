import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
url = 'http://localhost:8501'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url,
        scope='user-top-read'
    )
)

st.set_page_config(page_title='PlaceHolder Name')
st.title('blah blah blah')
st.write('hello hello hello')

# Fetch top tracks
topTracks = sp.current_user_top_tracks(limit=20, time_range='short_term')
trackIds = [track['id'] for track in topTracks['items']]

# Validate track IDs
if not trackIds:
    st.error("No top tracks found. Please ensure your Spotify account has sufficient listening history.")
else:
    try:
        # Create dataframe
        df['track_name'] = [track['name'] for track in topTracks['items']]
        df = df[['track_name', 'danceability', 'energy', 'valence']]
        df.set_index('track_name', inplace=True)

        # Display bar chart
        st.subheader('Spotify Song Suggester')
        st.bar_chart(df, height=500)
    except Exception as e:
        st.error(f"An error occurred while fetching audio features: {e}")
