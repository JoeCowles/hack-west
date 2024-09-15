'use client';
import React, { useState } from 'react'
import { IoSend } from 'react-icons/io5'
import Cookies from 'js-cookie'

const Chatbar = () => {
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    const userId = Cookies.get('user_id')

    console.log(userId)
    if (!userId) {
      console.error('User ID not found')
      console.log(userId)
      setIsLoading(false)
      return
    }

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/create-course`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${userId}`,
        },
        body: JSON.stringify({ prompt: input }),
      })

      if (response.ok) {
        const data = await response.json()
        console.log('Course created:', data)
        // Handle successful course creation (e.g., show a success message, update UI)
      } else {
        console.error('Failed to create course')
        // Handle error (e.g., show error message)
      }
    } catch (error) {
      console.error('Error creating course:', error)
      // Handle error (e.g., show error message)
    } finally {
      setIsLoading(false)
      setInput('')
    }
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
            disabled={isLoading}
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 text-red-500 hover:text-red-600 transition-colors duration-200 rounded-full p-1"
            aria-label="Send message"
            disabled={isLoading}
          >
            <IoSend size={20} />
          </button>
        </div>
      </form>
    </div>
  )
}

export default Chatbar