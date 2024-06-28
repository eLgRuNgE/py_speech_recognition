import speech_recognition as sr
import subprocess
import os
from openai import OpenAI, OpenAIError, APIError, RateLimitError
from pydub import AudioSegment
import time

client = OpenAI(api_key='aaaaaa')

MAX_TOKENS = 2000  # Adjust based on the token limit for the API

# Function to read the transcription file
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# Function to split text into chunks
def split_text(text, max_tokens=MAX_TOKENS):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Function to check remaining quota
def check_quota():
    try:
        response = client.usage.retrieve()
        if 'used' in response and 'limit' in response:
            used = response['used']
            limit = response['limit']
            return limit - used
    except OpenAIError as e:
        print(f"Error checking quota: {e}")
    return 0

# Function to get the summary for a chunk of text
def get_summary_for_chunk(chunk):
    prompt = f"This is a transcription of a recording:\n{chunk}\n\nPlease summarize it and provide the key points and important dates to note."

    # Implement retry mechanism
    for attempt in range(5):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ]
            )
            summary = response.choices[0].message.content.strip()
            return summary
        except (RateLimitError, APIError) as e:
            if 'insufficient_quota' in str(e) or isinstance(e, RateLimitError):
                print(f"Rate limit error: {e}. Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)
            else:
                raise e
    raise Exception("Exceeded maximum retries due to rate limit error.")

# Function to get the summary for the entire transcription
def get_summary(transcription):
    chunks = split_text(transcription)
    summaries = [get_summary_for_chunk(chunk) for chunk in chunks]
    return ' '.join(summaries)

# Function to save the summary to a file
def save_summary_to_file(summary, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(summary)

# Main function for audio transcription and summary
def process_audio_files():
    print(f"Iniciando el reconocimiento...\n")

    CHUNK_LENGTH_MS = 60000  # Length of each chunk in milliseconds (60 seconds)

    media_folder = "media"
    transcription_folder = "transcription"
    summary_folder = "summary"

    if not os.path.exists(transcription_folder):
        os.makedirs(transcription_folder)
    if not os.path.exists(summary_folder):
        os.makedirs(summary_folder)

    for audio_file_name in os.listdir(media_folder):
        if audio_file_name.endswith(".m4a"):
            print(f"Inicio del reconocimiento del archivo: {audio_file_name}\n")
            audio_file_path = os.path.join(media_folder, audio_file_name)
            wav_file_path = os.path.join(media_folder, os.path.splitext(audio_file_name)[0] + ".wav")
            transcription_file_path = os.path.join(transcription_folder, os.path.splitext(audio_file_name)[0] + ".txt")
            summary_file_path = os.path.join(summary_folder, os.path.splitext(audio_file_name)[0] + "__resume.txt")

            if os.path.exists(transcription_file_path):
                print(f"Transcripción ya existe para {audio_file_name}, saltando transcripción...\n")
            else:
                if not os.path.exists(audio_file_path):
                    print(f"Error: El archivo {audio_file_path} no existe.")
                    continue

                subprocess.run(["ffmpeg", "-i", audio_file_path, wav_file_path])

                if os.path.exists(wav_file_path):
                    recognizer = sr.Recognizer()
                    audio = AudioSegment.from_wav(wav_file_path)
                    chunks = [audio[i:i + CHUNK_LENGTH_MS] for i in range(0, len(audio), CHUNK_LENGTH_MS)]

                    full_text = ""
                    for i, chunk in enumerate(chunks):
                        chunk_file_path = os.path.join(media_folder, f"chunk_{i}.wav")
                        chunk.export(chunk_file_path, format="wav")

                        with sr.AudioFile(chunk_file_path) as source:
                            audio_data = recognizer.record(source)

                        try:
                            text = recognizer.recognize_google(audio_data, language="es-ES")
                            full_text += text + " "
                            print(f'Texto reconocido para el fragmento {i} de {audio_file_name}:\n{text}')
                        except sr.UnknownValueError:
                            print(f"Lo siento, no pude entender el audio del fragmento {i} de {audio_file_name}.")
                        except sr.RequestError as e:
                            print(f"Error al realizar la solicitud al servicio de reconocimiento de voz para el fragmento {i} de {audio_file_name}; {e}")

                        os.remove(chunk_file_path)

                    with open(transcription_file_path, "w", encoding='utf-8') as file:
                        file.write(full_text.strip())
                    print(f"Transcripción completa guardada en {transcription_file_path}")

            transcription = read_txt_file(transcription_file_path)
            try:
                # Check quota before proceeding
                remaining_quota = check_quota()
                if remaining_quota > 0:
                    summary = get_summary(transcription)
                    save_summary_to_file(summary, summary_file_path)
                    print(f"Resumen guardado en {summary_file_path}")
                else:
                    print("No hay suficiente cuota disponible para obtener el resumen.")
            except Exception as e:
                print(f"Error al obtener el resumen: {e}")
                # Manejar la situación aquí, por ejemplo, enviar una notificación o registrar el error

if __name__ == "__main__":
    process_audio_files()
