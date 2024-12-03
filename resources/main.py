import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
url = 'http://localhost:3000'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url,
        scope='user-top-read'
    )
)


st.set_page_config(page_title = 'PlaceHolder Name', page_icon='🎧')
st.title('blah blah blah')
st.write('hello hello hello')
topTracks = sp.current_user_top_tracks(limit=50, time_range='medium_term')
trackIds = [track['id'] for track in topTracks['items']]
audio_features = sp.audio_features(trackIds)

df = pd.DataFrame(audio_features)
df['track_name'] = [track['name'] for track in topTracks['items']]
df = df[['track_name', 'danceability', 'energy', 'valence']]
df.set_index('track_name', inplace=True)

st.subheader('Audio Features for Top Tracks')
st.bar_chart(df, height=1000)
