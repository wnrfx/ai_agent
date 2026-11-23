import os 


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_directory_abs = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_directory_abs, directory)) 

    # if directory == ".":
    #     print("Results for current directory")
    # else: 
    #     print(f"Results for '{directory}' directory")


    valid_target_directory = os.path.commonpath([working_directory_abs, target_directory]) == working_directory_abs 
    if not valid_target_directory: 
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        if os.path.isdir(target_directory): 
            ls = os.listdir(target_directory)
            files_info = []
            for file in ls:
                file_path = os.path.join(target_directory, file) 
                files_info.append(f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
                
            return "\n".join(files_info)

        else:   
            return f'Error: "{directory}" is not a directory'
