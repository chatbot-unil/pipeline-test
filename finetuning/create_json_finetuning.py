import json
import os
import argparse
from dotenv import load_dotenv
import random

parser = argparse.ArgumentParser(description="Create JSON file for fine-tuning OpenAI model.")
parser.add_argument('--training_data', type=str, default='../data/finetuning/training/pool_data.jsonl', help='Path to training data')
parser.add_argument('--validating_data', type=str, default='../data/finetuning/validating/pool_data.jsonl', help='Path to validating data')
parser.add_argument('--path_to_pool_data', type=str, default='../data/pool_data', help='Path to pool data')

args = parser.parse_args()

load_dotenv()

system_message = os.getenv("SYSTEM_MESSAGE")

def open_json_data(path_to_file):
    with open(path_to_file) as json_file:
        data = json.load(json_file)
    return data

def open_all_json_data(path_to_folder):
    data = []
    for filename in os.listdir(path_to_folder):
        if filename.endswith(".json"):
            data.append(open_json_data(path_to_folder + "/" + filename))
    return data

def write_jsonl_data(data, path_to_file):
    with open(path_to_file, 'w', encoding='utf-8') as f:
        for example in data:
            json.dump(example, f, ensure_ascii=False)
            f.write('\n')
            
def create_training_data(sentences, system_message, repeat_times=1):
    """Creates training data in chat-completion format for each question-answer pair, repeated 'repeat_times' times."""
    training_data = []
    for sentence in sentences:
        for data in sentence:
            entry = {
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": data["question"]},
                    {"role": "assistant", "content": str(data["answer"])}
                ]
            }
            training_data.append(entry)
    return training_data

if __name__ == "__main__":
    print("Creating JSONL files for fine-tuning...")
    print("Training file: " + args.training_data)
    print("Validating file: " + args.validating_data)
    print("system_message: " + system_message)

    training_data = open_all_json_data(args.path_to_pool_data)
    prepared_data = []

    for data in training_data:
        random.shuffle(data)
        prepared_data.append(create_training_data(data, system_message))

    for i in range(len(prepared_data)):
        random.shuffle(prepared_data[i])
        path_training = args.training_data[:-6] + str(i) + "-training.jsonl"
        path_validating = args.validating_data[:-6] + str(i) + "-validating.jsonl"
        print("Writing " + path_training + "...")
        print("Writing " + path_validating + "...")
        training_data = prepared_data[i][:int(len(prepared_data[i]) * 0.8)]
        validating_data = prepared_data[i][int(len(prepared_data[i]) * 0.8):]
        write_jsonl_data(training_data, path_training)
        write_jsonl_data(validating_data, path_validating)
