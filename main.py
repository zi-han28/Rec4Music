from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List, Dict, Any
import uvicorn
import json
import os
import base64
import time
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from genius_api import get_lyrics_with_info
from engine import ReccobeatsAPI, valid_recommendations, get_cbf_recommendations_from_favourites
from auth import (
    init_db, create_user, authenticate_user, 
    get_user_favourites, add_to_favourites, 
    remove_from_favourites, is_favourite)

load_dotenv()

app = FastAPI(
    title="Music Recommendation API",
    description="Music recommendation website",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    
os.environ["SPOTIPY_CLIENT_ID"] = client_id
os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8501/callback"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

@app.get("/search")
async def search_tracks(q: str = Query(..., min_length=1)):
    try:
        results = sp.search(q=q, type="track", limit=5)
        tracks = results["tracks"]["items"]
        return {
            "results": [
                {
                    "track_id": track["id"],
                    "track_name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "album_image": track["album"]["images"][1]["url"] if track["album"]["images"] else None,
                    "spotify_url": track["external_urls"]["spotify"],
                    "preview_url": track.get("preview_url")
                }
                for track in tracks
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/track/{track_id}")
async def get_track(track_id: str):
    try:
        track = sp.track(track_id)
        return {
            "track_id": track["id"],
            "track_name": track["name"],
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "album_image": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
            "spotify_url": track["external_urls"]["spotify"],
            "embed_url": f"https://open.spotify.com/embed/track/{track['id']}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/track/{track_id}/lyrics")
async def get_track_lyrics(track_id: str):
    try:
        # First get the track details to get track name and artist
        track = sp.track(track_id)
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        
        # Fetch lyrics from Genius
        lyrics_data = get_lyrics_with_info(track_name, artist_name)
        
        if lyrics_data and lyrics_data.get('lyrics'):
            return {
                "lyrics": lyrics_data['lyrics'],
                "url": lyrics_data.get('url'),
            }
        else:
            return {
                "lyrics": None,
                "error": lyrics_data.get('error', 'Lyrics not found')
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching lyrics: {str(e)}")

@app.get("/track/{track_id}/recommendations")
async def get_track_recommendations(track_id: str, k: int = 6):
    try:
        api = ReccobeatsAPI()
        recs = api.get_valid_recommendations(
            spotify_track_id=track_id,
            final_recommendations_count=k
        )
        return {
            "recommendations": [
                {
                    "track_id": r["track_id"],
                    "track_name": r["track_name"],
                    "artists": r["artists"],
                    "similarity_score": r["similarity_score"],
                    "popularity": r.get("popularity")
                }
                for r in recs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendations: {str(e)}")
    
@app.get("/health")
async def health():
    return {"status": "ok"}