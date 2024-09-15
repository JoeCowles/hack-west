'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';
import { btoa } from 'buffer';

const api_url = process.env.NEXT_PUBLIC_API_URL;


export function getUser() {

  
  const [userId, setUserId] = useState<string | null>(null);
  const [username, setUsername] = useState<string | null>(null);

  const router = useRouter();

  useEffect(() => {
    const storedUserId = Cookies.get('user_id');
    const storedUsername = Cookies.get('username');
    if (storedUserId && storedUsername) {
      setUserId(storedUserId);
      setUsername(storedUsername);
    } else {
      router.push('/login');
    }
  }, [router]);

  const login = async (email: string, password: string) => {
    try {
      const pass_hash = password; // Simple base64 encoding for demonstration
      console.log(`${api_url}/login?email=${encodeURIComponent(email)}&pass_hash=${encodeURIComponent(pass_hash)}`);
      const response = await fetch(`${api_url}/login?email=${encodeURIComponent(email)}&pass_hash=${encodeURIComponent(pass_hash)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Setting user id and username");
        console.log(data.user_id);
        console.log(email);
        setUserId(data.user_id);
        setUsername(email);
        Cookies.set('user_id', data.user_id, { expires: 7 }); // Expires in 7 days
        Cookies.set('username', email, { expires: 7 });
        console.log("User logged in");
        console.log(data.user_id);
        console.log(data.username);
        
        router.push('/home');
      } else {
        throw new Error('Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const signup = async (email: string, password: string) => {
    try {
      const pass_hash = password; // Simple encoding for demonstration
      const response = await fetch(`${api_url}/signup?email=${encodeURIComponent(email)}&pass_hash=${encodeURIComponent(pass_hash)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      if (response.ok) {
        const data = await response.json();
        setUserId(data.user_id);
        setUsername(email);
        console.log(data.user_id);
        Cookies.set('user_id', data.user_id, { expires: 7 });
        router.push('/home');
      } else {
        console.log(response);
        throw new Error('Signup failed');
      }
    } catch (error) {
      console.error('Signup error:', error);
    }
  };

  const logout = () => {
    Cookies.remove('user_id');
    Cookies.remove('username');
    setUserId(null);
    setUsername(null);
    router.push('/');
  };

  return { userId, username, login, signup, logout };
}
