'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';


export default function ForYou(){
    const [analysis , setAnalysis] = useState<string | null>(null);
    const [message, setMessage] = useState('')
    const [loadingContent, setloadingContent] = useState(true);
    const [generating, setGenerating] = useState(true);
    const [error, setError] = useState('')
    const router = useRouter();

    const loadCached = async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            router.push('/login');
            return;
        }
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/FYP/analysis`, {headers: { Authorization: `Bearer ${token}` }});
            if (res.status === 401) {
                localStorage.removeItem('access_token');
                router.push('/login');
                return;
            }
            if (!res.ok) {
                const errData = await res.json().catch(() => null);
                throw new Error(errData?.detail || 'Failed to load analysis');
            }
            const data = await res.json();
            setAnalysis(data.music_analysis ?? null);
            setMessage(data.message ?? '');
        }catch (e) {
            setError(e instanceof Error ? e.message : 'Could not load your analysis.');
        } finally {
            setloadingContent(false);
        }
    };

    useEffect(()=>{
        loadCached();
    },[router])

    const handleGenerate = async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            router.push('/login');
            return;
        }
        setGenerating(true);
        setError('');
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/FYP/analysis/generate`, {method: 'POST', headers: { Authorization: `Bearer ${token}` }});
            if (res.status === 401) {
                localStorage.removeItem('access_token');
                router.push('/login');
                return;
            }
            if (!res.ok) {
                const errData = await res.json().catch(() => null);
                throw new Error(errData?.detail || 'Failed to generate analysis');
            }
            const data = await res.json();
            setAnalysis(data.music_analysis);
            setMessage('');
        }catch(e){
            setError(e instanceof Error ? e.message : 'Could not generate your analysis.');
        }finally{
            setGenerating(false);
        }
    }
    return (
        <main className="min-h-screen bg-gray-950 text-white px-6 py-10">
            <div className="container mx-auto max-w-2xl">
                <h1 className="text-3xl font-bold mb-8">🎯 For You</h1>

                {loadingContent ? (
                    <div className="flex items-center gap-3">
                        <div className="animate-spin h-5 w-5 border-2 border-purple-500 border-t-transparent rounded-full" />
                            <p className="text-gray-400">Analysing your taste...</p>
                        </div>
                        ) : (
                            <>
                            {error && <p className="text-red-400 mb-4">{error}</p>}
                            {analysis ? (
                                <div className="bg-gray-900 rounded-xl p-6 mb-6">
                                    <h2 className="text-xl font-semibold text-purple-400 mb-3">
                                        Your listening personality
                                    </h2>
                                    <p className="text-gray-300 leading-relaxed">{analysis}</p>
                                </div>
                                ):(
                                    <p className="text-gray-500 mb-6">{message || 'No analysis generated yet.'}</p>
                                )}
                                <button onClick={handleGenerate} disabled={generating} className="bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white font-semibold px-6 py-3 rounded-lg transition-colors cursor-pointer flex items-center gap-2">
                                    {generating && (<div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />)}
                                    {generating ? 'Generating...' : analysis ? '🔄 Regenerate' : '✨ Generate'}
                                </button>
                                </>
                                )}
            </div>
        </main>
    );
}