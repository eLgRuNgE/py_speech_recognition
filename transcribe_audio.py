import speech_recognition as sr
import subprocess
import os

# Paths to the audio files
audio_file_path = "media/AUDIO-2022-11-28-11-58-17.m4a"
wav_file_path = "media/AUDIO-2022-11-28-11-58-17.wav"
transcription_folder = "transcription"

# Ensure the transcription folder exists
if not os.path.exists(transcription_folder):
    os.makedirs(transcription_folder)

# Derive the transcription file path
transcription_file_path = os.path.join(transcription_folder, os.path.splitext(os.path.basename(audio_file_path))[0] + ".txt")

# Check if the audio file exists
if not os.path.exists(audio_file_path):
    print(f"Error: El archivo {audio_file_path} no existe.")
else:
    # Use ffmpeg to convert the audio file to WAV format
    subprocess.run(["ffmpeg", "-i", audio_file_path, wav_file_path])

    # Check if the WAV file was created
    if os.path.exists(wav_file_path):
        # Initialize recognizer
        recognizer = sr.Recognizer()

        # Recognize speech using the converted WAV file
        with sr.AudioFile(wav_file_path) as source:
            audio = recognizer.record(source)

        # Transcribe audio to text
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            print(f'Texto reconocido:\n{text}')

            # Save the transcription to a text file
            with open(transcription_file_path, "w") as file:
                file.write(text)
            print(f"Transcripción guardada en {transcription_file_path}")
        except sr.UnknownValueError:
            print("Lo siento, no pude entender el audio.")
        except sr.RequestError as e:
            print(f"Error al realizar la solicitud al servicio de reconocimiento de voz; {e}")
    else:
        print(f"Error: No se pudo crear el archivo WAV {wav_file_path}.")
