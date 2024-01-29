# Main script setup
import argparse
import os
import re
import time
from dotenv import load_dotenv
import json
from openai import OpenAI

from classes.assistant import Assistant
from classes.thread import Thread
from classes.run import Run
from classes.file_manager import FileManager
from classes.role import Role

from func.tool_config import TOOLS
from func.tool_config import FUNCTIONS_TO_HANDLE

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["MODEL_TO_USE"] = os.getenv("MODEL_TO_USE")

parser = argparse.ArgumentParser(description='Create assistants on OpenAI.')
parser.add_argument('--data_path', default='../data/json', help='Path to the JSON file or directory containing JSON files')
parser.add_argument('--model', default=os.getenv("MODEL_TO_USE"), help='Model to use')
parser.add_argument('--name', default='unil_assistant', help='Name of the assistant')
parser.add_argument('--init_message', default='Bonjour', help='Initial message to send to the assistant')
parser.add_argument('--output', default='output_images', help='Output directory')
args = parser.parse_args()

def get_answer_json(text):
   print(text['answer'])


client = OpenAI()

file_manager = FileManager(client)

# File operations
data_path = args.data_path
data_path = os.path.join(data_path)
proxy_file_path = os.path.join(data_path, 'proxy.json')
files = []

if os.path.isfile(data_path) and data_path.endswith(".json"):
    file = file_manager.send_file_to_openai(data_path)
    files.append(file)
elif os.path.isdir(data_path):
    files = file_manager.send_all_files(data_path)

file_manager.add_ids_to_proxy_file(proxy_file_path, files)
print("Files sent to OpenAI: " + str([f"ID: {file.id}, Name: {file.filename}" for file in files]))

# Upload the proxy file
proxy_file = file_manager.send_file_to_openai(proxy_file_path)

# Instructions and tools for the assistant
INSTRUCTIONS = """
Étant donné la liste JSON suivante, qui contient des informations sur différents fichiers de statistiques étudiantes, votre tâche est de simplement identifier les fichiers pertinents et d'extraire leurs IDs. 
Il n'est pas nécessaire de chercher ou de fournir une réponse à une question spécifique dans un premier temps.

Utilisez la fonction suivante pour ajouter un fichier à l'assistant:

add_file_to_the_assistant(file_ids=["file_id_1", "file_id_2", "file_id_3"])

Dans un second temps, vous pourrez répondre à la question quand vous aurez identifié les fichiers pertinents.

La réponse doit être structurée comme suit uniquement  aucune autre réponse ne sera acceptée:

{
    "answer": 'la réponse complète à la question en string',
    "valeurs": ['valeur1', 'valeur2', 'valeur3']
}

Dans le cas où vous ne trouvez pas de réponse, veuillez utiliser le format suivant pour indiquer qu'aucune réponse n'a été trouvée :

{
    "answer": None,
    "valeurs": []
}

A tout moment, Si le sujet de la question change, et que les fichiers pertinents sont différents, vous pouvez utiliser la fonction suivante pour recharger l'assistant avec uniquement le fichier proxy:

reload_assistant_with_only_proxy_file(proxy_file_id="file_id")

A noté que passé un certain nombre de fichiers (20) l'assistant ne pourra plus être rechargé avec de nouveaux fichiers. Dans ce cas, il faudra impérativement recharger l'assistant avec uniquement le fichier proxy.

Merci d'avance pour votre aide !
"""

# Create an assistant
assistant = Assistant(client, name=args.name, instructions=INSTRUCTIONS, tools=TOOLS, model=args.model, file_ids=[proxy_file.id])
assistant.create()

# Create a thread
thread = Thread(client)
thread.create()

run = Run(client, thread_id=thread.thread_id, assistant_id=assistant.assistant_id)

# Debugging URLs
print(f"Debugging: Useful for checking the generated agent in the playground. https://platform.openai.com/playground?mode=assistant&assistant={assistant.assistant_id}")
print(f"Debugging: Useful for checking logs. https://platform.openai.com/playground?thread={thread.thread_id}")

# Interaction loop
user_input = input("Quel est votre question ? ")
while user_input.lower() != "exit" and user_input != "":
    # Send a message to the thread
    time_start = time.time()
    thread.send_message(user_input, Role.USER)

    run.start()
    run.execute_and_monitor(FUNCTIONS_TO_HANDLE)

    messages_all = thread.get_messages()
    messages = json.loads(json.loads(messages_all.model_dump_json())['data'][0]['content'][0]["text"]['value'])
    print(messages['valeurs'])
    print(f"Temps de réponse: {time.time() - time_start} secondes")

    user_input = input("Quel est votre question ? ")

# Clean up
assistant.delete()
print("Assistant deleted with ID: " + assistant.assistant_id)

# Delete files
for file in files:
    file_manager.delete_file(file.id)
print("Files deleted with ID: " + str([file.id for file in files]))

file_manager.delete_file(proxy_file.id)
print("Proxy file deleted with ID: " + proxy_file.id)
