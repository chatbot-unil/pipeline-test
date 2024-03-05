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
parser.add_argument('--model', default='', help='Model to test')
args = parser.parse_args()

def create_dataset():
	# python3 create_test_dataset.py --data data/pool_data/pool_1_data.json --nb 30
	subprocess.run(["python3", "create_test_dataset.py", "--data", args.pool, "--nb", str(args.nb)])
	print("Dataset created")

def test_finetuning():
	# python3 test_finetuning.py --data data/test/test_data.json
	subprocess.run(["python3", "test_finetuning.py", "--data", args.dataset, "--pool_type", args.pool_type, "--model", args.model])
	print("Finetuning tested")

def create_plot():
	# python3 create_box_plot.py --path logs/assistants
	subprocess.run(["python3", "create_box_plot.py", "--path", "logs", "--pool_type", args.pool_type])
	print("Plots created")

if __name__ == "__main__":
	nb_times = int(args.nb_times)
	for i in range(nb_times):
		create_dataset()
		test_finetuning()
		time.sleep(5)
	create_plot()