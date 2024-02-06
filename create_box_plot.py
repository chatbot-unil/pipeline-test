import os
import re
import json
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description='Create box plot')
parser.add_argument('--path', default='logs', help='Path to the logs folder')
parser.add_argument('--plots', default='plots', help='Type of boxplot to create')
args = parser.parse_args()


def get_all_logs(path):
    finetuning_array = []
    assistant_array = []
    for root, dirs, files in os.walk(path):
        if "finetunning" in root:
            for file in files:
                    with open(root + "/" + file, "r") as f:
                        data = f.read()
                        data = json.loads(data)
                        finetuning_array.append(data)
        elif "assistant" in root and "old" not in root:
            for file in files:
                with open(root + "/" + file, "r") as f:
                    data = f.read()
                    data = json.loads(data)
                    assistant_array.append(data)

    return finetuning_array, assistant_array

def create_plot_finetuning(finetuning_array):
    dict_finetuning = {}
    for data in finetuning_array:
        if data['model'] not in dict_finetuning:
            dict_finetuning[data['model']] = []
        dict_finetuning[data['model']].append(data['accuracy'] * 100)
    
    # subboxplot for the accuracy of eatch model
    num_subplots = len(dict_finetuning)
    fig, ax = plt.subplots(1, num_subplots,  figsize=(num_subplots * 4, 5))
    fig.suptitle('Finetuning accuracy')
    if num_subplots == 1:
        ax = [ax]
    for model in enumerate(dict_finetuning):
        ax[model[0]].boxplot(dict_finetuning[model[1]])
        ax[model[0]].set_title(model[1])
        ax[model[0]].set_ylabel('Accuracy in %')
        ax[model[0]].set_xlabel('Number of test ' + str(len(dict_finetuning[model[1]])))
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(args.plots + "/finetuning_accuracy.png")


def create_plot_assistant(assistant_array):
    dict_assistant = {}
    for data in assistant_array:
        if data['model'] not in dict_assistant:
            dict_assistant[data['model']] = []
        dict_assistant[data['model']].append(data['accuracy'] * 100)

    # subboxplot for the accuracy of eatch model
    num_subplots = len(dict_assistant)
    fig, ax = plt.subplots(1, num_subplots,  figsize=(num_subplots * 4, 5))
    fig.suptitle('Assistant accuracy')
    if num_subplots == 1:
        ax = [ax]
    for model in enumerate(dict_assistant):
        ax[model[0]].boxplot(dict_assistant[model[1]])
        ax[model[0]].set_title(model[1])
        ax[model[0]].set_ylabel('Accuracy in %')
        ax[model[0]].set_xlabel('Number of test ' + str(len(dict_assistant[model[1]])))
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(args.plots + "/assistant_accuracy.png")

if not os.path.exists(args.plots):
	os.makedirs(args.plots)
finetuning_array, assistant_array = get_all_logs(args.path)
create_plot_finetuning(finetuning_array)
create_plot_assistant(assistant_array)