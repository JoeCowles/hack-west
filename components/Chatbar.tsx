'use client';
import React, { useState } from 'react'
import { IoSend } from 'react-icons/io5'

const Chatbar = () => {
  const [input, setInput] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Chat input:', input)
    setInput('')
  }

  return (
    <div className="w-full max-w-3xl mx-auto">
      <form onSubmit={handleSubmit} className="flex items-center">
        <div className="relative w-full">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="w-full px-4 py-2 bg-gray-800 text-white border border-gray-700 rounded-full focus:outline-none focus:ring-2 focus:ring-red-500 pr-12"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 text-red-500 hover:text-red-600 transition-colors duration-200 rounded-full p-1"
            aria-label="Send message"
          >
            <IoSend size={20} />
          </button>
        </div>
      </form>
    </div>
  )
}

export default Chatbar