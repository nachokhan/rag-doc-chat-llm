import React, { useState } from 'react';

function MarketAnalysis() {
    const [query, setQuery] = useState('');
    const [taskId, setTaskId] = useState(null);
    const [progress, setProgress] = useState('');
    const [report, setReport] = useState('');
    const [error, setError] = useState('');

    const startAnalysis = async () => {
        if (!query) {
            alert('Please enter a query.');
            return;
        }

        setProgress('Starting analysis...');
        setReport('');
        setError('');
        setTaskId(null);

        try {
            const response = await fetch('/api/analysis/market', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });

            if (!response.ok) {
                throw new Error('Failed to start analysis.');
            }

            const data = await response.json();
            setTaskId(data.task_id);

            const eventSource = new EventSource(`/api/analysis/stream/${data.task_id}`);

            eventSource.addEventListener('progress', (e) => {
                setProgress(e.data);
            });

            eventSource.addEventListener('complete', (e) => {
                setReport(e.data);
                setProgress('Analysis complete.');
                eventSource.close();
            });

            eventSource.addEventListener('error', (e) => {
                setError('An error occurred during analysis.');
                setProgress('');
                eventSource.close();
            });

        } catch (err) {
            setError(err.message);
            setProgress('');
        }
    };

    return (
        <div className="market-analysis">
            <h2>Market Analysis</h2>
            <div className="analysis-controls">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Enter your market query..."
                />
                <button onClick={startAnalysis}>Generate Report</button>
            </div>
            {progress && <div className="progress-log">Status: {progress}</div>}
            {error && <div className="error-log">Error: {error}</div>}
            {report && (
                <div className="report-display">
                    <h3>Report</h3>
                    <pre>{report}</pre>
                </div>
            )}
        </div>
    );
}

export default MarketAnalysis;
