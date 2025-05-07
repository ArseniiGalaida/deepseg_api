import runpod
import base64
import os
import tempfile
from process_nifti import process_nifti_file

def handler(job):
    try:
        input_data = job["input"]
        file_data = input_data["file_data"]
        filename = "input_file.nii.gz"

        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, filename)
            with open(input_path, "wb") as f:
                f.write(base64.b64decode(file_data))

            output_filename = f"seg_{filename}"
            output_path = os.path.join(temp_dir, output_filename)

            process_nifti_file(input_path, output_path)

            with open(output_path, "rb") as f:
                result_data = base64.b64encode(f.read()).decode('utf-8')
            
            return {
                "file_data": result_data
            }
            
    except Exception as e:
        return {
            "error": str(e)
        }

runpod.serverless.start({"handler": handler})