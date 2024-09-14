import React from 'react'
import Link from 'next/link'
import { getUser } from '../hooks/getUser'

// props for sidebar
interface SidebarProps {
  username: string;
}

const Sidebar = ({ username }: SidebarProps) => {
  return (
    <aside className="w-64 bg-black p-6 text-white animate-slideInFromLeft">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-red-500 mb-4">{username}</h2>
      </div>
      <nav>
        <h3 className="font-bold mb-4 text-lg text-gray-300">Courses</h3>
        <ul className="space-y-2">
          <li>
            <Link href="/courses/1" className="text-gray-400 hover:text-red-400 transition-colors duration-200">
              Course 1
            </Link>
          </li>
          {/* Add more course links as needed */}
        </ul>
      </nav>
    </aside>
  )
}

export default Sidebar
