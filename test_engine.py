import unittest
from typing import List, Dict
from engine import get_recommendations_from_favourites

def test_get_recommendations_from_favourites():
    """
    Simple test function to verify get_recommendations_from_favourites works
    using only Spotify track IDs.
    """
    print("=" * 60)
    print("TESTING: get_recommendations_from_favourites")
    print("=" * 60)
    
    # Test data: 6 Spotify track IDs
    test_track_ids = [
        "6l8GvAyoUZwWDgF1e4822w",  # Example track 1
        "46nmxXC0nbxl8Wm2Vrdo70",  # Example track 2
        "7lQ8MOhq6IN2w8EYcFNSUk",  # Example track 3
        "0VjIjW4GlUZAMYd2vXMi3b",  # Example track 4
        "7qiZfU4dY1lWllzX7mPBI3",  # Example track 5
        "4Dvkj6JhhA12EX05fT7y2e"   # Example track 6
    ]
    
    # Convert to the expected format (list of dicts with 'track_id' key)
    user_favourites = [{"track_id": track_id} for track_id in test_track_ids]
    
    print(f"\n📊 Input: {len(user_favourites)} favourite tracks")
    print(f"Track IDs: {test_track_ids}\n")
    
    try:
        # Call the function
        print("🔄 Calling get_recommendations_from_favourites...")
        recommendations = get_recommendations_from_favourites(
            user_favourites=user_favourites,
            k=6  # Request 6 recommendations
        )
        
        # Check results
        if recommendations is None:
            print("❌ Function returned None")
            return False
            
        if not recommendations:
            print("⚠️ Function returned an empty list (no recommendations found)")
            print("   This might happen if the API is rate-limited or tracks don't exist")
            return False
        
        # Display results
        print(f"\n✅ SUCCESS! Found {len(recommendations)} recommendations\n")
        print("-" * 60)
        print("RECOMMENDATIONS:")
        print("-" * 60)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. Track ID: {rec}")
            
            # Show similarity score if available
            if 'similarity_score' in rec:
                print(f"   Similarity: {rec['similarity_score']:.3f}")
            print()
        
        print("=" * 60)
        print("✅ TEST PASSED - Function executed successfully")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED - Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_passed = test_get_recommendations_from_favourites()

    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    print("=" * 60)
    print(f"Recommendations Test:  {'✅ PASSED' if test_passed else '❌ FAILED'}")
    print("=" * 60)