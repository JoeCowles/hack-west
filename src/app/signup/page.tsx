'use client';
import React, { useState } from 'react'
import Link from 'next/link'
import { getUser } from '../../../hooks/getUser'

const SignupPage = () => {
  const [email, setEmail] = useState('')
  const [confirmEmail, setConfirmEmail] = useState('')
  const [password, setPassword] = useState('')
  const { signup } = getUser()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (email !== confirmEmail) {
      alert('Emails do not match')
      return
    }
    await signup(email, password)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <div className="bg-gray-900 p-8 rounded-lg shadow-lg w-96">
        <h1 className="text-3xl font-bold mb-6 text-white text-center">Register</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="email" className="block text-white mb-2">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 bg-gray-800 text-white rounded focus:outline-none focus:ring-2 focus:ring-red-600"
              placeholder="Enter your email"
              required
            />
          </div>
          
          <div className="mb-4">
            <label htmlFor="confirmEmail" className="block text-white mb-2">Confirm Email</label>
            <input
              type="email"
              id="confirmEmail"
              value={confirmEmail}
              onChange={(e) => setConfirmEmail(e.target.value)}
              className="w-full px-3 py-2 bg-gray-800 text-white rounded focus:outline-none focus:ring-2 focus:ring-red-600"
              placeholder="Confirm your email"
              required
            />
          </div>
          <div className="mb-6">
            <label htmlFor="password" className="block text-white mb-2">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 bg-gray-800 text-white rounded focus:outline-none focus:ring-2 focus:ring-red-600"
              placeholder="Enter your password"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700 transition duration-300"
          >
            Sign up
          </button>
        </form>
        <p className="mt-4 text-center text-gray-400">
          Already have an account?{' '}
          <Link href="/login" className="text-red-500 hover:text-red-400">
            Log in
          </Link>
        </p>
      </div>
    </div>
  )
}

export default SignupPage