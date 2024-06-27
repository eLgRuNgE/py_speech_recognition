# Audio Transcription Script

Este repositorio contiene un script para convertir archivos de audio en formato M4A a texto utilizando `ffmpeg` y `speech_recognition`. El script convierte el archivo de audio a formato WAV y luego transcribe el audio a texto, guardando la transcripción en un archivo de texto en una carpeta llamada `transcription`.

## Requisitos

- Python 3.6 o superior
- `ffmpeg`
- `speech_recognition`
- `pyaudio`

## Instalación

### macOS

1. Instalar Homebrew (si no está instalado):

    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. Instalar `ffmpeg` y `portaudio`:

    ```sh
    brew install ffmpeg portaudio
    ```

3. Crear un entorno virtual (opcional pero recomendado):

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4. Instalar las dependencias de Python:

    ```sh
    pip install SpeechRecognition pyaudio
    ```

### Windows

1. Descargar e instalar `ffmpeg` desde el sitio oficial: [FFmpeg Download](https://ffmpeg.org/download.html). Asegúrate de agregar `ffmpeg` al PATH del sistema.

2. Instalar `portaudio` y `pyaudio`:

    2.1 Descargar e instalar `portaudio` desde el sitio oficial: [PortAudio Download](http://www.portaudio.com/download.html).

    2.2 Descargar el instalador de PyAudio desde [aquí](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) y luego instalarlo:

    ```sh
    pip install path/to/your/downloaded/pyaudio-*.whl
    ```

3. Crear un entorno virtual (opcional pero recomendado):

    ```sh
    python -m venv .venv
    .venv\Scripts\activate
    ```

4. Instalar las dependencias de Python:

    ```sh
    pip install SpeechRecognition
    ```

### Ubuntu Linux

1. Actualizar los repositorios e instalar `ffmpeg` y las dependencias necesarias:

    ```sh
    sudo apt update
    sudo apt install ffmpeg libportaudio2
    ```

2. Instalar `portaudio` y `pyaudio`:

    ```sh
    sudo apt install portaudio19-dev python3-pyaudio
    ```

3. Crear un entorno virtual (opcional pero recomendado):

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4. Instalar las dependencias de Python:

    ```sh
    pip install SpeechRecognition pyaudio
    ```

## Uso

1. Clonar el repositorio:

    ```sh
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Asegúrate de que los archivos de audio M4A estén en la carpeta `media`.

3. Ejecutar el script:

    ```sh
    python transcribe_audio.py
    ```

4. La transcripción se guardará en un archivo de texto en la carpeta `transcription` con el mismo nombre que el archivo de audio original.

## Notas

- Asegúrate de que los archivos de audio estén correctamente ubicados y que las rutas en el script sean precisas.
- Si encuentras problemas durante la instalación de las dependencias, consulta la documentación oficial de cada herramienta para obtener más ayuda.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
