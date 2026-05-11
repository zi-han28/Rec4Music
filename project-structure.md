# Workspace Structure

Files listed in .gitignore will be excluded.

## Configuration Files

### requirements.txt
```
fastapi
uvicorn[standard]
python-multipart
pydantic
python-dotenv
bcrypt
sqlite3-api
requests
numpy
pandas
scikit-learn
transformers
torch
lyricsgenius
```

## File Structure

- 📄 BERT_analysis.py
  - Imports:
    - import re
    - import torch
    - import transformers.AutoTokenizer
    - import transformers.AutoModelForSequenceClassification
  - Functions:
    - run_unit_test
  - Classes:
    - SentimentAnalyzer
  - Methods:
    - __init__
    - _clean_text
    - analyze
- 📄 auth.py
  - Imports:
    - import sqlite3
    - import bcrypt
    - import streamlit as st
    - import json
  - Functions:
    - init_db
    - create_user
    - authenticate_user
    - get_user_favourites
    - add_to_favourites
    - remove_from_favourites
    - is_favourite
- 📄 engine.py
  - Imports:
    - import requests
    - import numpy as np
    - import pandas as pd
    - import typing.Dict
    - import typing.Optional
    - import typing.Tuple
    - import typing.Any
    - import typing.List
    - import json
    - import time
    - import sklearn.preprocessing.StandardScaler
    - import sklearn.neighbors.NearestNeighbors
    - import os
    - import pickle
    - import pathlib.Path
  - Functions:
    - train_knn
    - get_cbf_recommendations_from_favourites
    - valid_recommendations
  - Classes:
    - ReccobeatsAPI
  - Methods:
    - __init__
- 📄 genius_api.py
  - Imports:
    - import os
    - import re
    - import typing.Optional
    - import typing.Dict
    - import lyricsgenius
    - import dotenv.load_dotenv
    - import streamlit as st
  - Functions:
    - get_genius_api
    - get_lyrics
    - get_lyrics_with_info
  - Classes:
    - GeniusAPI
  - Methods:
    - __init__
- 📄 main.py
  - Imports:
    - import fastapi.FastAPI
    - import fastapi.HTTPException
    - import fastapi.Depends
    - import fastapi.status
    - import fastapi.Query
    - import fastapi.middleware.cors.CORSMiddleware
    - import fastapi.security.HTTPBearer
    - import fastapi.security.HTTPAuthorizationCredentials
    - import typing.Optional
    - import typing.List
    - import typing.Dict
    - import typing.Any
    - import uvicorn
    - import json
    - import os
    - import base64
    - import time
    - import dotenv.load_dotenv
    - import spotipy
    - import spotipy.oauth2.SpotifyClientCredentials
    - import BERT_analysis.SentimentAnalyzer
    - import genius_api.get_lyrics_with_info
    - import engine.ReccobeatsAPI
    - import engine.valid_recommendations
    - import engine.get_cbf_recommendations_from_favourites
    - import auth.(
- 📁 reccobeats-frontend/
  - 📄 AGENTS.md
  - 📄 CLAUDE.md
  - 📄 README.md
  - 📁 app/
    - 📄 favicon.ico
    - 📄 globals.css
    - 📄 layout.tsx
      - Imports:
        - import { Geist, Geist_Mono } from "next/font/google"
      - Exports:
        - metadata
      - Functions:
        - RootLayout
    - 📄 page.tsx
      - Imports:
        - import { useState } from 'react'
        - import Image from 'next/image'
        - import { useRouter } from 'next/navigation'
      - Functions:
        - SearchPage
        - handleSearch
  - 📄 eslint.config.mjs
  - 📄 next-env.d.ts
  - 📄 next.config.ts
  - 📄 package-lock.json
  - 📄 package.json
  - 📄 postcss.config.mjs
  - 📁 public/
    - 📄 file.svg
    - 📄 globe.svg
    - 📄 next.svg
    - 📄 vercel.svg
    - 📄 window.svg
  - 📄 tsconfig.json
- 📄 requirements.txt
