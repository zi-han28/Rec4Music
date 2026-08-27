'use client';

import { useState } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';

export default function homePage() {

  return ( 
    <main className="min-h-screen bg-gray-950 text-white px-6 py-10">
      <h1 className="text-3xl font-bold">What is Rec4Music?</h1>
      <p className='text-xl'>It's a Final year project I made, that is currently being improved on to include better technology and slower loading time fo rrecommendations</p>
    </main>
  );
}