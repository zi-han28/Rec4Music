import unittest
from typing import List, Dict
from engine import ReccobeatsAPI, get_recommendations_from_favourites, analyse_favourites

# def test_get_recommendations_from_favourites():
#     """
#     Simple test function to verify get_recommendations_from_favourites works
#     using only Spotify track IDs.
#     """
#     print("=" * 60)
#     print("TESTING: get_recommendations_from_favourites")
#     print("=" * 60)
    
#     # Test data: 6 Spotify track IDs
#     test_track_ids = [
#         "6l8GvAyoUZwWDgF1e4822w",  # Example track 1
#         "46nmxXC0nbxl8Wm2Vrdo70",  # Example track 2
#         "7lQ8MOhq6IN2w8EYcFNSUk",  # Example track 3
#         "0VjIjW4GlUZAMYd2vXMi3b",  # Example track 4
#         "7qiZfU4dY1lWllzX7mPBI3",  # Example track 5
#         "4Dvkj6JhhA12EX05fT7y2e"   # Example track 6
#     ]
    
#     # Convert to the expected format (list of dicts with 'track_id' key)
#     user_favourites = [{"track_id": track_id} for track_id in test_track_ids]
    
#     print(f"\n📊 Input: {len(user_favourites)} favourite tracks")
#     print(f"Track IDs: {test_track_ids}\n")
#     fav_analysis = analyse_favourites(user_favourites)
#     taste_profile = fav_analysis['taste_profile']
#     fav_parameter = fav_analysis['std_factor']
#     fav_input = fav_analysis['mean_factor']
#     print(taste_profile)
#     print("fav_parameter:",fav_parameter, "fav_input:",fav_input)
#     try:
#         # Call the function
#         print("🔄 Calling get_recommendations_from_favourites...")
#         recommendations = get_recommendations_from_favourites(
#             user_favourites=user_favourites,
#             k=6  # Request 6 recommendations
#         )
#         # Check results
#         if recommendations is None:
#             print(" Function returned None")
#             return False
            
#         if not recommendations:
#             print("Function returned an empty list (no recommendations found)")
#             print("   This might happen if the API is rate-limited or tracks don't exist")
#             return False
        
#         # Display results
#         print(f"\n SUCCESS! Found {len(recommendations)} recommendations\n")
#         print("-" * 60)
#         print("RECOMMENDATIONS:")
#         print("-" * 60)
        
#         for i, rec in enumerate(recommendations, 1):
#             print(f"{i}. Track ID: {rec}")
            
#             # Show similarity score if available
#             if 'similarity_score' in rec:
#                 print(f"   Similarity: {rec['similarity_score']:.3f}")
#             print()
        
#         print("=" * 60)
#         print(" TEST PASSED - Function executed successfully")
#         print("=" * 60)
#         return True
        
#     except Exception as e:
#         print(f"\n TEST FAILED - Error: {e}")
#         import traceback
#         traceback.print_exc()
#         return False

def test_reccobeats_api_call():
    """
    Direct test of the Reccobeats API layer.
    Verifies the API is reachable and returns recommendations for a known seed.
    """
    print("=" * 60)
    print("TESTING: ReccobeatsAPI.get_recommendations")
    print("=" * 60)

    api = ReccobeatsAPI()

    # --- Step 1: verify a single track resolves in Reccobeats ---
    test_track_id = "70LcF31zb1H0PyJoS1Sx1r"
    print(f"\n🔍 Step 1: Resolving track details for {test_track_id}")

    details = api.get_track_details(test_track_id)
    if not details:
        print(f"❌ get_track_details returned None — track ID not found in Reccobeats")
        print("   This means the API is unreachable OR the track isn't in the catalog.")
        return False

    reccobeats_id = details.get("id")
    print(f"✅ Track resolved: '{details.get('trackTitle')}' by "
          f"{', '.join(a.get('name', '?') for a in details.get('artists', []))}")
    print(f"   Reccobeats ID: {reccobeats_id}")

    # --- Step 2: verify audio features endpoint works for this track ---
    print(f"\n🔍 Step 2: Fetching audio features")
    features, rid = api.get_audio_features(test_track_id)
    if not features:
        print(f"❌ get_audio_features returned None for {test_track_id}")
        return False

    print(f"✅ Audio features retrieved (keys: {list(features.keys())[:6]}...)")

    # --- Step 3: call get_recommendations directly ---
    print(f"\n🔍 Step 3: Calling get_recommendations (size=6)")
    recs = api.get_recommendations(spotify_track_id=test_track_id, size=6)

    if recs is None:
        print("❌ get_recommendations returned None (request failed)")
        return False

    if not recs:
        print("⚠️ get_recommendations returned an empty list")
        print("   API is reachable but returned no content for this seed.")
        return False

    print(f"✅ API returned {len(recs)} recommendations\n")
    print("-" * 60)
    for i, rec in enumerate(recs, 1):
        title = rec.get("trackTitle", "Unknown")
        artists = ", ".join(a.get("name", "?") for a in rec.get("artists", []))
        pop = rec.get("popularity", "?")
        print(f"{i}. {title} — {artists} (popularity: {pop})")
        print(f"   reccobeats id: {rec.get('id')}")
    print("-" * 60)

    print("\n" + "=" * 60)
    print("✅ TEST PASSED — Reccobeats API is reachable and returning data")
    print("=" * 60)
    return True



if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# Reccobeats API Layer Tests")
    print("#" * 60 + "\n")

    api_test_passed = test_reccobeats_api_call()

    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    print("=" * 60)
    print(f"Reccobeats API call:    {'✅ PASSED' if api_test_passed else '❌ FAILED'}")
    print("=" * 60)