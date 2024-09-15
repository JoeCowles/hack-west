'use client';
import React, { useState, useEffect } from 'react';
import Chatbar from '../../../components/Chatbar';
import Sidebar from "../../../components/Sidebar";
import Cookies from 'js-cookie';
import { useRouter } from 'next/navigation';

interface Topic {
  id: string;
  topic: string;
}

const Home = () => {
  const router = useRouter();
  const [user, setUser] = useState("");
  const [topics, setTopics] = useState<Topic[]>([]);

  useEffect(() => {
    const username = Cookies.get("username") || "";
    setUser(username);
    
    if (!username) {
      router.push('/login');
    }
  }, [router]);

  useEffect(() => {
    // Fetch the topics from the database "/"
    //const topics = 
    //setTopics(topics);
  }, []);

  console.log("Username", user);

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <Sidebar username={user ? user : ""} topics={topics} />
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