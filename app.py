from flask import Flask, request, jsonify 
from dotenv import load_dotenv
import os
import google.generativeai as genai
from rag_pipeline import Rag_pipeline
from authlib.integrations.flask_oauth2 import ResourceProtector, current_token
from auth_utils import Auth0JWTBearerTokenValidator
import psycopg2
from flask_cors import CORS

rag_pipeline = Rag_pipeline()

load_dotenv() 

os.makedirs('user_data', exist_ok=True)

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(os.getenv('AUTH0_DOMAIN'), os.getenv('AUTH0_API_AUDIENCE'))
require_auth.register_token_validator(validator)

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    dbname=os.getenv('DB_NAME')
)

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)
print(bool(API_KEY))


@app.route('/upload', methods=['POST'])
def upload_file():
    #auth0_user_id = current_token.get('sub')
    auth0_user_id = "test_id"
    uploaded_files = request.files.getlist("files")
    user_info_path = os.path.join('user_data', auth0_user_id)
    os.makedirs(user_info_path, exist_ok=True)
    all_chunks = []
    all_metadata = []
    cursor = conn.cursor()
    query = "INSERT INTO files (user_id, filename) VALUES (%s, %s);"
    try:
        for file in uploaded_files:
            filename = file.filename
            cursor.execute(query, (auth0_user_id, filename))
            if filename.endswith('.pdf'):
                chunks, metadata = rag_pipeline.process_pdf(file)
                all_chunks.extend(chunks)
                all_metadata.extend(metadata)

            elif filename.endswith('.csv'):
                chunks, metadata = rag_pipeline.process_csv(file)
                all_chunks.extend(chunks)
                all_metadata.extend(metadata)
            
        conn.commit() 

        if all_chunks:
            rag_pipeline.save_data(user_info_path, all_chunks, all_metadata)
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"An error occurred: {e}"}), 500
    finally:
        cursor.close()

    return jsonify({"message": "Files uploaded and metadata saved successfully"})
        


@app.route('/query', methods=['POST'])
@require_auth()
def handle_query():
    auth0_user_info = current_token.get('sub')
    user_info_path = os.path.join('user_data', auth0_user_info)
    user_question = request.json['question']

    index, metadata, chunks = rag_pipeline.retrieve_data(user_info_path)
    
    response = rag_pipeline.search_and_generate_response(user_question, index, chunks, metadata)
    return jsonify({"answer": response})

if __name__ == '__main__':
    app.run(debug=True, port=5001)