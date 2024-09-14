'use client';
import React from 'react'
import Chatbar from '../../../components/Chatbar'
import Sidebar from "../../../components/Sidebar"
import { getUser } from '../../../hooks/getUser'
import { useState, useEffect } from 'react';

const Home = () => {
  const [user, setUser] = useState<string | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      const { username } = await getUser();
      setUser(username);
    };
    fetchUser();
  }, []);

  console.log("Username", user)
  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <Sidebar username={user ? user : ""} />
      <main className="flex-1 p-8 overflow-hidden animate-fadeIn flex justify-center items-center h-screen">
        <div className="animate-slideInFromBottom">
          <h2 className="text-center font-bold text-2xl mb-6 bg-gradient-to-r from-red-400 via-pink-500 text-transparent bg-clip-text bg-300% animate-shimmer">
            What would you like to learn today?
          </h2>
          <Chatbar />
        </div>
      </main>
    </div>
  )
}

export default Home