import Image from "next/image";
import Link from "next/link";

export default function Home() {
  // Sample course data
  const featuredCourses = [
    {
      id: 1,
      title: "Introduction to Web Development",
      description: "Learn the basics of HTML, CSS, and JavaScript to build your first website.",
      instructor: "John Smith",
      duration: "8 weeks",
      level: "Beginner",
      image: "/images/web-dev.jpg"
    },
    {
      id: 2,
      title: "Data Science Fundamentals",
      description: "Master the essential concepts of data analysis, visualization, and machine learning.",
      instructor: "Emma Johnson",
      duration: "10 weeks",
      level: "Intermediate",
      image: "/images/data-science.jpg"
    },
    {
      id: 3,
      title: "Mobile App Development",
      description: "Build cross-platform mobile applications using React Native.",
      instructor: "Alex Chen",
      duration: "12 weeks",
      level: "Intermediate",
      image: "/images/mobile-dev.jpg"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header/Hero Section */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white pt-4">
        <div className="container mx-auto px-4 py-16 sm:py-24">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div>
              <h1 className="text-4xl sm:text-5xl font-bold mb-4">
                Expand Your Knowledge with Our Online Courses
              </h1>
              <p className="text-xl mb-8 opacity-90">
                Access high-quality courses taught by industry experts. Learn at your own pace and advance your career.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link href="/courses" className="bg-white text-blue-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors">
                  Browse Courses
                </Link>
                <Link href="/signup" className="bg-transparent border-2 border-white px-6 py-3 rounded-lg font-medium hover:bg-white/10 transition-colors">
                  Sign Up Free
                </Link>
              </div>
            </div>
            <div className="hidden md:flex justify-end">
              <div className="relative w-full max-w-md h-80">
                {/* Placeholder for hero image - replace with your actual image */}
                <div className="absolute inset-0 bg-white/20 rounded-lg flex items-center justify-center">
                  <span className="text-lg font-medium">Hero Image Placeholder</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Features Section */}
      <section className="py-16 bg-white dark:bg-gray-800">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 dark:text-white">Why Choose Our Platform</h2>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
            <div className="p-6 rounded-lg border border-gray-100 dark:border-gray-700 shadow-sm dark:bg-gray-700">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600 dark:text-blue-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 dark:text-white">Expert Instructors</h3>
              <p className="text-gray-600 dark:text-gray-300">Learn from industry professionals with years of experience in their respective fields.</p>
            </div>
            
            <div className="p-6 rounded-lg border border-gray-100 dark:border-gray-700 shadow-sm dark:bg-gray-700">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600 dark:text-blue-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 dark:text-white">Flexible Learning</h3>
              <p className="text-gray-600 dark:text-gray-300">Study at your own pace with lifetime access to course materials and resources.</p>
            </div>
            
            <div className="p-6 rounded-lg border border-gray-100 dark:border-gray-700 shadow-sm dark:bg-gray-700">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600 dark:text-blue-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 dark:text-white">Certification</h3>
              <p className="text-gray-600 dark:text-gray-300">Earn certificates upon course completion to showcase your newly acquired skills.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Courses */}
      <section className="py-16 bg-gray-50 dark:bg-gray-800">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center mb-12">
            <h2 className="text-3xl font-bold dark:text-white">Featured Courses</h2>
            <Link href="/courses" className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium">
              View All Courses →
            </Link>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredCourses.map((course) => (
              <div key={course.id} className="bg-white dark:bg-gray-700 rounded-lg overflow-hidden shadow-sm border border-gray-100 dark:border-gray-600">
                <div className="h-48 bg-gray-200 dark:bg-gray-600 relative">
                  {/* Course image placeholder */}
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-gray-500 dark:text-gray-300">Course Image</span>
                  </div>
                </div>
                <div className="p-6">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-blue-600 dark:text-blue-300 bg-blue-50 dark:bg-blue-900/30 px-3 py-1 rounded-full">
                      {course.level}
                    </span>
                    <span className="text-sm text-gray-500 dark:text-gray-400">{course.duration}</span>
                  </div>
                  <h3 className="text-xl font-bold mb-2 dark:text-white">{course.title}</h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-4">{course.description}</p>
                  <div className="flex items-center text-sm text-gray-500 dark:text-gray-400 mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <span>Instructor: {course.instructor}</span>
                  </div>
                  <Link href={`/courses/${course.id}`} className="block text-center bg-blue-600 hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600 text-white py-2 rounded-lg transition-colors">
                    View Course
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 bg-white dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 dark:text-white">What Our Students Say</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg border border-gray-100 dark:border-gray-700">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gray-300 dark:bg-gray-600 rounded-full mr-4"></div>
                <div>
                  <h4 className="font-medium dark:text-white">Sarah Johnson</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Web Development Student</p>
                </div>
              </div>
              <p className="text-gray-600 dark:text-gray-300">
                "The courses are well-structured and the instructors are knowledgeable. I've learned so much in just a few weeks!"
              </p>
            </div>
            
            <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg border border-gray-100 dark:border-gray-700">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gray-300 dark:bg-gray-600 rounded-full mr-4"></div>
                <div>
                  <h4 className="font-medium dark:text-white">Michael Thompson</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Data Science Student</p>
                </div>
              </div>
              <p className="text-gray-600 dark:text-gray-300">
                "The hands-on projects helped me apply what I learned immediately. I now feel confident in my abilities as a data analyst."
              </p>
            </div>
            
            <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg border border-gray-100 dark:border-gray-700">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gray-300 dark:bg-gray-600 rounded-full mr-4"></div>
                <div>
                  <h4 className="font-medium dark:text-white">Lisa Chen</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Mobile Development Student</p>
                </div>
              </div>
              <p className="text-gray-600 dark:text-gray-300">
                "The support from instructors is amazing. Whenever I got stuck, they were there to help me understand and move forward."
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 bg-blue-600 dark:bg-blue-800 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Start Learning?</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto opacity-90">
            Join thousands of students who are already enhancing their skills and advancing their careers.
          </p>
          <Link href="/signup" className="inline-block bg-white text-blue-700 dark:text-blue-800 px-8 py-4 rounded-lg font-medium text-lg hover:bg-gray-100 transition-colors">
            Get Started Today
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 dark:bg-gray-950 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-lg font-bold mb-4">LMS Platform</h3>
              <p className="text-gray-400">Providing quality education accessible to everyone, anywhere in the world.</p>
            </div>
            
            <div>
              <h3 className="text-lg font-bold mb-4">Quick Links</h3>
              <ul className="space-y-2">
                <li><Link href="/courses" className="text-gray-400 hover:text-white transition-colors">Courses</Link></li>
                <li><Link href="/instructors" className="text-gray-400 hover:text-white transition-colors">Instructors</Link></li>
                <li><Link href="/about" className="text-gray-400 hover:text-white transition-colors">About Us</Link></li>
                <li><Link href="/contact" className="text-gray-400 hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-bold mb-4">Categories</h3>
              <ul className="space-y-2">
                <li><Link href="/category/web-development" className="text-gray-400 hover:text-white transition-colors">Web Development</Link></li>
                <li><Link href="/category/data-science" className="text-gray-400 hover:text-white transition-colors">Data Science</Link></li>
                <li><Link href="/category/mobile-development" className="text-gray-400 hover:text-white transition-colors">Mobile Development</Link></li>
                <li><Link href="/category/design" className="text-gray-400 hover:text-white transition-colors">Design</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-bold mb-4">Connect With Us</h3>
              <div className="flex space-x-4 mb-4">
                <a href="#" className="text-gray-400 hover:text-white transition-colors">
                  <span className="sr-only">Facebook</span>
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd" />
                  </svg>
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors">
                  <span className="sr-only">Twitter</span>
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                  </svg>
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors">
                  <span className="sr-only">Instagram</span>
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clipRule="evenodd" />
                  </svg>
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors">
                  <span className="sr-only">YouTube</span>
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M19.812 5.418c.861.23 1.538.907 1.768 1.768C21.998 8.746 22 12 22 12s0 3.255-.418 4.814a2.504 2.504 0 0 1-1.768 1.768c-1.56.419-7.814.419-7.814.419s-6.255 0-7.814-.419a2.505 2.505 0 0 1-1.768-1.768C2 15.255 2 12 2 12s0-3.255.417-4.814a2.507 2.507 0 0 1 1.768-1.768C5.744 5 11.998 5 11.998 5s6.255 0 7.814.418ZM15.194 12 10 15V9l5.194 3Z" clipRule="evenodd" />
                  </svg>
                </a>
              </div>
              <p className="text-gray-400 text-sm">© {new Date().getFullYear()} LMS Platform. All rights reserved.</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
