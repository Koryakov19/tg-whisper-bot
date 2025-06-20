import subprocess
import os
import time

def transcribe(file_path: str) -> str:
    model_path = "models/ggml-small.bin"
    # whisper-cli создает файл с именем input_file.txt
    output_path = f"{file_path}.txt"

    command = [
        "../whisper.cpp/build/bin/whisper-cli",
        "-m", model_path,
        "-f", file_path,
        "-otxt",
        "-l", "auto"
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        return f"[Ошибка whisper-cli]: {result.stderr.decode()}"

    # Надёжное ожидание файла
    start_time = time.time()
    timeout = 10  # секунд

    while time.time() - start_time < timeout:
        if os.path.exists(output_path):
            with open(output_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        time.sleep(0.3)

    return "[Ошибка]: файл результата не найден за разумное время."
