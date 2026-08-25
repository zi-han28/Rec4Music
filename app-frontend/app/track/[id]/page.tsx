// app-frontend/app/track/[id]
'use client';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';

interface Track {
  track_id: string;
  track_name: string;
  artist: string;
  album: string;
  album_image: string | null;
  embed_url: string;
}
interface LyricsData {
  lyrics: string | null;
  url?: string;
  error?: string;
}
interface Recommendations{
  track_id: string;
  track_name: string;
  artists: string;
  similarity_score: number;
  popularity: number | null;
}

export default function SongPage(){
    const{ id } = useParams();
    const [track, setTrack] = useState<Track | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [lyrics, setLyrics] = useState<LyricsData | null>(null);
    const [loadingLyrics, setLoadingLyrics] = useState(false);
    const [showLyrics, setShowLyrics] = useState(false);
    const router = useRouter();
    const [recommendations, setRecommendations] = useState<Recommendations[]>([]);
    const [loadingRecs, setLoadingRecs] = useState(true);
    const [recsError, setRecsError] = useState('');
    const [favouritedIds, setFavouriteIds] = useState <Set<string>>(new Set());

    useEffect(() =>{
        const fetchTrack = async ()=>{
            try{
                const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/track/${id}`)
                if (!res.ok) throw new Error('Track not found');
                const data = await res.json();
                setTrack(data);
            } catch(e){
                setError('Could not load track')
            } finally{
                setLoading(false)
            }
        };

        if(id) fetchTrack();
    }, [id])

      const toggleFavourite = async (track: Track, e: React.MouseEvent) => {
        e.stopPropagation(); // don't trigger the card's onClick navigation
    
        const token = localStorage.getItem('access_token');
        if (!token) {
          router.push('/login');
          return;
        }
    
        const isFav = favouritedIds.has(track.track_id);
        try{
          if (isFav){
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/favourites?track_id=${track.track_id}`,
              {
                method: 'DELETE',
                headers: {Authorization: `Bearer ${token}`},
              }
            );
            if (!res.ok) {
                const errData = await res.json().catch(() => null)
                throw new Error (errData?.detail || 'Failed to remove favourited track');
            }
            setFavouriteIds((prev) => {
              const next = new Set(prev);
              next.delete(track.track_id);
              return next;
            });
          } else {
            const res = await fetch (`${process.env.NEXT_PUBLIC_API_URL}/favourites`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({
                track_id: track.track_id,
                track_name: track.track_name,
                artist_name: track.artist,
                album_name: track.album,
                album_image: track.album_image,
              }),
            });
            if (!res.ok){
                const errData = await res.json().catch(()=>null)
                throw new Error(errData?.detail ||'Failed to add new favourite');
            } 
            setFavouriteIds((prev) => new Set(prev).add(track.track_id));
          }
        }catch(err){
          console.error(err)
        }
      }
    
    // load recommendations
    useEffect(() => {
        const fetchRecommendations = async () => {
            setLoadingRecs(true);
            try {
                const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/track/${id}/recommendations?k=6`);
                if (!res.ok) throw new Error('Failed to fetch recommendations');
                const data = await res.json();
                setRecommendations(data.recommendations);
            } catch (e) {
                setRecsError('Could not load recommendations');
            } finally {
                setLoadingRecs(false);
            }
        };

        if (id) fetchRecommendations();
    }, [id]);

    // Fetch lyrics when track is loaded and user wants to see them
    const fetchLyrics = async () => {
        if (!track) return;

        // If lyrics already fetched, just show them without re-fetching
        if (lyrics !== null) {
            setShowLyrics(true);
            return;
        }
        
        setLoadingLyrics(true);
        setShowLyrics(true);
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/track/${id}/lyrics`);
            if (!response.ok) {
                throw new Error('Failed to fetch lyrics');
            }
            const data = await response.json();
            setLyrics(data);
        } catch (err) {
            setLyrics({ lyrics: null, error: 'Could not load lyrics' });
        } finally {
            setLoadingLyrics(false);
        }
    };

    const CloseLyrics = async () => {
        setShowLyrics(false);
    }

    if (loading) return <p className="text-white p-10">Loading...</p>;
    if (error || !track) return <p className="text-red-400 p-10">{error}</p>;

    return (
        <main className="min-h-screen bg-gray-950 text-white px-6 py-10 ">
            <div className="container mx-auto">
                <button onClick={() => router.back()} type="button" className="text-white bg-gradient-to-r from-purple-500 via-purple-600 to-purple-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-purple-300 dark:focus:ring-purple-800 font-medium rounded-4xl text-sm px-4 py-2.5 text-center leading-5 cursor-pointer">
                    Back</button>
                <p className="text-2xl font-bold">{track.track_name}</p>
                {track.album_image ? (
                            <Image
                                src={track.album_image}
                                alt={track.album}
                                width={300}
                                height={300}
                                className="rounded-lg"/>) : (
                            <div className="bg-gray-600 rounded-lg" />
                            )}
                <p className="text-gray-400 mt-1">{track.album}</p>
                <p className="text-gray-500 text-sm mt-1">{track.artist}</p>

                <button onClick={(e) => toggleFavourite(track, e)} type="button" className="bg-violet-500 hover:bg-violet-600 focus:outline-2 focus:outline-offset-2 focus:outline-violet-500 active:bg-violet-700 font-medium rounded  px-4 py-2.5 text-center leading-5 cursor-pointer mt-4 ">
                    {favouritedIds.has(track.track_id) ? '❤️' : '🤍'}</button>

                <div className="mt-6 rounded-lg overflow-hidden">
                    <iframe
                        src={track.embed_url}
                        width="100%"
                        height="80"
                        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"/>
                </div>

                {/* Lyrics Section */}
                <div className="relative mt-8">
                    {!showLyrics ? (
                        <button
                            onClick={fetchLyrics}
                            className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 cursor-pointer">
                            Show Lyrics
                        </button>
                    ) : loadingLyrics ? (
                        <div className="text-center py-8 flex items-center gap-3">
                            <div className="animate-spin h-5 w-5 border-2 border-purple-500 border-t-transparent rounded-full" />
                            <p className="text-gray-400">Loading lyrics</p>
                        </div>
                    ) : lyrics?.lyrics ? (
                        <div className="bg-gray-900 rounded-lg p-6">
                            <h3 className="text-2xl font-bold mb-4 text-purple-400">Lyrics</h3>
                            <div>
                                <button onClick={CloseLyrics} className='absolute top-3 right-3 cursor-pointer'>❌</button>
                            </div>
                            <div className="prose prose-invert max-w-none">
                                <pre className="whitespace-pre-wrap font-sans text-gray-300 leading-relaxed">
                                    {lyrics.lyrics}
                                </pre>
                            </div>
                            {lyrics.url && (
                                <a href={lyrics.url} 
                                target="_blank" 
                                rel="noopener noreferrer" 
                                className="inline-block mt-4 text-purple-400 hover:text-purple-300 transition-colors">
                                    View on Genius →
                                </a>
                            )}
                        </div>
                    ) : (
                        <div className="bg-yellow-900/50 border border-yellow-700 rounded-lg p-6 text-center">
                            <p className="text-yellow-300">
                                {lyrics?.error || "Lyrics not available for this song"}
                            </p>
                        </div>
                    )}
                </div>
                {/* Recommendations Section */}
                <div className="mt-10">
                    <h3 className="text-2xl font-bold mb-4 text-purple-400">Similar Songs</h3>

                    {loadingRecs ? (
                        <div className="flex items-center gap-3 py-8">
                            <div className="animate-spin h-5 w-5 border-2 border-purple-500 border-t-transparent rounded-full" />
                            <p className="text-gray-400">Finding similar songs</p>
                        </div>
                    ) : recsError ? (
                        <p className="text-red-400">{recsError}</p>
                    ) : recommendations.length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            {recommendations.map((rec) => (
                                <div
                                    key={rec.track_id}
                                    onClick={() => router.push(`/track/${rec.track_id}`)}
                                    className="bg-gray-900 hover:bg-gray-800 rounded-lg p-4 cursor-pointer transition-colors"
                                >
                                    <p className="font-semibold truncate">{rec.track_name}</p>
                                    <p className="text-gray-400 text-sm truncate">{rec.artists}</p>
                                    <p className="text-purple-400 text-xs mt-2">
                                        {(rec.similarity_score * 100).toFixed(1)}% match
                                    </p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-gray-500">No recommendations found.</p>
                    )}
                </div>
            </div>
        </main>
    );
}