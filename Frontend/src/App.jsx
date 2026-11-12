import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Logout from './pages/Logout'
import Register from './pages/register'
import Home from './pages/Home'
import NotFound from './pages/NotFound'
import Profile from './pages/Profile'
import Search from './pages/search'
import UserProfile from './pages/UserProfile'
import CreateCourses from './pages/CreateCourse'
import CourseDetail from './pages/CourseDetail'

import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import { ProfileProvider } from './components/ProfileContext'
import { NotificationProvider } from './components/Notifications'

function logout(){
  localStorage.clear()
  return <Navigate to="/login"></Navigate>
}

function RegisterAndLogout(){
  localStorage.clear()
  return <Register />
}

function App() {

  return (
    <BrowserRouter>
    <NotificationProvider>
        <ProfileProvider>
        <Routes>
          <Route element={<Layout/>}>
            <Route
              path="/"
              element={
                <ProtectedRoute>
                    <Home />
                </ProtectedRoute>
              }
            />
            {/* users routes */}
            <Route path="/users/search" element={<ProtectedRoute>< Search /></ProtectedRoute>}/> 
            <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>}/>
            <Route path="/users/:id" element={<ProtectedRoute><UserProfile /></ProtectedRoute>} />         
            <Route path="/login" element={<Login/>} />
            <Route path="/logout" element={<Logout/>}/>
            <Route path="/register" element={<Register/>}/> 

            {/* Courses routes */}
            <Route path="/courses/create" element={<ProtectedRoute>< CreateCourses /></ProtectedRoute>}/>
            <Route path="/courses/:slug" element={<ProtectedRoute><CourseDetail /></ProtectedRoute>}/>
            <Route path="*" element={<NotFound/>}></Route>
          </Route>
        </Routes>
        </ProfileProvider>
      </NotificationProvider>
    </BrowserRouter>
  )
}

export default App
