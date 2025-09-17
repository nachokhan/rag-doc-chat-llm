import React, { useState } from 'react';
import FileUpload from './FileUpload';
import Chat from './Chat';
import DocumentList from './DocumentList';
import MarketAnalysis from './MarketAnalysis';
import './App.css';

function App() {
  const [docId, setDocId] = useState('');
  const [documents, setDocuments] = useState([]);

  const fetchDocuments = async () => {
    try {
      const response = await fetch('/api/documents/');
      if (!response.ok) {
        throw new Error('Failed to fetch documents');
      }
      const data = await response.json();
      setDocuments(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>mini-docufi</h1>
      </header>
      <div className="container">
        <div className="document-section">
          <FileUpload setDocId={setDocId} onUploadSuccess={fetchDocuments} />
          <DocumentList setDocId={setDocId} documents={documents} fetchDocuments={fetchDocuments} />
          {docId && <Chat docId={docId} />}
        </div>
        <div className="analysis-section">
          <MarketAnalysis />
        </div>
      </div>
    </div>
  );
}

export default App;
