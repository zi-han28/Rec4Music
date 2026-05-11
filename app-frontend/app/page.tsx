'use client';

import { useState } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';

interface Track {
  track_id: string;
  track_name: string;
  artist: string;
  album: string;
  album_image: string | null;
}

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Track[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError('');

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/search?q=${encodeURIComponent(query)}`
      );
      if (!res.ok) throw new Error('Search failed');
      const data = await res.json();
      setResults(data.results);
    } catch (e) {
      setError('Search failed. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white px-6 py-10">
      <h1 className="text-3xl font-bold mb-8">🎵 Music Search</h1>

      {/* Search bar */}
      <div className="flex gap-3 mb-8">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          placeholder="Search for a song..."
          className="flex-1 bg-gray-800 rounded-lg px-4 py-3 text-white 
                     placeholder-gray-400 focus:outline-none focus:ring-2 
                     focus:ring-green-500"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="bg-green-500 hover:bg-green-400 text-black font-semibold 
                     px-6 py-3 rounded-lg disabled:opacity-50 transition"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {/* Error */}
      {error && (
        <p className="text-red-400 mb-4">{error}</p>
      )}

      {/* Results */}
      <div className="flex flex-col gap-4">
        {results.map((track) => (
          <div
            key={track.track_id}
            className="flex items-center gap-4 bg-gray-800 rounded-xl p-4 
                       hover:bg-gray-700 transition cursor-pointer"
            onClick={() => router.push(`/track/${track.track_id}`)}
          >
            {track.album_image ? (
              <Image
                src={track.album_image}
                alt={track.album}
                width={64}
                height={64}
                className="rounded-lg"
              />
            ) : (
              <div className="w-16 h-16 bg-gray-600 rounded-lg" />
            )}
            <div className="flex-1 min-w-0">
              <p className="font-semibold truncate">{track.track_name}</p>
              <p className="text-gray-400 text-sm truncate">{track.artist}</p>
              <p className="text-gray-500 text-xs truncate">{track.album}</p>
            </div>
            <span className="text-gray-400 text-sm">→</span>
          </div>
        ))}
      </div>
    </main>
  );
}