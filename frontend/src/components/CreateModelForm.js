import React from 'react';
import './CreateModelForm.css'; // Don't forget to import the CSS!

function CreateModelForm({ onCancelForm }) {
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

            <button className="form-button button-upload">
                Upload Your Documents
            </button>

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