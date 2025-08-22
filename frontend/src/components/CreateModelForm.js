import React from 'react';
import './CreateModelForm.css'; // Don't forget to import the CSS!

function CreateModelForm() {
    return (
        <div className="form-card">
            <div className="close-button">
                &times;
            </div>
            <h1>Create a New RAG Model</h1>

            <div className="form-group">
                <label className="form-label">Model Name</label>
                <input 
                    type="text"
                    id="model-name"
                    class="form-input"
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