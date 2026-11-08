import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/login'
import Logout from './pages/Logout'
import Register from './pages/register'
import Home from './pages/home'
import NotFound from './pages/NotFound'
import Profile from './pages/Profile'
import Search from './pages/search'
import UserProfile from './pages/UserProfile'

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
            <Route path="/users/search" element={<ProtectedRoute>< Search /></ProtectedRoute>}/> 
            <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>}/>
            <Route path="/users/:id" element={<ProtectedRoute><UserProfile /></ProtectedRoute>} />         
            <Route path="/login" element={<Login/>} />
            <Route path="/logout" element={<Logout/>}/>
            <Route path="/register" element={<Register/>}/> 
            <Route path="*" element={<NotFound/>}></Route>
          </Route>
        </Routes>
        </ProfileProvider>
      </NotificationProvider>
    </BrowserRouter>
  )
}

export default App
