import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/login'
import Logout from './pages/Logout'
import Register from './pages/register'
import Home from './pages/home'
import NotFound from './pages/NotFound'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'

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
          <Route path="/profile" element={<ProtectedRoute><Profile/></ProtectedRoute>}/>
          
          <Route path="/login" element={<Login/>} />
          <Route path="/logout" element={<Logout/>}/>
          <Route path="/register" element={<RegisterAndLogout/>}/> 
          <Route path="*" element={<NotFound/>}></Route>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
