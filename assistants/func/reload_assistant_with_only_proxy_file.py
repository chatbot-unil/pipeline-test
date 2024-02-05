# func_dir/reload_assistant_with_only_proxy_file.py

import json
from assistants.classes.database import Data

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

FUNCTION = {
    "type": "function",
    "function": {
        "name": "reload_assistant_with_only_proxy_file",
        "description": "Use this function to reload the assistant with only the proxy file any time if the current assistant has too many files (20) or if the files are not relevant to the question",
        "parameters": {
            "type": "object",
            "properties": {
                "proxy_file_id": {
                    "type": "string",
                    "description": "ID of the proxy file",
                },
            },
            "required": ["proxy_file_id"],
        },
    },
}

def reload_assistant_with_only_proxy_file(assistant_id, proxy_file_id):
    if Data("assistants/database/database.db", path_init="assistants/database/init.sql").is_in_files(proxy_file_id):
        Data("assistants/database/database.db", path_init="assistants/database/init.sql").truncate_current_files()
        Data("assistants/database/database.db", path_init="assistants/database/init.sql").add_file_to_current(proxy_file_id)
        client.beta.assistants.update(
            assistant_id=assistant_id,
            file_ids=[proxy_file_id],
        )
        return json.dumps({"file_ids": [proxy_file_id]})
    else:
        return json.dumps({"error": "File not found"})