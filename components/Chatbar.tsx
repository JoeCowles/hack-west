'use client';
import React, { useState } from 'react'
import { IoSend } from 'react-icons/io5'
import Cookies from 'js-cookie'

const Chatbar = () => {
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const userId = Cookies.get('user_id');
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return;

    setIsLoading(true);

    try {
      // Simulating API call
      //await new Promise(resolve => setTimeout(resolve, 2000));
      // Here you would typically make your actual API call
      const response = await fetch(`${apiUrl}/create-course?prompt=${input}&user_id=${userId}`, { method: 'POST'});
      if (!response.ok) throw new Error('Failed to send message');

      setInput('');
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className={`fixed left-0 right-0 transition-all duration-500 ease-in-out ${isLoading ? 'top-0' : 'bottom-0'}`}>
      <div className="w-full max-w-3xl mx-auto p-4">
        <form onSubmit={handleSubmit} className="relative">
          <div className="relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="w-full px-4 py-2 bg-gray-800 text-white border border-gray-700 rounded-full focus:outline-none focus:ring-2 pr-12"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="absolute right-1 top-1/2 -translate-y-1/2 text-red-500 hover:text-red-600 transition-colors duration-200 rounded-full p-2"
              aria-label="Send message"
              disabled={isLoading}
            >
              <IoSend size={20} />
            </button>
          </div>
        </form>
        {isLoading && (
          <div className="mt-4 h-2 w-full bg-gray-700 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-red-500 via-pink-500 to-red-500 animate-shimmer bg-300%"></div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Chatbar