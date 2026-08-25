'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/AuthContext';

export default function Navbar() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isNavOpen, setIsNavOpen] = useState(false);
  const { username, logout } = useAuth();

  return (
    <nav className="bg-gray-950 border-b border-gray-800">
      <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        {/* Logo */}
        <Link href="/" className="flex items-center">
          <span className="self-center text-2xl font-semibold text-white">
            Rec4Music
          </span>
        </Link>

        {/* Right side */}
        <div className="flex items-center md:order-2 space-x-3 relative">
          {username ? (
            <>
              <button
                type="button"
                className="flex items-center gap-2 text-sm bg-gray-800 rounded-full px-4 py-2
                           hover:bg-gray-700 transition cursor-pointer"
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}>
                <span className="text-white">{username}</span>
              </button>

              {isDropdownOpen && (
                <div className="absolute top-[52px] right-0 w-48 bg-gray-800 divide-y
                                 divide-gray-700 rounded-lg shadow-lg z-50">
                  <div className="px-4 py-3">
                    <span className="block text-sm text-white">Logged in as</span>
                    <span className="block text-sm text-gray-400 truncate">{username}</span>
                  </div>
                  <ul className="py-2">
                    <li>
                      <Link
                        href="/search"
                        className="block px-4 py-2 text-sm text-gray-200 hover:bg-gray-700"
                        onClick={() => setIsDropdownOpen(false)}>
                        Search for a new song
                      </Link>
                    </li>
                    <li>
                      <button
                        onClick={() => {
                          logout();
                          setIsDropdownOpen(false);
                        }}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-200
                                   hover:bg-gray-700 cursor-pointer">
                        Log out
                      </button>
                    </li>
                  </ul>
                </div>
              )}
            </>
          ) : (
            <div className="flex items-center gap-3">
              <Link
                href="/login"
                className="text-sm text-gray-300 hover:text-white transition"
              >
                Log in
              </Link>
              <Link
                href="/register"
                className="text-sm bg-purple-600 hover:bg-purple-700 text-white
                           px-4 py-2 rounded-lg transition"
              >
                Sign up
              </Link>
            </div>
          )}

          {/* Mobile hamburger */}
          <button
            type="button"
            className="inline-flex items-center p-2 w-10 h-10 text-gray-400 rounded-lg
                       md:hidden hover:bg-gray-800"
            onClick={() => setIsNavOpen(!isNavOpen)}
          >
            <span className="sr-only">Open main menu</span>
            <svg className="w-5 h-5" fill="none" viewBox="0 0 17 14">
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M1 1h15M1 7h15M1 13h15"
              />
            </svg>
          </button>
        </div>

        {/* Nav links */}
        <div className={`items-center ${isNavOpen ? 'block' : 'hidden'} w-full md:flex md:w-auto md:order-1`}>
          <ul className="flex flex-col font-medium p-4 md:p-0 mt-4 md:space-x-6 md:flex-row">
            <li>
              <Link
                href="/search"
                className="block py-2 px-3 text-gray-200 rounded-md hover:bg-gray-800
                           md:hover:bg-transparent md:hover:text-purple-400">
                Search
              </Link>
            </li>
            <li>
              <Link
                href="/FYP"
                className="block py-2 px-3 text-gray-200 rounded-md hover:bg-gray-800
                           md:hover:bg-transparent md:hover:text-purple-400">
                For You
              </Link>
            </li>
            <li>
              <Link
                href="/favourites"
                className="block py-2 px-3 text-gray-200 rounded-md hover:bg-gray-800
                           md:hover:bg-transparent md:hover:text-purple-400">
                Favourites
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}