'use client';
import React, { useState } from 'react'

const Chatbar = () => {
  const [input, setInput] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Chat input:', input)
    setInput('')
  }

  return (
    <form onSubmit={handleSubmit} className="flex animate-fadeIn">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder=""
        className="w-full px-4 py-3 bg-gray-800 text-white border border-gray-700 rounded-full focus:outline-none focus:ring-2 focus:ring-red-500 transition-all duration-200"
      />
 
    </form>
  )
}

export default Chatbar
