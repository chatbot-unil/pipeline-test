import json
import argparse
import os
import random

parser = argparse.ArgumentParser(description="Create dataset for testing.")
parser.add_argument('--data', type=str, default='data/pool_data', help='Path to question data')
parser.add_argument('--nb', type=int, default=10, help='Number of questions to test')
parser.add_argument('--output', type=str, default='data/test', help='Output directory')
args = parser.parse_args()

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

def save_json(data, path):
	with open(path, 'w', encoding='utf-8') as outfile:
		json.dump(data, outfile, ensure_ascii=False, indent=4)

if os.path.isdir(args.data):
	data = open_all_question_data(args.data)
	
elif os.path.isfile(args.data):
	data = [open_question_data(args.data)]

data_one_tab = process_data_dir(data)
random.shuffle(data_one_tab)

final_data = data_one_tab[:args.nb]

data_filename = os.path.join(args.output, 'test_data.json')

save_json(final_data, data_filename)