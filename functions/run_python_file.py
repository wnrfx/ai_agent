import os
import subprocess


schema_run_python_file = {
    "type": "function", 
    "function": {
        "name": "run_python_file", 
        "description": "Runs a python file within the specified file_path relative to the working directory", 
        "parameters": {
            "type": "object", 
            "required": ["file_path"], 
            "properties": {
                "file_path": {
                    "type": "string", 
                    "description": "The path to the python file that should be executed", 
                },
                "args": {
                    "type": "array", 
                    "items": {
                        "type": "string", 
                    },
                    "description": "Optional list of arguments to pass into a python script", 
                },
            },
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

    command = ["python3", target_file]

    ret_list = []

    if args:
        command.extend(args)
    valid_target = os.path.commonpath([working_directory_abs, os.path.abspath(target_file)]) == working_directory_abs

    if valid_target:
        if os.path.isfile(target_file):

            if target_file[-3:] != ".py":
                return f'Error: "{file_path}" is not a Python file'

            result = subprocess.run(command, cwd=working_directory_abs, timeout=30, capture_output=True, text=True)

            if result.returncode != 0:
                ret_list.append(f"Process exited with code {result.returncode}")

            if result.stdout:
                ret_list.append(f"STDOUT: \n{result.stdout}")

            if result.stderr:
                ret_list.append(f"STDERR: \n{result.stderr}")

            if not result.stderr and not result.stdout:
                ret_list.append("No output produced")

            return "\n".join(ret_list)

        else:
             return f'Error: "{file_path}" does not exist or is not a regular file'
    else:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
