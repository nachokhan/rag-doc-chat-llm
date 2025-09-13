import React, { useState } from 'react';
import FileUpload from './FileUpload';
import Chat from './Chat';
import './App.css';

function App() {
  const [docId, setDocId] = useState('');

  return (
    <div className="App">
      <header className="App-header">
        <h1>mini-docufi</h1>
      </header>
      <div className="container">
        <FileUpload setDocId={setDocId} />
        {docId && <Chat docId={docId} />}
      </div>
    </div>
  );
}

export default App;