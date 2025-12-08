import os
import time
import random
import playsound
import sounddevice as sd
import numpy as np
import wavio
import whisper
from gtts import gTTS
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

# API key for LangChain and OpenAI embeddings
API_KEY = "yourAPIKey"

db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:"password"@localhost:db_name")
llm = OpenAI(model_name="gpt-3.5-turbo-instruct", openai_api_key=API_KEY)
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

def speak(text):
    tts = gTTS(text=text, lang="en", slow=False)
    filename = f"{random.randint(1, 10000)}.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def record_audio(filename, duration=8, sample_rate=44100, silence_threshold=100, silence_duration=3):
    print("Recording audio...")
    speak("Please speak your command.")
    audio_data = []
    silent_counter = 0
    recording = True
    block_size = int(sample_rate * 0.1)

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype=np.int16) as stream:
        start_time = time.time()
        while recording:
            block, _ = stream.read(block_size)
            audio_data.append(block)
            volume = np.abs(block).mean()
            if volume < silence_threshold:
                silent_counter += 0.1
            else:
                silent_counter = 0
            if silent_counter >= silence_duration or (time.time() - start_time) >= duration:
                recording = False
    audio_data = np.concatenate(audio_data, axis=0)
    wavio.write(filename, audio_data, sample_rate)
    print("Recording finished.")

def recognize_speech_whisper():
    model = whisper.load_model("base")  
    audio_file = "input.wav"
    record_audio(audio_file, duration=8)
    print("Transcribing audio...")
    result = model.transcribe(audio_file)
    os.remove(audio_file) 
    text = result.get("text", "").strip().lower()
    print(f"Recognized: {text}")
    return text


def ask_database(prompt):

    query = f"""
    Given an input question, first create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer.
    Use the following format:

    Question: Question here
    SQLQuery: SQL Query to run
    SQLResult: Result of the SQLQuery
    Answer: Final answer here

    {prompt}
    """
    try:
        response = db_chain.run(query)
        print("SQL Answer:", response)
        speak(response)  
    except Exception as e:
        print("Error:", e)
        speak("An error occurred while processing your query.")

def build_faiss_index():
    """
    Connect to the illnesses database, fetch the relevant fields from the illnesses table,
    and build a FAISS index over the illnesses data.
    """
    import psycopg2
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password='pixel3105',
        database='illness_db'
    )
    cur = conn.cursor()
    cur.execute("SELECT illness_name, possible_symptoms, treatment_plan, common_causes, recommended_tests FROM illnesses;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    documents = []
    for row in rows:
        illness_name, symptoms, treatment_plan, common_causes, tests = row
        content = (
            f"Illness: {illness_name}\n"
            f"Symptoms: {symptoms}\n"
            f"Treatment: {treatment_plan}\n"
            f"Causes: {common_causes}\n"
            f"Tests: {tests}"
        )
        documents.append(Document(page_content=content))
    
    embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore


faiss_index = build_faiss_index()

def semantic_search(query, k=3):
    """
    Perform a semantic search on the FAISS index and return the top k relevant documents.
    """
    results = faiss_index.similarity_search(query, k=k)
    return results

def ask_semantic_database(prompt):
    results = semantic_search(prompt)
    if results:
        combined_text = "\n\n".join([doc.page_content for doc in results])
        response_text = f"I found the following relevant information:\n{combined_text}"
        print("Semantic Search Answer:\n", response_text)
        speak(response_text)
    else:
        speak("No relevant entries found.")


if __name__ == "__main__":
    print("Starting the application...")
    speak("Starting the application.")
    
    while True:
        user_command = recognize_speech_whisper()
        if user_command:
           
            if user_command in ['abort', 'end', 'terminate', 'exit']:
                print("Ending the session.")
                speak("Thanks for using the assistant. Goodbye!")
                break
            
            print(f"Processing: {user_command}")
          
            if "semantic" in user_command or "search" in user_command:
                ask_semantic_database(user_command)
            else:
               
                ask_database(user_command)
        else:
            print("No command recognized.")
            speak("I didn't catch that. Please try again.")
