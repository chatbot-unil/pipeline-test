import json
import argparse
import os
from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser(description='Create test pool data from JSON files.')
parser.add_argument('--datapath', default='data/json', help='Path to the JSON file or directory containing JSON files')
parser.add_argument('--questionspath', default='data/templates/', help='Path to the JSON file or directory containing JSON files')
args = parser.parse_args()

env = Environment(loader=FileSystemLoader(args.questionspath + 'pools/'))

def open_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def open_jsons(path):
    jsons = {}
    for filename in os.listdir(path):
        if filename.endswith(".json") and filename != 'proxy.json':
            json_path = os.path.join(path, filename)
            filiere = get_filiere(json_path)
            jsons[filiere] = open_json(json_path)
    return jsons

def get_filiere(path):
    filename_with_extension = path.split('/')[-1]
    filiere = filename_with_extension.split('.')[0]
    return filiere

def create_question_from_template(template, data):
    questions = template.render(data).split('\n')
    questions = [q for q in questions if q.strip()]
    return questions

def create_data_from_file(data):
    formatted_data = {}
    for filiere in data:
        data_filiere = data[filiere]
        formatted_data[filiere] = {
        }
            

if __name__ == '__main__':
    jsons_data = open_jsons(args.datapath)

    data = create_data_from_file(jsons_data)

    # Chargement du template
    template = env.get_template('pool_1.j2')

    # Variables à passer au template
    data = {
        'sexe': 'masculin',
        'faculte': 'Sciences',
        'annee': '2024',
        'ch_etrangers': 'CH'
    }

    # Création du tableau de questions
    questions_tableau = create_question_from_template(template, data)

    # Affichage du tableau de questions
    for question in questions_tableau:
        print(question)