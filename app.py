from flask import Flask, request, jsonify 
from dotenv import load_dotenv
import os
import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import csv
import json
import google.generativeai as genai

load_dotenv() 

os.makedirs('user_data', exist_ok=True)

app = Flask(__name__)

API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)
print(bool(API_KEY))

model_embeddings = SentenceTransformer('all-MiniLM-L6-v2')
model_gemini = genai.GenerativeModel('gemini-1.5-flash-latest')

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def generate_embeddings(chunks):
    embeddings = model_embeddings.encode(chunks)
    embeddings = np.array(embeddings, dtype='float32')
    return embeddings

@app.route('/upload', methods=['POST'])
def upload_file(user_id):
    uploaded_files = request.files.getlist("files")
    user_info_path = os.path.join('user_data', user_id)
    os.makedirs(user_info_path, exist_ok=True)
    all_chunks = []
    all_metadata = []
    for file in uploaded_files:
        filename = file.filename
        if filename.endswith('.pdf'):
            with pdfplumber.open(file) as pdf:
                full_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
            chunks = chunk_text(full_text)
            all_chunks.extend(chunks)
            for i in range(len(chunks)):
                all_metadata.append({'source': filename})

        elif filename.endswith('.csv'):
            csv_content = file.stream.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(csv_content)
            header = next(csv_reader)

            for row in csv_reader:
                row_description = ", ".join([f'{header[i]} is {row[i]}' for i in range(len(header))])
                full_chunk = f"Record: {row_description}"
                all_chunks.append(full_chunk)
                all_metadata.append({'source': filename})
    if all_chunks:
        embeddings = generate_embeddings(all_chunks)
        embedding_dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(embedding_dim)
        index.add(embeddings)
        faiss.write_index(index, os.path.join(user_info_path, 'indexes.bin'))

        with open(os.path.join(user_info_path, 'metadata.json'), 'w') as f:
            json.dump(all_metadata, f)

        with open(os.path.join(user_info_path, 'chunks.json'), 'w') as f:
            json.dump(all_chunks, f)

@app.route('/query', methods=['POST'])
def handle_query():
    user_question = request.json['question']

    index = faiss.read_index('indexes/unified_index.bin')
    with open('indexes/metadata.json', 'r') as f:
        metadata = json.load(f)
    with open('indexes/chunks.json', 'r') as f:
        chunks = json.load(f)
    
    query_embedding = model_embeddings.encode([user_question])

    distances, indices = index.search(np.array(query_embedding, dtype='float32'), 3)

    best_chunks = [chunks[i] for i in indices[0]]
    files = [metadata[i]['source'] for i in indices[0]]

    context_info = "\n\n".join(best_chunks)
    
    prompt = f"""You are an expert AI research assistant. Answer the user's question based only on the following context.
            Do not make up information. If you can't answer, then state that you can't answer.
            
            Context Info: {context_info}\n\nUser Question: {user_question}
            """
    
    response = model_gemini.generate_content(prompt)
    print(response.text)


if __name__ == '__main__':
    app.run(debug=True)