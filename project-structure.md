# Workspace Structure

Files listed in .gitignore will be excluded.

## Configuration Files

### requirements.txt
```
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.12.1
attrs==25.4.0
bcrypt==5.0.0
beautifulsoup4==4.14.3
cachetools==6.2.6
certifi==2026.7.22
charset-normalizer==3.4.4
click==8.3.1
dnspython==2.8.0
duckdb==1.4.4
fastapi==0.136.1
filelock==3.25.0
fsspec==2026.2.0
gitdb==4.0.12
GitPython==3.1.46
h11==0.16.0
hf-xet==1.3.2
httpcore==1.0.9
httptools==0.7.1
httpx==0.28.1
huggingface_hub==1.5.0
idna==3.11
joblib==1.5.3
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
lyricsgenius==3.7.6
markdown-it-py==4.0.0
mdurl==0.1.2
mpmath==1.3.0
narwhals==2.17.0
networkx==3.6.1
numpy==2.4.2
packaging==26.0
pandas==2.3.3
pillow==12.1.1
protobuf==6.33.5
pyarrow==23.0.1
pydantic==2.13.4
pydantic_core==2.46.4
Pygments==2.19.2
PyJWT==2.14.0
pymongo==4.18.1
python-dateutil==2.9.0.post0
python-dotenv==1.2.2
python-multipart==0.0.27
pytz==2026.1.post1
PyYAML==6.0.3
redis==7.2.1
referencing==0.37.0
regex==2026.2.28
requests==2.32.5
rich==14.3.3
rpds-py==0.30.0
safetensors==0.7.0
scikit-learn==1.8.0
scipy==1.17.1
setuptools==82.0.0
shellingham==1.5.4
six==1.17.0
smmap==5.0.2
soupsieve==2.8.3
spotipy==2.25.2
sqlite3_api==2.0.4
starlette==1.0.0
sympy==1.14.0
tenacity==9.1.4
threadpoolctl==3.6.0
tokenizers==0.22.2
toml==0.10.2
torch==2.10.0
torchvision==0.25.0
tqdm==4.67.3
transformers==5.2.0
typer==0.24.1
typer-slim==0.24.0
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2025.3
urllib3==2.6.3
uvicorn==0.46.0
uvloop==0.22.1
watchfiles==1.1.1
websockets==16.0
Werkzeug==3.1.6
youtube-search-python==1.6.6
yt-dlp==2026.8.19

```

## File Structure

- 📄 Dockerfile
- 📁 app-frontend/
  - 📄 AGENTS.md
  - 📄 CLAUDE.md
  - 📄 README.md
  - 📁 app/
    - 📁 FYP/
      - 📄 page.tsx
        - Imports:
          - import { useState } from 'react'
          - import Image from 'next/image'
          - import { useRouter } from 'next/navigation'
        - Functions:
          - ForYou
    - 📄 favicon.ico
    - 📁 favourites/
      - 📄 page.tsx
        - Imports:
          - import { useEffect, useState } from 'react'
          - import Image from 'next/image'
          - import { useRouter } from 'next/navigation'
        - Functions:
          - FavouritesPage
          - fetchFavourites
          - handleRemove
          - fetchFavRec
    - 📄 globals.css
    - 📄 layout.tsx
      - Imports:
        - import { Geist, Geist_Mono } from "next/font/google"
        - import { AuthProvider } from '@/lib/AuthContext'
        - import Navbar from "@/components/navbar"
      - Exports:
        - metadata
      - Functions:
        - RootLayout
    - 📁 login/
      - 📄 page.tsx
        - Imports:
          - import { useState } from 'react'
          - import { useRouter } from 'next/navigation'
          - import Link from 'next/link'
          - import { useAuth } from '@/lib/AuthContext'
        - Functions:
          - LoginPage
          - handleSubmit
    - 📄 page.tsx
      - Imports:
        - import { useState } from 'react'
        - import Image from 'next/image'
        - import { useRouter } from 'next/navigation'
      - Functions:
        - homePage
    - 📁 register/
      - 📄 page.tsx
        - Imports:
          - import { useState } from 'react'
          - import { useRouter } from 'next/navigation'
          - import Link from 'next/link'
        - Functions:
          - RegisterPage
          - handleSubmit
    - 📁 search/
      - 📄 page.tsx
        - Imports:
          - import { useState } from 'react'
          - import Image from 'next/image'
          - import { useRouter } from 'next/navigation'
          - import { json } from 'stream/consumers'
        - Functions:
          - SearchPage
          - handleSearch
    - 📁 track/
      - 📁 [id]/
        - 📄 page.tsx
          - Imports:
            - import { useRouter } from 'next/navigation'
            - import { useEffect, useState } from 'react'
            - import { useParams } from 'next/navigation'
            - import Image from 'next/image'
          - Functions:
            - SongPage
            - fetchTrack
            - toggleFavourite
            - fetchRecommendations
            - fetchLyrics
            - CloseLyrics
  - 📁 components/
    - 📄 navbar.tsx
      - Imports:
        - import { useState } from 'react'
        - import Link from 'next/link'
        - import { useAuth } from '@/lib/AuthContext'
      - Functions:
        - Navbar
  - 📄 eslint.config.mjs
  - 📁 lib/
    - 📄 AuthContext.tsx
      - Imports:
        - import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react"
      - Exports:
        - AuthProvider
        - useAuth
      - Functions:
        - AuthProvider
        - login
        - logout
        - useAuth
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
- 📄 auth.py
  - Imports:
    - import bcrypt
    - import db.users_collection
  - Functions:
    - init_db
    - create_user
    - authenticate_user
    - get_user_favourites
    - add_to_favourites
    - remove_from_favourites
    - is_favourite
- 📄 db.py
  - Imports:
    - import os
    - import certifi
    - import pymongo.MongoClient
    - import dotenv.load_dotenv
- 📄 engine.py
  - Imports:
    - import urllib.response
    - import random
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
    - analyse_favourites
    - get_recommendations_from_favourites
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
    - import genius_api.get_lyrics_with_info
    - import engine.ReccobeatsAPI
    - import engine.valid_recommendations
    - import engine.get_recommendations_from_favourites
    - import engine.analyse_favourites
    - import auth.(
    - import pydantic.BaseModel
    - import datetime.datetime
    - import datetime.timedelta
    - import datetime.timezone
    - import jwt
  - Functions:
    - create_access_token
    - get_current_username
  - Classes:
    - UserCredentials
    - TokenResponse
    - FavouriteTrack
- 📄 project-structure.md
- 📄 railway.toml
- 📄 requirements.txt
- 📄 test_engine.py
  - Imports:
    - import unittest
    - import typing.List
    - import typing.Dict
    - import engine.get_recommendations_from_favourites
    - import engine.analyse_favourites
  - Functions:
    - test_get_recommendations_from_favourites
- 📄 users.db
