import requests
import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple, Any, List
import json
import time
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import os
import pickle
from pathlib import Path



# knn model
def train_knn(vectors: np.ndarray, n_neighbors: int = 10, scale: bool = True) -> Tuple['NearestNeighbors', np.ndarray, Optional['StandardScaler']]:
    """
    Shared KNN trainer used by CBF (song page), CBF (taste profile), and CF.
    
    Returns:
        - Fitted NearestNeighbors model
        - Scaled (or raw) vectors used for fitting
        - StandardScaler instance (None if scale=False)
    """
    scaler = None
    if scale:
        scaler = StandardScaler()
        scaled = scaler.fit_transform(vectors)
    else:
        scaled = vectors

    k = min(n_neighbors, len(scaled))
    model = NearestNeighbors(n_neighbors=k, metric='cosine', algorithm='brute')
    model.fit(scaled)
    return model, scaled, scaler


class ReccobeatsAPI:
    """Client for interacting with the Reccobeats API."""
    
    def __init__(self):
        """Initialize the Reccobeats API client."""
        self.base_url = "https://api.reccobeats.com/v1"
        self.headers = {
            'Accept': 'application/json'
        }
    
    def get_track_details(self, spotify_track_id: str) -> Optional[Dict[str, Any]]:
        """
        Get track details from Reccobeats API using Spotify track ID.
        """
        url = f"{self.base_url}/track?ids={spotify_track_id}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            track_data = response.json()
            
            if "content" in track_data and len(track_data["content"]) > 0:
                return track_data["content"][0]
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None
        except json.JSONDecodeError:
            return None
    
    def get_audio_features(self, spotify_track_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get audio features for the selected Spotify track.
        """
        # Get track details to extract Reccobeats ID
        track_details = self.get_track_details(spotify_track_id)
        
        if not track_details:
            return None, None
        
        # Extract Reccobeats ID
        reccobeats_id = track_details.get("id")
        if not reccobeats_id:
            return None, None
        
        #Get audio features using Reccobeats ID
        url = f"{self.base_url}/track/{reccobeats_id}/audio-features"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            audio_features = response.json()
            return audio_features, reccobeats_id
            
        except requests.exceptions.RequestException:
            return None, reccobeats_id
        except json.JSONDecodeError:
            return None, reccobeats_id
    
    def get_batch_AF(self, reccobeats_ids: List[str], batch_size: int = 40) -> List[Dict]:
        """
        Get audio features for multiple tracks using Reccobeats IDs.
        """
        all_features = []
        
        for i in range(0, len(reccobeats_ids), batch_size):
            batch = reccobeats_ids[i:i + batch_size]
            params = {"ids": ",".join(batch)}

            url = f"{self.base_url}/audio-features"
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
                
            features_list = self.extract_features_from_response(data)
            if features_list:
                all_features.extend(features_list)
                
            print(f"Processed {min(i + batch_size, len(reccobeats_ids))} / {len(reccobeats_ids)} Reccobeats IDs")
            time.sleep(0.2)
            
            # try:
            # except Exception as e:
            #     print(f"Request error for batch starting at index {i}: {e}")
            #     time.sleep(1.0)
                # Retry logic omitted for brevity, keeping main flow clean
                
        return all_features
    
    def extract_features_from_response(self, data: Any) -> List[Dict]:
        """Extract audio features list from API response."""
        if isinstance(data, dict):
            if "audio_features" in data:
                features_list = data["audio_features"] or []
            elif "features" in data:
                features_list = data["features"] or []
            elif "data" in data:
                features_list = data["data"] or []
            elif "items" in data:
                features_list = data["items"] or []
            elif "content" in data:
                features_list = data["content"] or []
            else:
                candidates = [v for v in data.values() if isinstance(v, list)]
                features_list = candidates[0] if candidates else []
        elif isinstance(data, list):
            features_list = data
        else:
            features_list = []
        return features_list
    
    def extract_audio_features_vector(self, audio_features: Dict) -> List[float]:
        """Extract and normalize audio features into a numerical vector."""
        feature_definitions = {
            'danceability': {'range': (0, 1), 'default': 0.5},
            'energy': {'range': (0, 1), 'default': 0.5},
            'valence': {'range': (0, 1), 'default': 0.5},
            'tempo': {'range': (0, 250), 'default': 120},
            'loudness': {'range': (-60, 0), 'default': -10},
            'acousticness': {'range': (0, 1), 'default': 0.5},
            'instrumentalness': {'range': (0, 1), 'default': 0.5},
            'liveness': {'range': (0, 1), 'default': 0.5},
            'speechiness': {'range': (0, 1), 'default': 0.5},
            'key': {'range': (0, 11), 'default': 0},
            'mode': {'range': (0, 1), 'default': 1}
        }
        
        feature_vector = []
        for feature_name, feature_config in feature_definitions.items():
            if feature_name in audio_features and audio_features[feature_name] is not None:
                value = audio_features[feature_name]
                min_val, max_val = feature_config['range']
                if max_val > min_val:
                    normalized = (value - min_val) / (max_val - min_val)
                    normalized = max(0, min(1, normalized))
                else:
                    normalized = 0.5
                feature_vector.append(normalized)
            else:
                min_val, max_val = feature_config['range']
                default_val = feature_config['default']
                normalized = (default_val - min_val) / (max_val - min_val) if max_val > min_val else 0.5
                feature_vector.append(normalized)
        
        return feature_vector
    
    def get_recommendations(
        self, 
        spotify_track_id: str,
        size: int = 6,  # Default size updated to 6
        **kwargs
    ) -> Optional[List[Dict[str, Any]]]:
        """Get track recommendations based on a Spotify track ID."""
        params = {
            'size': size,
            'seeds': spotify_track_id
        }
        
        # Add optional filters
        optional_params = ['acousticness', 'danceability', 'energy', 'instrumentalness', 
                          'key', 'liveness', 'loudness', 'mode', 'speechiness', 
                          'tempo', 'valence', 'popularity']
        
        for param in optional_params:
            if param in kwargs and kwargs[param] is not None:
                params[param] = kwargs[param]
        
        try:
            url = f"{self.base_url}/track/recommendation"
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            recommendations_data = response.json()
            if "content" in recommendations_data:
                return recommendations_data["content"]
            else:
                return []
        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return None
        
    @staticmethod
    def extract_spotifyID_from_url(spotify_url: str) -> str:

        if not spotify_url or 'spotify.com/track/' not in spotify_url:
            return ''
        parts = spotify_url.split('spotify.com/track/')
        if len(parts) > 1:
            track_part = parts[1]
            if len(track_part) == 22: #make sure that the spotify id is only 22 characters
                return track_part
        return ''

    
    def rec_metadata(self, initial_recs: List[Dict]) -> Tuple[List[str], Dict]:
        """
        Process raw recommendation results into reccobeats_ids list and rec_map dict.
        Shared helper for get_enhanced_recommendations and CF pipeline.
        """
        reccobeats_ids = []
        rec_map = {}
        
        for rec in initial_recs:
            rid = rec.get('id')
            if rid:
                reccobeats_ids.append(rid)
                
                spotify_url = rec.get('href', '')
                spotify_id = self.extract_spotifyID_from_url(spotify_url)
                track_id_to_use = spotify_id if spotify_id else rid
                
                rec_map[rid] = {
                    'track_title': rec.get('trackTitle', 'Unknown'),
                    'artists': ', '.join([a.get('name', 'Unknown') for a in rec.get('artists', [])]),
                    'spotify_url': spotify_url,
                    'spotify_track_id': track_id_to_use,
                    'popularity': rec.get('popularity', 0)  # Reccobeats 0-100
                }
        
        return reccobeats_ids, rec_map

    
    def get_enhanced_recommendations(
        self, 
        spotify_track_id: str,
        initial_recommendations_count: int = 100,
        final_recommendations_count: int = 6,
        original_features: Optional[Dict] = None,
        **filters) -> List[Dict]:
        """
        Get enhanced recommendations using K-NN filtering.
        """
        try:
            if original_features:
                features = original_features
            else:
                features, _= self.get_audio_features(spotify_track_id)
                if not features:
                    return []
            original_vector = self.extract_audio_features_vector(original_features)
            
            
            # 2. Get initial recommendations
            initial_recs = self.get_recommendations(
                spotify_track_id,
                size=initial_recommendations_count,
                **filters
            )
            if not initial_recs:
                return []
            
            # 3. Process metadata & extract IDs from
            reccobeats_ids, rec_map = self.rec_metadata(initial_recs)

            if not reccobeats_ids:
                return []

            # 4. Batch fetch audio features for recommendations
            batch_features = self.get_batch_AF(reccobeats_ids)
            features_by_id = {f.get('id'): f for f in batch_features if f.get('id')}
            
            # 5. Prepare data for K-NN
            recs_with_features = []
            for rid in reccobeats_ids:
                if rid in features_by_id and rid in rec_map:
                    feat_vec = self.extract_audio_features_vector(features_by_id[rid])
                    meta = rec_map[rid]
                    recs_with_features.append({
                        'track_id': meta['spotify_track_id'],
                        'track_name': meta['track_title'],
                        'artists': meta['artists'],
                        'feature_vector': feat_vec,
                        'popularity': meta['popularity'],
                        'spotify_url': meta['spotify_url'],
                        'reccobeats_id': rid  # Store for fallback
                    })

            # 6. Run K-NN
            vectors = np.array([original_vector] + [r['feature_vector'] for r in recs_with_features])
            knn, scaled_vectors, _= train_knn(vectors, n_neighbors=final_recommendations_count + 1)
            distances, indices= knn.kneighbors(scaled_vectors[0:1])
            
            final_recs = []
            for i, neighbor_idx in enumerate(indices[0]):
                if neighbor_idx == 0: continue # Skip self
                
                rec_idx = neighbor_idx - 1 # Adjust for offset
                if 0 <= rec_idx < len(recs_with_features):
                    rec = recs_with_features[rec_idx]
                    similarity = 1 - distances[0][i]
                    
                    # Weight by popularity (optional)
                    weighted_score = (0.9 * similarity) + (0.1 * (rec['popularity'] / 100.0))
                    
                    final_recs.append({
                        'track_id': rec['track_id'],
                        'track_name': rec['track_name'],
                        'artists': rec['artists'],
                        'similarity_score': weighted_score,
                        'popularity': rec['popularity'],
                        'reccobeats_id': rec['reccobeats_id']
                    })
            
            final_recs.sort(key=lambda x: x['similarity_score'], reverse=True)
            return final_recs[:final_recommendations_count]
            
        except Exception as e:
            print(f"Error in enhanced recommendations: {e}")
            return []

    def get_valid_recommendations(
        self,
        spotify_track_id: str,
        final_recommendations_count: int = 6,
        og_feature: Optional[Dict] = None,
        min_similarity: float = 0.7,
        **filters
    ) -> List[Dict]:
        """
        Wrapper around get_enhanced_recommendations that retries with
        different popularity tiers until final_recommendations_count
        songs above min_similarity are collected.
        """
        qualified_recs = []
        seen_track_ids = set()
        # 
        popularity_tiers = [100,90,80,70,60,50,40,30,20,10,100,90,80,70,60,50,40,30,20,10]
        for round_num, pop_value in enumerate(popularity_tiers):
            if len(qualified_recs) >= final_recommendations_count:
                break
            
            # Build filters for this round
            round_filters = dict(filters)
            if pop_value is not None:
                round_filters['popularity'] = pop_value
            
            recs = self.get_enhanced_recommendations(
                spotify_track_id=spotify_track_id,
                initial_recommendations_count=100,
                final_recommendations_count=6,
                original_features=og_feature,
                **round_filters
            )
            
            if not recs:
                continue
            
            new_this_round = 0
            for rec in recs:
                if rec['track_id'] in seen_track_ids:
                    continue
                
                seen_track_ids.add(rec['track_id'])
                
                if rec['similarity_score'] >= min_similarity:
                    qualified_recs.append(rec)
                    new_this_round += 1
            
            pop_label = f"popularity={pop_value}" if pop_value is not None else "no filter"
            print(f"Round {round_num + 1} ({pop_label}): {len(qualified_recs)}/{final_recommendations_count} qualified (>= {min_similarity*100:.0f}%)")
        
        qualified_recs.sort(key=lambda x: x['similarity_score'], reverse=True)
        return qualified_recs[:final_recommendations_count]
    
def get_cbf_recommendations_from_favourites(
    user_favourites: List[Dict],
    k: int = 6,
    exclude_ids: set = None
) -> List[Dict]:
    """
    Scoring uses the same formula as the song-page CBF:
      weighted = 0.9 * cosine_similarity + 0.1 * (reccobeats_popularity / 100)
    """
    if not user_favourites:
        return []
    
    api = ReccobeatsAPI()
    
    feature_keys = [
        'danceability', 'energy', 'valence', 'tempo', 'loudness',
        'acousticness', 'instrumentalness', 'liveness', 'speechiness',
        'key', 'mode'
    ]

    fav_features = []
    fav_ids_for_seeds = []
    
    for fav in user_favourites:
        track_id = fav.get('track_id', '')
        if not track_id:
            continue
        features, _ = api.get_audio_features(track_id)
        if features:
            fav_features.append(api.extract_audio_features_vector(features))
            fav_ids_for_seeds.append(track_id)
    
    if not fav_features:
        return []
    
    # 2. Average into taste profile
    taste_profile = {}
    for key in feature_keys:
        values = [f[key] for f in fav_features if key in f and f[key] is not None]
        if values:
            taste_profile[key] = sum(values) / len(values)
    
    # 3. Seed recommendations from up to 3 favourites
    seed_ids = fav_ids_for_seeds[:3]
    seen_ids = set(exclude_ids) if exclude_ids else set()
    seen_ids.update(f.get('track_id', '') for f in user_favourites)
    
    all_recs = []
    
    for seed_id in seed_ids:
        try:
            recs = api.get_enhanced_recommendations(
                spotify_track_id=seed_id,
                initial_recommendations_count=100,
                final_recommendations_count=k,
                original_features=taste_profile
            )
            if recs:
                for rec in recs:
                    if rec['track_id'] not in seen_ids:
                        seen_ids.add(rec['track_id'])
                        rec['source'] = 'cbf'
                        all_recs.append(rec)
        except Exception as e:
            print(f"CBF seed error for {seed_id}: {e}")
    
    # 4. Sort by similarity score and return top k
    all_recs.sort(key=lambda x: x['similarity_score'], reverse=True)
    return all_recs[:k]
    

def valid_recommendations(
        features_dict: Dict,
        spotify_track_id: str = None,
        dataset_path: str = None,
        k: int = 6
) -> List[Dict]:
    if not spotify_track_id:
        return []
    
    api = ReccobeatsAPI()
    return api.get_valid_recommendations(
        spotify_track_id,
        og_feature = features_dict if features_dict else None
    )
