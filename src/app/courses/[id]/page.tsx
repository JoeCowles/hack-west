'use client';
import React, { useState, useEffect } from 'react';
import Sidebar from "../../../../components/Sidebar";
import Cookies from 'js-cookie';
import { useRouter } from 'next/navigation';
import { usePathname } from 'next/navigation';

interface Lesson {
  id: string;
  description: string;
  video_id: string;
  quiz_id: string | null;
}

const LessonCard: React.FC<{ lesson: Lesson; onClick: () => void }> = ({ lesson, onClick }) => (
  <div 
    className="bg-gray-800 p-4 rounded-lg shadow-md cursor-pointer hover:bg-gray-700 transition-colors"
    onClick={onClick}
  >
    <h3 className="text-xl font-semibold mb-2">{lesson.description}</h3>
    {lesson.quiz_id && <p className="text-green-400">Quiz available</p>}
  </div>
);

const VideoPopup: React.FC<{ 
  videoId: string; 
  quizId: string | null; 
  onClose: () => void; 
  onQuizStart: () => void;
  showQuiz: boolean;
}> = ({ videoId, quizId, onClose, onQuizStart, showQuiz }) => (
  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div className="bg-gray-800 p-6 rounded-lg max-w-4xl w-full">
      {!showQuiz && (
        <>
          <iframe
            width="100%"
            height="480"
            src={`https://www.youtube.com/embed/${videoId}`}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
          <div className="mt-4 flex justify-between">
            <button 
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
              onClick={onClose}
            >
              Close
            </button>
            {quizId && (
              <button 
                className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                onClick={onQuizStart}
              >
                Take Quiz
              </button>
            )}
          </div>
        </>
      )}
      {showQuiz && quizId && <QuizPopup quizId={quizId} onClose={onClose} />}
    </div>
  </div>
);

interface Question {
  id: string;
  question: string;
  choices: string[];
  correct_answer: number;
}

const QuizPopup: React.FC<{ quizId: string; onClose: () => void }> = ({ quizId, onClose }) => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await fetch(`${apiUrl}/get-quiz?lesson_id=${quizId}`);
        const data = await response.json();
        setQuestions(data.questions);
        console.log(data.questions);
      } catch (error) {
        console.error("Error fetching quiz questions:", error);
      }
    };
    fetchQuestions();
  }, [quizId, apiUrl]);

  const handleAnswerSelect = (index: number) => {
    setSelectedAnswer(index);
    setIsCorrect(index === questions[currentQuestionIndex].correct_answer);
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSelectedAnswer(null);
      setIsCorrect(null);
    } else {
      onClose();
    }
  };

  if (questions.length === 0) {
    return <div>Loading quiz...</div>;
  }

  const currentQuestion = questions[currentQuestionIndex];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg max-w-2xl w-full">
        <h2 className="text-2xl font-bold mb-4">{currentQuestion.question}</h2>
        <div className="space-y-2">
          {currentQuestion.choices.map((choice, index) => (
            <button
              key={index}
              className={`w-full p-2 text-left rounded ${
                selectedAnswer === index
                  ? isCorrect
                    ? 'bg-green-500 text-white'
                    : 'bg-red-500 text-white'
                  : 'bg-gray-200 hover:bg-gray-300'
              }`}
              onClick={() => handleAnswerSelect(index)}
              disabled={selectedAnswer !== null}
            >
              {choice}
            </button>
          ))}
        </div>
        {selectedAnswer !== null && (
          <div className="mt-4">
            <p className={isCorrect ? 'text-green-600' : 'text-red-600'}>
              {isCorrect ? 'Correct!' : 'Incorrect. Try again!'}
            </p>
            <button
              className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              onClick={handleNextQuestion}
            >
              {currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'Finish Quiz'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

const Home = () => {
  const router = useRouter();
  const [user, setUser] = useState("");
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null);
  const [selectedQuiz, setSelectedQuiz] = useState<string | null>(null);
  const pathname = usePathname();
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const [showQuiz, setShowQuiz] = useState(false);

  useEffect(() => {
    const username = Cookies.get("username") || "";
    setUser(username);
    
    if (!username) {
      router.push('/login');
    }
  }, [router]);

  const courseId = pathname.split("/")[2];

  useEffect(() => {
    const fetchLessons = async () => {
      try {
        const response = await fetch(`${apiUrl}/get-lessons?syllabus_id=${courseId}`);
        const data = await response.json();
        setLessons(data.lessons);
      } catch (error) {
        console.error("Error fetching lessons:", error);
      }
    };
    fetchLessons();
  }, [courseId, apiUrl]);

  const handleLessonClick = (videoId: string) => {
    setSelectedVideo(videoId);
    setShowQuiz(false);
  };

  const closeVideo = () => {
    setSelectedVideo(null);
    setShowQuiz(false);
  };

  const startQuiz = () => {
    setShowQuiz(true);
  };

  const closeQuiz = () => {
    setSelectedQuiz(null);
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <Sidebar username={user ? user : ""}/>
      <div className="flex-1 overflow-auto p-8">
        <h1 className="text-3xl font-bold mb-6">Course Lessons</h1>
        <div className="flex flex-col space-y-4">
          {lessons.map((lesson) => (
            <LessonCard 
              key={lesson.id} 
              lesson={lesson} 
              onClick={() => handleLessonClick(lesson.video_id)}
            />
          ))}
        </div>
      </div>
      {selectedVideo && (
        <VideoPopup 
          videoId={selectedVideo} 
          quizId={lessons.find(lesson => lesson.video_id === selectedVideo)?.quiz_id || null}
          onClose={closeVideo} 
          onQuizStart={startQuiz}
          showQuiz={showQuiz}
        />
      )}
    </div>
  )
}

export default Home