import os
import argparse
from dotenv import load_dotenv
import json
import subprocess
import threading
import time

parser = argparse.ArgumentParser(description='Test Pipeline subprocesses')
parser.add_argument('--pool', default='data/pool_data/pool_1_data.json', help='Path to the JSON file containing test data')
parser.add_argument('--pool_type', default='pool_1', help='Type of pool')
parser.add_argument('--dataset', default='data/test/test_data.json', help='Path to the JSON file containing test data')
parser.add_argument('--nb', default=10, help='Number of questions to test')
parser.add_argument('--nb_times', default=1, help='Number of times to test the pipeline')
args = parser.parse_args()

#model = ['gpt-4-1106-preview', 'gpt-4-turbo-preview']
#name = ['test_unil_assistant', 'test_unil_assistant_turbo']

model = ['gpt-4-1106-preview']
name = ['test_unil_assistant']

def create_dataset():
	# python3 create_test_dataset.py --data data/pool_data/pool_1_data.json --nb 30
	subprocess.run(["python3", "create_test_dataset.py", "--data", args.pool, "--nb", str(args.nb)])
	print("Dataset created")

def test_finetuning():
	# python3 test_finetuning.py --data data/test/test_data.json
	subprocess.run(["python3", "test_finetuning.py", "--data", args.dataset, "--pool_type", args.pool_type])
	print("Finetuning tested")

def test_assistants(model, name):
	# python3 test_assistants.py --data_test data/test/test_data.json --name test_unil_assistant --model gpt-4-1106-preview
	subprocess.run(["python3", "test_assistants.py", "--data_test", args.dataset, "--name", name, "--model", model, "--pool_type", args.pool_type])
	print("Assistant {} tested".format(model))

def create_plot():
	# python3 create_box_plot.py --path logs/assistants
	subprocess.run(["python3", "create_box_plot.py", "--path", "logs", "--pool_type", args.pool_type])
	print("Plots created")

if __name__ == "__main__":
	nb_times = int(args.nb_times)
	for i in range(nb_times):
		create_dataset()
		test_finetuning()
		for i in range(len(model)):
			test_assistants(model[i], name[i])
		print("All assistants tested")
		time.sleep(5)
		create_plot()