from question import Question
import json
import os
import argparse
from openai import OpenAI
from datetime import datetime
import random
import re

from dotenv import load_dotenv

parser = argparse.ArgumentParser(description="Fine-tune OpenAI model.")
parser.add_argument('--model', type=str, default='', help='Model to test')
parser.add_argument('--data', type=str, default='data/pool_data', help='Path to question data')
parser.add_argument('--question', type=str, default='', help='Question to test')
parser.add_argument('--nb_questions', type=int, default=10, help='Number of questions to test')
parser.add_argument('--pool_type', type=str, default='pool_1', help='Type of pool')
args = parser.parse_args()

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
system_message = os.getenv("SYSTEM_MESSAGE")

client = OpenAI()

def open_question_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def open_all_question_data(path):
    all_data = []
    for filename in os.listdir(path):
        if filename.endswith('.json'):
            all_data.append(open_question_data(os.path.join(path, filename)))
    return all_data

def process_data_dir(data):
    processed_data = []
    for d in data:
        for q in d:
            for a in q:
                processed_data.append(a)
    return processed_data

def get_last_fine_tuned_model():
    list_models = client.fine_tuning.jobs.list(limit=5)
    for model in list_models.data:
        if model.status == 'succeeded':
            created_at = datetime.utcfromtimestamp(model.created_at).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Model name: {model.fine_tuned_model} - Created at: {created_at} - Epochs: {model.hyperparameters.n_epochs}")
            return model.fine_tuned_model, model.hyperparameters.n_epochs
    return None

def get_args_model_info():
    list_models = client.fine_tuning.jobs.list(limit=50)
    for model in list_models.data:
        if model.fine_tuned_model == args.model:
            if model.status == 'succeeded':
                created_at = datetime.utcfromtimestamp(model.created_at).strftime('%Y-%m-%d %H:%M:%S')
                print(f"Model name: {model.fine_tuned_model} - Created at: {created_at} - Epochs: {model.hyperparameters.n_epochs}")
                return model.fine_tuned_model, model.hyperparameters.n_epochs
    return None

def evaluate_questions(questions):
    nb_valid_questions = 0
    for question in questions:
        if question.valid:
            nb_valid_questions += 1
    return nb_valid_questions / len(questions)

def completions(message, model_id):
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": message},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content

def extract_number_from_string(input_string):
    numbers = re.findall(r'[+-]?[0-9]+(?:\.[0-9]+)?', input_string)
    # test if it's a float
    if len(numbers) > 1:
        return [float(x) for x in numbers]
    else:
        return float(numbers[0]) if numbers else None

def test_question(question):
    response = completions(question.question, model_id)
    print(f"Question: {question.question}")
    print(f"Valid answer: {question.answer_valid}")
    answer = extract_number_from_string(response)
    print(f"Model answer: {answer}")
    question.set_answer(answer)

def save_json_questions(json_questions, path):
    with open(path, 'w', encoding='utf-8') as outfile:
        json.dump(json_questions, outfile, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    if args.model == '':
        model_id , epochs = get_last_fine_tuned_model()
    else:
        model_id , epochs = get_args_model_info()

    data_one_tab = []

    if os.path.isdir(args.data):
        data = open_all_question_data(args.data)
        data_one_tab = process_data_dir(data)
        random.shuffle(data_one_tab)
        nb_questions = args.nb_questions
        
    elif os.path.isfile(args.data):
        data = [open_question_data(args.data)]
        data_one_tab = data[0] 
        nb_questions = len(data[0])

    questions = []
    json_questions = {
        'model': model_id,
        'type': "fine-tuning",
        'epochs': epochs,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'nb_questions': nb_questions,
        'pool_type': args.pool_type,
        'questions': [],
        'accuracy': 0
    }

    if args.question == '':
        for question in data_one_tab[:nb_questions]:
            if question['answer']['value'] is type(float):
                questions.append(Question(question['question'], float(question['answer']['value'])))
            else:
                questions.append(Question(question['question'], question['answer']['value']))

        for question in questions:
            test_question(question)
            question.set_valid(question.evaluate())
            json_questions['questions'].append(question.to_json())

        json_questions['accuracy'] = evaluate_questions(questions)

        path = f"logs/finetunning/{args.pool_type}/{model_id}/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json"
        # path = f"logs/finetunning/{model_id}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json"
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        save_json_questions(json_questions, path)
        print("Test finished and saved in " + path)