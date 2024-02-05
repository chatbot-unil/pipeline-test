# func_dir/add_file_to_the_assistant.py
from assistants.classes.file_manager import FileManager
from assistants.classes.database import Data
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

FUNCTION = {
    "type": "function",
    "function": {
        "name": "add_file_to_the_assistant",
        "description": "Use this function to add a file to the assistant",
        "parameters": {
            "type": "object",
            "properties": {
                "file_ids": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "List of file IDs to add to the assistant",
                },
            },
            "required": ["file_ids"],
        },
    },
}

def add_file_to_the_assistant(file_ids, assistant_id):
    if Data("assistants/database/database.db", path_init="assistants/database/init.sql").is_in_files(file_ids):
        old_file_ids = FileManager(client).get_file_ids_from_assistant(assistant_id)
        for file_id in file_ids:
            Data("assistants/database/database.db", path_init="assistants/database/init.sql").add_file_to_current(file_id)
        file_ids.extend(old_file_ids)
        client.beta.assistants.update(
            assistant_id=assistant_id,
            file_ids=file_ids,
        )
        return json.dumps({"file_ids": file_ids})
    else:
        return json.dumps({"error": "File not found"})
