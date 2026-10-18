# test_recommendations.py
from engine import ReccobeatsAPI

def test_single_track_recommendations():
    # Initialize the Reccobeats API client
    api = ReccobeatsAPI()
    
    # Target Spotify Track ID provided
    test_track_id = "4laW52Dhj4RhmYqdXYiYw9"
    
    print(f"🔍 Fetching recommendations for Spotify ID: {test_track_id}...\n")
    
    # Call the unified get_music_recommendations method
    recommendations = api.get_valid_recommendations(
        spotify_track_id=test_track_id,
        final_recommendations_count=6
    )
    
    if recommendations:
        print(f"✅ Successfully retrieved {len(recommendations)} recommendations:\n")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['track_name']} by {rec['artists']}")
            print(f"   - Similarity Score: {rec['similarity_score']:.2f}")
            print(f"   - Popularity: {rec['popularity']}")
            print(f"   - Spotify Track ID: {rec['track_id']}\n")
    else:
        print("❌ No recommendations were returned. Check network connectivity or track ID validity.")

if __name__ == "__main__":
    test_single_track_recommendations()