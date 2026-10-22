import React from 'react'
import ReactDOM from 'react-dom/client'
import { Navbar, Nav, Container } from "react-bootstrap"
import App from './App.jsx'
import 'bootstrap/dist/css/bootstrap.min.css'
import './styles/style.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)