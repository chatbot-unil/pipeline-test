import os
import json

class FileManager:
    def __init__(self, client):
        self.client = client
        
    def send_file_to_openai(self, data):
        with open(data, 'rb') as file_data:
            file = self.client.files.create(purpose='assistants', file=file_data)
            return file

    def send_all_files(self, dir):
        files = []
        for file_name in os.listdir(dir):
            if file_name.endswith(".json") and "proxy" not in file_name:
                file_path = os.path.join(dir, file_name)
                files.append(self.send_file_to_openai(file_path))
        return files

    def add_ids_to_proxy_file(self, proxy_file, files):
        with open(proxy_file, 'r', encoding='utf-8') as file:
            proxy_data = json.load(file)

        for item in proxy_data:
            file_name = item['name']
            for uploaded_file in files:
                if uploaded_file.filename == file_name:
                    item['id'] = uploaded_file.id
                    break

        with open(proxy_file, 'w', encoding='utf-8') as file:
            json.dump(proxy_data, file, indent=4, ensure_ascii=False)
            
    def get_file_ids_from_assistant(self, assistant_id):
        assistant = self.client.beta.assistants.retrieve(assistant_id=assistant_id)
        return assistant.file_ids

    def delete_file(self, file_id):
        if file_id:
            self.client.files.delete(file_id=file_id)
