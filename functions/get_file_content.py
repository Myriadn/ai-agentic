import os

from google.genai import types

import config


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(os.path.join(abs_working_dir, file_path))

    try:
        if os.path.commonpath([abs_working_dir]) != os.path.commonpath(
            [abs_working_dir, abs_target_file]
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_target_file, "r") as f:
            content = f.read(config.token)
            extra = f.read(1)
            if extra:
                content += (
                    f'[...File "{file_path}" truncated at {config.token} characters]'
                )
            return content

    except Exception as e:
        return f"Error: {str(e)}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get inside the file content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="it's a path to get content from that file",
            ),
        },
        required=["file_path"],
    ),
)
