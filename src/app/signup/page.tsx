import React from 'react'
import Link from 'next/link'

const LoginPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <div className="bg-gray-900 p-8 rounded-lg shadow-lg w-96">
        <h1 className="text-3xl font-bold mb-6 text-white text-center">Login</h1>
        <form>
          <div className="mb-4">
            <label htmlFor="email" className="block text-white mb-2">Email</label>
            <input
              type="text"
              id="username"
              className="w-full px-3 py-2 bg-gray-800 text-white rounded focus:outline-none focus:ring-2 focus:ring-red-600"
              placeholder="Enter your email"
            />
          </div>
          
          <div className="mb-4">
            <label htmlFor="email" className="block text-white mb-2">Confirm Email</label>
            <input
              type="text"
              id="username"
              className="w-full px-3 py-2 bg-gray-800 text-white rounded focus:outline-none focus:ring-2 focus:ring-red-600"
              placeholder="Confirm your email"
            />
          </div>
          <div className="mb-6">
            <label htmlFor="password" className="block text-white mb-2">Password</label>
            <input
              type="password"
              id="password"
              className="w-full px-3 py-2 bg-gray-800 text-white rounded focus:outline-none focus:ring-2 focus:ring-red-600"
              placeholder="Enter your password"
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

export default LoginPage