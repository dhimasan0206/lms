"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export default function Dashboard() {
  const [user, setUser] = useState({
    name: "John Doe",
    email: "john.doe@example.com",
    role: "student",
  });
  
  const [courses, setCourses] = useState([
    {
      id: 1,
      title: "Introduction to Web Development",
      progress: 35,
      nextLesson: "CSS Layouts"
    },
    {
      id: 2,
      title: "Data Science Fundamentals",
      progress: 12,
      nextLesson: "Statistical Analysis"
    },
    {
      id: 3,
      title: "Mobile App Development",
      progress: 0,
      nextLesson: "Getting Started with React Native"
    }
  ]);

  // Simulate fetching user data
  useEffect(() => {
    // In a real app, this would be an API call
    console.log("Fetching user data...");
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="py-10">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          {/* Dashboard Header */}
          <div className="bg-white shadow rounded-lg p-6 mb-8">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Welcome, {user.name}</h1>
                <p className="text-gray-500">Let's continue your learning journey</p>
              </div>
              <div className="mt-4 md:mt-0">
                <Link
                  href="/courses"
                  className="bg-blue-600 text-white px-4 py-2 rounded-md font-medium hover:bg-blue-700 transition-colors"
                >
                  Browse All Courses
                </Link>
              </div>
            </div>
          </div>

          {/* Main Dashboard Content */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* In Progress Courses */}
            <div className="lg:col-span-2">
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-6">My Courses</h2>
                
                {courses.length > 0 ? (
                  <div className="space-y-6">
                    {courses.map((course) => (
                      <div key={course.id} className="border rounded-lg p-4">
                        <div className="flex justify-between items-start mb-3">
                          <h3 className="text-md font-medium">{course.title}</h3>
                          <span className="text-sm bg-blue-100 text-blue-800 py-1 px-2 rounded-full">
                            {course.progress}% Complete
                          </span>
                        </div>
                        
                        {/* Progress Bar */}
                        <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4">
                          <div
                            className="bg-blue-600 h-2.5 rounded-full"
                            style={{ width: `${course.progress}%` }}
                          ></div>
                        </div>
                        
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-500">
                            Next: {course.nextLesson}
                          </span>
                          <Link
                            href={`/courses/${course.id}`}
                            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                          >
                            Continue Learning →
                          </Link>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-10">
                    <p className="text-gray-500 mb-4">You haven't enrolled in any courses yet.</p>
                    <Link
                      href="/courses"
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      Explore Courses
                    </Link>
                  </div>
                )}
              </div>
            </div>

            {/* Dashboard Sidebar */}
            <div className="space-y-8">
              {/* Profile Card */}
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Profile</h2>
                <div className="flex items-center space-x-4">
                  <div className="flex-shrink-0">
                    <div className="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center">
                      <span className="text-blue-800 font-bold text-lg">
                        {user.name.charAt(0)}
                      </span>
                    </div>
                  </div>
                  <div>
                    <p className="font-medium">{user.name}</p>
                    <p className="text-sm text-gray-500">{user.email}</p>
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <Link
                    href="/profile"
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    View Profile Settings →
                  </Link>
                </div>
              </div>

              {/* Upcoming Events */}
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Upcoming Events</h2>
                <div className="space-y-4">
                  <div className="border-l-4 border-blue-500 pl-3">
                    <p className="font-medium">Web Development Q&A</p>
                    <p className="text-sm text-gray-500">Tomorrow, 6:00 PM</p>
                  </div>
                  <div className="border-l-4 border-blue-500 pl-3">
                    <p className="font-medium">Data Science Workshop</p>
                    <p className="text-sm text-gray-500">July 15, 4:30 PM</p>
                  </div>
                </div>
                <div className="mt-4">
                  <Link
                    href="/events"
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    View All Events →
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
} 