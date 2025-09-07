import React, { useState } from 'react';
import './CreateModelForm.css'; // Don't forget to import the CSS!

function CreateModelForm({ onCancelForm }) {
    const [files, setFiles] = useState<FileList | null>(null);
    const [status, setStatus] = useState<
        'initial' | 'uploading' | 'success' | 'fail'
    >('initial');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
        setStatus('initial');
        setFiles(e.target.files);
        }
    };

    const handleUpload = async () => {
        if (files) {
            setStatus('uploading');
            const formData = new FormData()
            Array.from(files || []).forEach((file) => {
                formData.append('files', file);
            });

            try {
                const result = await fetch('http://localhost:5001/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await result.json();
                console.log(data);
                setStatus('success');
            } catch (err) {
                console.log(err);
                setStatus('fail');
            }
            
        }
    };

    return (
        <div className="form-card">
            <button className="close-button" onClick={onCancelForm}>
                &times;
            </button>
            <h1>Create a New RAG Model</h1>

            <div className="form-group">
                <label className="form-label">Model Name</label>
                <input 
                    type="text"
                    id="model-name"
                    className="form-input"
                />
            </div>

            <div className="form-button">
                <input id="file" type="file" multiple onChange={handleFileChange} />
                <button className="button-upload" onClick={handleUpload}>
                    Upload Your Documents
                </button>
            </div>
            

            <p className="document-count">
                Number of Documents: X
            </p>

            <button className="form-button button-create">
                Create the RAG Model
            </button>
        </div>
    )
}

export default CreateModelForm;