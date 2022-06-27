import React from 'react'
import Postform from './components/PostForm'
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import FileUpload from './components/FileUpload'
import axios from 'axios';

function App() {
  return (
    <div>
      <Postform />
      <FileUpload />
    </div>
  )
}

export default App;