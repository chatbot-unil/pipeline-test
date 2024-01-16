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
parser.add_argument('--data', type=str, default='../data/pool_data', help='Path to question data')
parser.add_argument('--question', type=str, default='', help='Question to test')
parser.add_argument('--nb_questions', type=int, default=10, help='Number of questions to test')
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
			return model.fine_tuned_model
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
    return float(numbers[0]) if numbers else None

def test_question(question):
	response = completions(question.question, model_id)
	question.set_answer(extract_number_from_string(response))

if __name__ == '__main__':
	if args.model == '':
		model_id = get_last_fine_tuned_model()
	else:
		model_id = args.model

	data_one_tab = []

	if os.path.isdir(args.data):
		data = open_all_question_data(args.data)
		
	elif os.path.isfile(args.data):
		data = [open_question_data(args.data)]

	data_one_tab = process_data_dir(data)
	random.shuffle(data_one_tab)	

	if args.question == '':
		questions = []
		for question in data_one_tab[:args.nb_questions]:
			questions.append(Question(question['question'], float(question['answer']['value'])))

		for question in questions:
			test_question(question)
			question.set_valid(question.evaluate())
			question.print_all()
		
		print(f"Accuracy: {evaluate_questions(questions) * 100}%")