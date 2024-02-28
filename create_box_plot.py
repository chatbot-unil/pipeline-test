import os
import re
import json
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description='Create box plot')
parser.add_argument('--path', default='logs', help='Path to the logs folder')
parser.add_argument('--plots', default='plots', help='Type of boxplot to create')
parser.add_argument('--pool_type', default='pool_1', help='Type of pool')
args = parser.parse_args()

def group_data_by_pool_type(data):
    dict_data = {}
    for d in data:
        if d['pool_type'] not in dict_data:
            dict_data[d['pool_type']] = {}
        if d['model'] not in dict_data[d['pool_type']]:
            dict_data[d['pool_type']][d['model']] = []
        dict_data[d['pool_type']][d['model']].append(d['accuracy'] * 100)
    return dict_data

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
        elif "assistant" in root:
            for file in files:
                with open(root + "/" + file, "r") as f:
                    data = f.read()
                    data = json.loads(data)
                    assistant_array.append(data)

    return finetuning_array, assistant_array
    
def create_plot_finetuning(finetuning_array):
    data = group_data_by_pool_type(finetuning_array)
    num_subplots = len(data[args.pool_type])
    fig, ax = plt.subplots(1, num_subplots,  figsize=(num_subplots * 4, 5))
    fig.suptitle('Finetuning accuracy')
    if num_subplots == 1:
        ax = [ax]
    for model in enumerate(data[args.pool_type]):
        ax[model[0]].boxplot(data[args.pool_type][model[1]])
        ax[model[0]].set_title(model[1] + "\n" + args.pool_type)
        ax[model[0]].set_ylabel('Accuracy in %')
        ax[model[0]].set_xlabel('Number of test ' + str(len(data[args.pool_type][model[1]])))
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    path = f"{args.plots}/{args.pool_type}/finetuning_accuracy.png"
    if not os.path.exists(f"{args.plots}/{args.pool_type}"):
        os.makedirs(f"{args.plots}/{args.pool_type}")
    plt.savefig(path)

def create_plot_assistant(assistant_array):
    data = group_data_by_pool_type(assistant_array)
    num_subplots = len(data[args.pool_type])
    fig, ax = plt.subplots(1, num_subplots,  figsize=(num_subplots * 4, 5))
    fig.suptitle('Assistant accuracy')
    if num_subplots == 1:
        ax = [ax]
    for model in enumerate(data[args.pool_type]):
        ax[model[0]].boxplot(data[args.pool_type][model[1]])
        ax[model[0]].set_title(model[1] + "\n" + args.pool_type)
        ax[model[0]].set_ylabel('Accuracy in %')
        ax[model[0]].set_xlabel('Number of test ' + str(len(data[args.pool_type][model[1]])))
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    path = f"{args.plots}/{args.pool_type}/assistant_accuracy.png"
    if not os.path.exists(f"{args.plots}/{args.pool_type}"):
        os.makedirs(f"{args.plots}/{args.pool_type}")
    plt.savefig(path)

if not os.path.exists(args.plots):
    os.makedirs(args.plots)
finetuning_array, assistant_array = get_all_logs(args.path)
create_plot_finetuning(finetuning_array)
create_plot_assistant(assistant_array)