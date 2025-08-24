from flask import Flask, request, jsonify 
from dotenv import load_dotenv
import os
import google.generativeai as genai
from rag_pipeline import Rag_pipeline

rag_pipeline = Rag_pipeline()

load_dotenv() 

os.makedirs('user_data', exist_ok=True)

app = Flask(__name__)

API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)
print(bool(API_KEY))


@app.route('/upload/<user_id>', methods=['POST'])
def upload_file(user_id):
    uploaded_files = request.files.getlist("files")
    user_info_path = os.path.join('user_data', user_id)
    os.makedirs(user_info_path, exist_ok=True)
    all_chunks = []
    all_metadata = []
    for file in uploaded_files:
        filename = file.filename
        if filename.endswith('.pdf'):
            chunks, metadata = rag_pipeline.process_pdf(file)
            all_chunks.extend(chunks)
            all_metadata.extend(metadata)

        elif filename.endswith('.csv'):
            chunks, metadata = rag_pipeline.process_csv(file)
            all_chunks.extend(chunks)
            all_metadata.extend(metadata)

    if all_chunks:
        rag_pipeline.save_data(user_info_path, all_chunks, all_metadata)

@app.route('/query/<user_id>', methods=['POST'])
def handle_query(user_id):
    user_info_path = os.path.join('user_data', user_id)
    user_question = request.json['question']

    index, metadata, chunks = rag_pipeline.retrieve_data(user_info_path)
    
    response = rag_pipeline.search_and_generate_response(user_question, index, chunks, metadata)
    return jsonify({"answer": response})

if __name__ == '__main__':
    app.run(debug=True)