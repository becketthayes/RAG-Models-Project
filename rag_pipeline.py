from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import numpy as np 
import pdfplumber
import csv
import faiss
import os
import json

class Rag_pipeline():
    def __init__(self, embedding_name='all-MiniLM-L6-v2', model_name='gemini-1.5-flash-latest'):
        self.model_embeddings = SentenceTransformer(embedding_name)
        self.model_gemini = genai.GenerativeModel(model_name)
    
    def chunk_text(self, text, chunk_size):
        words = text.split()
        chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        return chunks
    
    def generate_embeddings(self, chunks):
        embeddings = self.model_embeddings.encode(chunks)
        embeddings = np.array(embeddings, dtype='float32')
        return embeddings
    
    def process_pdf(self, file):
        filename = file.filename
        with pdfplumber.open(file) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        chunks = self.chunk_text(full_text)
        metadata = [{'source': filename} for _ in range(len(chunks))]
        return chunks, metadata
    
    def process_csv(self, file):
        chunks = []
        metadata = []
        csv_content = file.stream.read().decode('utf-8').splitlines()
        csv_reader = csv.reader(csv_content)
        header = next(csv_reader)

        for row in csv_reader:
            row_description = ", ".join([f'{header[i]} is {row[i]}' for i in range(len(header))])
            full_chunk = f"Record: {row_description}"
            chunks.append(full_chunk)
            metadata.append({'source': file.filename})

        return chunks, metadata
    
    def save_data(self, data_path, all_chunks, all_metadata):
        embeddings = self.generate_embeddings(all_chunks)
        embedding_dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(embedding_dim)
        index.add(embeddings)

        faiss.write_index(index, os.path.join(data_path, 'indexes.bin'))

        with open(os.path.join(data_path, 'metadata.json'), 'w') as f:
            json.dump(all_metadata, f)

        with open(os.path.join(data_path, 'chunks.json'), 'w') as f:
            json.dump(all_chunks, f)

    def retrieve_data(self, data_path):

        index = faiss.read_index(os.path.join(data_path, "indexes.bin"))
        with open(os.path.join(data_path, "metadata.json"), 'r') as f:
            metadata = json.load(f)
        with open(os.path.join(data_path, "chunks.json"), 'r') as f:
            chunks = json.load(f)

        return index, metadata, chunks
    
    def search_and_generate_response(self, user_question, index, chunks, metadata):
        query_embedding = self.model_embeddings.encode([user_question])

        distances, indices = index.search(np.array(query_embedding, dtype='float32'), 3)

        best_chunks = [chunks[i] for i in indices[0]]
        files = [metadata[i]['source'] for i in indices[0]]

        context_info = "\n\n".join(best_chunks)

        prompt = f"""
            You are an expert AI research assistant. Answer the user's question based only on the following context.
            Do not make up information. If you can't answer, then state that you can't answer.
            
            Context Info: {context_info}\n\nUser Question: {user_question}
            """

        response = self.model_gemini.generate_content(prompt)
        return response.text
