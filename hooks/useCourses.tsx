'use client';

import { useState, useEffect } from 'react';

interface Course {
  id: string;
  title: string;
}

export function useCourses() {
  const [courses, setCourses] = useState<Course[]>([]);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await fetch('/api/get-courses');
        if (response.ok) {
          const data = await response.json();
          setCourses(data.courses);
        } else {
          throw new Error('Failed to fetch courses');
        }
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    };

    fetchCourses();
  }, []);

  return { courses };
}
