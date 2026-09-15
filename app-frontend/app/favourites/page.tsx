'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';

interface FavouriteTrack {
  track_id: string;
  track_name: string;
  artist_name: string;
  album_name: string;
  album_image: string | null;
}

interface favouriteRecommendation{
  track_id: string;
  track_name: string;
  artists: string;
  similarity_score: number;
  popularity: number | null;
}

interface tasteProfile{
  danceability?: number;
  energy?: number;
  valence?: number;
  tempo?: number;
  loudness?: number;
  acousticness?: number;
  instrumentalness?: number;
  liveness?: number;
  speechiness?: number;
  key?: number;
  mode?: number;
}

export default function FavouritesPage() {
  const [favourites, setFavourites] = useState<FavouriteTrack[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [removingId, setRemovingId] = useState<string | null>(null);
  const [favRec, setRecommendations] = useState<favouriteRecommendation[]>([]);
  const [tasteProfile, setTasteProfile] = useState<tasteProfile>({});
  const [loadingRecs, setLoadingRecs] = useState(true);
  const [recsError, setRecsError] = useState('');
  const router = useRouter();

//   fetch favourties
  useEffect(() => {
    const fetchFavourites = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/login');
        return;
      }

      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/favourites`, {
          headers: {Authorization: `Bearer ${token}`},
        });

        if (res.status === 401) {
          localStorage.removeItem('access_token');
          router.push('/login');
          return;
        }

        if (!res.ok){
            const errData = await res.json().catch(() => null);
            throw new Error(errData?.detail || 'Failed to load favourites');
        } 

        const data = await res.json();
        setFavourites(data.favourites);
      } catch (e) {
        setError('Could not load your favourites.');
      } finally {
        setLoading(false);
      }
    };

    fetchFavourites();
  }, [router]);

  const handleRemove = async (trackId: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/login');
      return;
    }

    setRemovingId(trackId);
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/favourites?track_id=${trackId}`,
        {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (res.status === 401) {
        localStorage.removeItem('access_token');
        router.push('/login');
        return;
      }

      if (!res.ok) throw new Error('Failed to remove favourite');

      setFavourites((prev) => prev.filter((t) => t.track_id !== trackId));
    } catch (e) {
      setError('Could not remove that track. Please try again.');
    } finally {
      setRemovingId(null);
    }
  };

  // display favourite recommendations
  useEffect(()=>{
    const fetchFavRec = async () =>{
      const token = localStorage.getItem('access_token');
      if(!token) return;
      try{
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/favourites/recommendations`, {headers: {Authorization:`Bearer ${token}`}});
        if (res.status == 401){
          localStorage.removeItem('access_token');
          router.push('/login');
          return;
        }
        if (!res.ok) throw new Error('Failed to fetch recommendations');

        const data = await res.json();
        setTasteProfile(data.taste_profile || {});
        setLoadingRecs(true);
        setRecommendations(data.recommendations?? []);
      }catch(e){
        setRecsError('could not load favourite recommendations')
        setRecommendations([]);
      }
      finally{
        setLoadingRecs(false);
      }
    };
    fetchFavRec();
  },[router]);

  if (loading) {
    return (
      <main className="min-h-screen bg-gray-950 text-white px-6 py-10">
        <div className="flex items-center gap-3">
          <div className="animate-spin h-5 w-5 border-2 border-purple-500 border-t-transparent rounded-full" />
          <p className="text-gray-400">Loading your favourites...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white px-6 py-10">
      <div className="container mx-auto max-w-2xl">
        <h1 className="text-3xl font-bold mb-8"> Your Favourites</h1>

        {error && <p className="text-red-400 mb-4">{error}</p>}

        {favourites.length === 0 ? (
          <p className="text-gray-500">
            You haven&apos;t favourited any songs yet. Go search for some!
          </p>
        ) : (
          <div className="flex flex-col gap-4">
            {favourites.map((track) => (
              <div
                key={track.track_id}
                className="flex items-center gap-4 bg-gray-800 rounded-xl p-4
                           hover:bg-gray-700 transition"
              >
                <div
                  className="flex items-center gap-4 flex-1 min-w-0 cursor-pointer"
                  onClick={() => router.push(`/track/${track.track_id}`)}>
                  {track.album_image ? (
                    <Image
                      src={track.album_image}
                      alt={track.album_name}
                      width={64}
                      height={64}
                      className="rounded-lg"
                    />
                  ) : (
                    <div className="w-16 h-16 bg-gray-600 rounded-lg" />
                  )}
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold truncate">{track.track_name}</p>
                    <p className="text-gray-400 text-sm truncate">{track.artist_name}</p>
                    <p className="text-gray-500 text-xs truncate">{track.album_name}</p>
                  </div>
                </div>

                <button
                  onClick={() => handleRemove(track.track_id)}
                  disabled={removingId === track.track_id}
                  className="text-red-400 hover:text-red-300 text-sm px-3 py-2
                             disabled:opacity-50 cursor-pointer">
                  {removingId === track.track_id ? '...' : '❌'}
                </button>
              </div>
            ))}
          </div>
        )}
        <div className="mt-10">
          <h2 className="text-2xl font-bold mb-4">Your taste profile</h2>
          <p>Based on your favourited songs</p>
          {loadingRecs ? (
            <div className="flex items-center gap-3">
              <div className="animate-spin h-5 w-5 border-2 border-purple-500 border-t-transparent rounded-full" />
              <p className="text-gray-400">Analysing your taste...</p>
            </div>): 
            recsError ? (
              <p className="text-red-400">{recsError}</p>
            ) : (
              <>
                {Object.keys(tasteProfile).length>0 && (
                  <div className="bg-gray-800 rounded-lg p-4 mb-6">
                  <p className="text-sm text-gray-400 mb-2">Your taste profile</p>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-sm">
                    {Object.entries(tasteProfile).map(([key, value]) => (
                      <div key={key} className="text-gray-300">
                        {key}: <span className="text-white">{Number(value).toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                </div>
                )}
                {favRec.length>0 ? (
                  <div className="flex flex-col gap-3">
                    {favRec.map((rec) => (
                      <div
                        key={rec.track_id}
                        onClick={() => router.push(`/track/${rec.track_id}`)}
                        className="bg-gray-800 hover:bg-gray-700 rounded-lg p-4 cursor-pointer transition"
                      >
                        <p className="font-semibold">{rec.track_name}</p>
                        <p className="text-gray-400 text-sm">{rec.artists}</p>
                        <p className="text-purple-400 text-xs mt-1">
                          {(rec.similarity_score * 100).toFixed(1)}% match
                        </p>
                      </div>
                    ))}
                </div>): (
                  <p className="text-gray-500">No recommendations yet.</p>
                )}
              </>
            )}
        </div>
      </div>
    </main>
  );
}