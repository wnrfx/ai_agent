import os


MAX_CHARS = 10000 

schema_get_file_content = {
    "type": "function", 
    "function": {
        "name": "get_file_content", 
        "description": "Returns the content of the file specified in the relative file path to the working directory",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string", 
                    "description": "The path to the file that we want to get the contents of, relative to the working directory",  
                },  
            },
        },
    }, 
}


def get_file_content(working_directory: str, file_path: str) -> str: 

    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory, file_path))

    valid_target = os.path.commonpath([working_directory_abs, os.path.abspath(target_file)]) == working_directory_abs

    if valid_target: 
       
        if os.path.isfile(target_file): 
            
            with open(target_file, "r") as f: 
                file_contents = f.read(MAX_CHARS)

                if f.read(1): 
                    file_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'


            return file_contents

        else: 
            return f'Error: File not found or is not a regular file: "{file_path}"'

    else: 
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
