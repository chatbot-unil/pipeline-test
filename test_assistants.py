# Main script setup
import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import time
from question import Question
from datetime import datetime

from assistants.classes.assistant import Assistant
from assistants.classes.thread import Thread
from assistants.classes.run import Run
from assistants.classes.file_manager import FileManager
from assistants.classes.role import Role

from assistants.classes.database import Data

from assistants.func.tool_config import TOOLS
from assistants.func.tool_config import FUNCTIONS_TO_HANDLE

def open_test_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def prepare_data(data):
    questions = []
    for question in data:
        question_data = Question(question['question'], None)
        if type(question['answer']['value']) == list:
            question_data.set_answer_valid(question['answer']['value'])
        elif type(question['answer']['value']) == float:
            question_data.set_answer_valid([float(question['answer']['value'])])
        elif type(question['answer']['value']) == int:
            question_data.set_answer_valid([float(question['answer']['value'])])
        questions.append(question_data)
    return questions

def evaluate_questions(questions):
    nb_valid_questions = 0
    for question in questions:
        if question.valid:
            nb_valid_questions += 1
    return nb_valid_questions / len(questions)

def save_json_questions(json_questions, path):
    with open(path, 'w', encoding='utf-8') as outfile:
        json.dump(json_questions, outfile, ensure_ascii=False, indent=4)

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

parser = argparse.ArgumentParser(description='Test assistants on OpenAI.')
parser.add_argument('--data_test', default='data/test/test_data.json', help='Path to the JSON file containing test data')
parser.add_argument('--data_path', default='data/json', help='Path to the JSON file or directory containing JSON files')
parser.add_argument('--output', default='logs/assistants', help='Output directory')
parser.add_argument('--name', default='test_unil_assistant', help='Name of the assistant')
parser.add_argument('--model', default=os.getenv("MODEL_TO_USE"), help='Model to use')
args = parser.parse_args()

client = OpenAI()

file_manager = FileManager(client)

database = Data("assistants/database/database.db", init=True, path_init="assistants/database/init.sql")

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

[database.add_file(file.id, file.filename, 1) for file in files]

# Upload the proxy file
proxy_file = file_manager.send_file_to_openai(proxy_file_path)
database.add_file(proxy_file.id, proxy_file.filename, 3)

questions = prepare_data(open_test_data(args.data_test))

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

A noté que les proportions doivent être des floats (0.xx) et non des entiers (0).

A tout moment, Si le sujet de la question change, et que les fichiers pertinents sont différents, vous pouvez utiliser la fonction suivante pour recharger l'assistant avec uniquement le fichier proxy:

reload_assistant_with_only_proxy_file(proxy_file_id="file_id")

A noté que passé un certain nombre de fichiers (20) l'assistant ne pourra plus être rechargé avec de nouveaux fichiers. Dans ce cas, il faudra impérativement recharger l'assistant avec uniquement le fichier proxy.

Encore une fois je ne veux aucun texte en dehors de la réponse, et la réponse doit être structurée comme indiqué ci-dessus et rien de plus aucun autre format ne sera accepté pas de phrases.

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

output = []
json_questions = {
        'model': args.model,
        'type': "assistants",
        'epochs': "not applicable",
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'nb_questions': len(questions),
        'questions': [],
        'accuracy': 0
}
# Interaction loop
for question in questions:
    thread.send_message(question.question, Role.USER)

    run.start()
    run.execute_and_monitor(FUNCTIONS_TO_HANDLE)

    messages_all = thread.get_messages()
    last_message = messages_all.data[0].content[0].text.value
    valeurs = []
    try:
        last_message = json.loads(last_message)
        valeurs = last_message['valeurs']
        print(f"Last message: answer: {last_message['answer']}, valeurs: {last_message['valeurs']}")
    except:
        print(f"Last message: {last_message}")
        pass

    if len(valeurs) == 0:
        valeurs = None
    else:
        valeurs = [float(valeur) for valeur in valeurs]
    
    print(f"Question: {question.question}")
    print(f"Valeurs: {valeurs}")
    print(f"Answer valid: {question.answer_valid}")

    question.set_answer(valeurs)
    question.set_valid(question.evaluate())
    json_questions['questions'].append(question.to_json())
    
    time.sleep(10)

json_questions['accuracy'] = evaluate_questions(questions)

path = f"logs/assistants/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json"

save_json_questions(json_questions, path)

# Clean up
assistant.delete()
print("Assistant deleted with ID: " + assistant.assistant_id)

# Delete files
for file in files:
    file_manager.delete_file(file.id)
print("Files deleted with ID: " + str([file.id for file in files]))

file_manager.delete_file(proxy_file.id)
print("Proxy file deleted with ID: " + proxy_file.id)

# Disconnect from the database
database.disconnect()