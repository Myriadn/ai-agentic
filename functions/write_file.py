import os

from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(os.path.join(abs_working_dir, file_path))

    try:
        if os.path.commonpath([abs_working_dir]) != os.path.commonpath(
            [abs_working_dir, abs_target_file]
        ):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(abs_target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(abs_target_file), exist_ok=True)

        with open(abs_target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Editing files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="it's a path to edit that file",
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="Content to write ts file"
            ),
        },
        required=["file_path", "content"],
    ),
)
