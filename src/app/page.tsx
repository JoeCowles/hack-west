import Image from "next/image";

interface FeatureCardProps {
  title: string;
  description: string;
  icon: string;
}

function FeatureCard({ title, description, icon }: FeatureCardProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p>{description}</p>
    </div>
  );
}

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center">
        <video
          className="absolute inset-0 w-full h-full object-cover"
          autoPlay
          loop
          muted
          playsInline
        >
          <source src="/hero-video.mp4" type="video/mp4" />
        </video>
        <div className="relative z-10 text-center text-white">
          <h1 className="text-5xl font-bold mb-4">YoutubeStudyPlan.co</h1>
          <p className="text-xl font-bold">Learn anything, anywhere, anytime</p>
          <p className="text-xl mb-8 font-bold">Custom lession plans for any topic</p>
            <button className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
              Get Started
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-100 text-black">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard
              title="Custom Syllabus"
              description="Generate a personalized learning plan for any topic"
              icon="📚"
            />
            <FeatureCard
              title="Video Lectures"
              description="Access curated YouTube videos as your course material"
              icon="🎥"
            />
            <FeatureCard
              title="Quizzes & Tests"
              description="Reinforce your learning with interactive assessments"
              icon="✅"
            />
          </div>
        </div>
      </section>

      {/* About Us Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-8">About Us</h2>
          <p className="text-center max-w-2xl mx-auto">
            YoutubeStudyPlan.co is dedicated to revolutionizing online learning. 
            We combine the vast resources of YouTube with cutting-edge AI to create 
            personalized learning experiences for everyone, anywhere, anytime.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <Image src="/logo.png" alt="YoutubeStudyPlan.co Logo" width={150} height={50} />
            </div>
            <nav>
              <ul className="flex space-x-4">
                <li><a href="#" className="hover:text-gray-300">Home</a></li>
                <li><a href="#" className="hover:text-gray-300">Features</a></li>
                <li><a href="#" className="hover:text-gray-300">About</a></li>
                <li><a href="#" className="hover:text-gray-300">Contact</a></li>
              </ul>
            </nav>
          </div>
          <div className="mt-8 text-center">
            <p>&copy; 2023 YoutubeStudyPlan.co. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </main>
  );
}
