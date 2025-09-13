import React, { useState, useEffect } from 'react';

function DocumentList({ setDocId, documents, fetchDocuments }) {

  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <div>
      <h2>Select a Document to Chat With</h2>
      <select onChange={(e) => setDocId(e.target.value)}>
        <option value="">Select a document</option>
        {documents.map((doc) => (
          <option key={doc.id} value={doc.id}>
            {doc.filename}
          </option>
        ))}
      </select>
    </div>
  );
}

export default DocumentList;
