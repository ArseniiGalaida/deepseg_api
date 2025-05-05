import runpod
import base64
import os
import tempfile
from process_nifti import process_nifti_file

def handler(job):
    """
    Обработчик для RunPod
    
    Args:
        job (dict): Словарь с входными данными
            - input (dict): Входные данные
                - file_data (str): Base64-encoded файл
                - filename (str): Имя файла
    """
    try:
        # Получаем входные данные
        input_data = job["input"]
        file_data = input_data["file_data"]
        filename = input_data["filename"]
        
        # Создаем временную директорию
        with tempfile.TemporaryDirectory() as temp_dir:
            # Сохраняем входной файл
            input_path = os.path.join(temp_dir, filename)
            with open(input_path, "wb") as f:
                f.write(base64.b64decode(file_data))
            
            # Создаем путь для выходного файла
            output_filename = f"seg_{filename}"
            output_path = os.path.join(temp_dir, output_filename)
            
            # Обрабатываем файл
            process_nifti_file(input_path, output_path)
            
            # Читаем результат
            with open(output_path, "rb") as f:
                result_data = base64.b64encode(f.read()).decode('utf-8')
            
            return {
                "output": {
                    "file_data": result_data,
                    "filename": output_filename
                }
            }
            
    except Exception as e:
        return {
            "error": str(e)
        }

runpod.serverless.start({"handler": handler})