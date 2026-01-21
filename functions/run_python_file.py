import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(os.path.join(abs_working_dir, file_path))

    try:
        if os.path.commonpath([abs_working_dir, abs_target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not abs_target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_target_file]
        if args:
            command.extend(args)

        result = subprocess.run(
            command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30
        )

        outputan = []

        if result.returncode != 0:
            outputan.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            outputan.append("No output produced")

        if result.stdout:
            outputan.append(f"STDOUT: {result.stdout}")

        if result.stderr:
            outputan.append(f"STDERR: {result.stderr}")

        return "\n".join(outputan)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Running the python execution file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="it's a path to run that file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="this is opsional",
            ),
        },
        required=["file_path"],
    ),
)
