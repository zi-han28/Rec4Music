'use client';

import { useState } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';

interface Analysis{
content: string 
}


export default function ForYou(){
    const[loadingContent, setloadingContent] = usestate(true);
    return (
        <main>
            <p>For You Page</p>
        </main>
    );
}