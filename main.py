import os
import argparse
from dotenv import load_dotenv
import json
import subprocess

parser = argparse.ArgumentParser(description='Test Pipeline subprocesses')
parser.add_argument('--pool', default='data/pool_data/pool_1_data.json', help='Path to the JSON file containing test data')
parser.add_argument('--dataset', default='data/test/test_data.json', help='Path to the JSON file containing test data')
parser.add_argument('--nb', default=30, help='Number of questions to test')
args = parser.parse_args()

# list of models to test for assistant

model = ['gpt-4-1106-preview', 'gpt-4-turbo-preview']
name = ['test_unil_assistant', 'test_unil_assistant_turbo']

def create_dataset():
	# python3 create_test_dataset.py --data data/pool_data/pool_1_data.json --nb 30
	subprocess.run(["python3", "create_test_dataset.py", "--data", args.pool, "--nb", str(args.nb)])
	print("Dataset created")

def test_finetuning():
	# python3 test_finetuning.py --data data/test/test_data.json
	subprocess.run(["python3", "test_finetuning.py", "--data", args.dataset])

def test_assistants(model, name):
	# python3 test_assistants.py --data_test data/test/test_data.json --name test_unil_assistant --model gpt-4-1106-preview
	subprocess.run(["python3", "test_assistants.py", "--data_test", args.dataset, "--name", name, "--model", model])

if __name__ == "__main__":
	create_dataset()
	test_finetuning()
	for i in range(len(model)):
		test_assistants(model[i], name[i])