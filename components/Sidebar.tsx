import React from 'react'
import Link from 'next/link'
import { getUser } from '../hooks/getUser'
import Cookies from 'js-cookie';
import { useEffect, useState } from 'react';

// props for sidebar
interface Topic {
  id : string;
  topic : string;
}
interface SidebarProps {
  username: string;
}

const Sidebar = ({ username }: SidebarProps) => {
  const [syllabi, setSyllabi] = useState<Topic[]>([]);
  const userId = Cookies.get("user_id");
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  useEffect(() => {
    const fetchSyllabi = async () => {
      const response = await fetch(`${apiUrl}/get-courses?user_id=${userId}`);
      const data = await response.json();
      setSyllabi(data.syllabi);
    };
    fetchSyllabi();
  }, [userId]);

  return (
    <aside className="w-64 bg-black p-6 text-white animate-slideInFromLeft">
      <div className="mb-8">
        <h2 className="text-lg font-bold text-red-500 mb-4">{username}</h2>
      </div>
      <nav>
        <h3 className="font-bold mb-4 text-lg text-gray-300">Courses</h3>
        <ul className="space-y-2">
          {syllabi.map((syllabus) => (
            <li key={syllabus.id}>
              <Link href={`/courses/${syllabus.id}`} className="text-gray-400 hover:text-red-400 transition-colors duration-200">
                {syllabus.topic}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  )
}

export default Sidebar
