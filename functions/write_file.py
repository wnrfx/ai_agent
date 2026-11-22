import os 


schema_write_file = {
    "type": "function", 
    "function": {
        "name": "write_file",
        "description": "Writes contents into a specified file, with specified relative path from the working directory, if file doesn't exist the new file will be created", 
        "parameters": {
            "type": "object", 
            "required": ["file_path", "content"],
            "properties": {
                "file_path": {
                    "type": "string", 
                    "description": "The path to the file we want to write to, relative to the working directory",
                },
                "content": {
                    "type": "string", 
                    "description": "The content that need to be written to the file within the specified path", 
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
        working_directory_abs = os.path.abspath(working_directory) 
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

        valid_target_file = os.path.commonpath([working_directory_abs, os.path.abspath(target_file)]) == working_directory_abs 

        if valid_target_file: 
            
            if os.path.isdir(target_file):

                return f'Error: Cannot write to "{file_path}" as it is a directory'

            try: 
                parent_directory = os.path.dirname(target_file) 

                if parent_directory: 
                    os.makedirs(parent_directory, exist_ok=True) 

                with open(target_file, "w", encoding="utf-8") as f: 
                    f.write(content)

                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

            except OSError as e: 
                return f'Error: Failed to write "{file_path}": {e}'

        else: 
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
