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

const phrases = [
  "Generating Syllabus",
  "Creating Lesson Plan",
  "Finding General Trends",
  "Scraping Lecture Videos",
  "Generating Quizzes"
];

const AnimatedPhrase = () => {
  const [currentPhraseIndex, setCurrentPhraseIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentPhraseIndex((prevIndex) => (prevIndex + 1) % phrases.length);
    }, 20000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-8 overflow-hidden">
      <div className="animate-slide-up">
        {phrases.map((phrase, index) => (
          <div key={index} className="h-8">
            {currentPhraseIndex === index && phrase}
          </div>
        ))}
      </div>
    </div>
  );
};

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
      <Sidebar username={user ? user : ""}/>
      <main className="flex-1 p-8 overflow-hidden animate-fadeIn flex flex-col">
        <div className="flex-grow flex flex-col items-center justify-center space-y-64 -mt-16">
          <h2 className="text-center font-bold text-4xl bg-gradient-to-r from-red-600 via-pink-500 to-red-600 text-transparent bg-clip-text bg-300% animate-shimmer">
            What would you like to learn today?
          </h2>
          <Chatbar className="w-full max-w-2xl" />
          <AnimatedPhrase />
        </div>
      </main>
    </div>
  )
}

export default Home