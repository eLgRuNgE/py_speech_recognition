import speech_recognition as sr
import subprocess
import os

# Constants
CHUNK_LENGTH_MS = 60000  # Length of each chunk in milliseconds (60 seconds)

# Folder paths
media_folder = "media"
transcription_folder = "transcription"

# Ensure the transcription folder exists
if not os.path.exists(transcription_folder):
    os.makedirs(transcription_folder)

# Process each M4A file in the media folder
for audio_file_name in os.listdir(media_folder):
    if audio_file_name.endswith(".m4a"):
        audio_file_path = os.path.join(media_folder, audio_file_name)
        wav_file_path = os.path.join(media_folder, os.path.splitext(audio_file_name)[0] + ".wav")
        transcription_file_path = os.path.join(transcription_folder, os.path.splitext(audio_file_name)[0] + ".txt")

        # Check if the audio file exists
        if not os.path.exists(audio_file_path):
            print(f"Error: El archivo {audio_file_path} no existe.")
            continue

        # Use ffmpeg to convert the audio file to WAV format
        subprocess.run(["ffmpeg", "-i", audio_file_path, wav_file_path])

        # Check if the WAV file was created
        if os.path.exists(wav_file_path):
            # Initialize recognizer
            recognizer = sr.Recognizer()

            # Split the audio file into chunks
            from pydub import AudioSegment
            audio = AudioSegment.from_wav(wav_file_path)
            chunks = [audio[i:i + CHUNK_LENGTH_MS] for i in range(0, len(audio), CHUNK_LENGTH_MS)]

            # Process each chunk
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

                # Remove the chunk file after processing
                os.remove(chunk_file_path)

            # Save the full transcription to a text file
            with open(transcription_file_path, "w") as file:
                file.write(full_text.strip())
            print(f"Transcripción completa guardada en {transcription_file_path}")
        else:
            print(f"Error: No se pudo crear el archivo WAV {wav_file_path}.")
