# Fine tunning the LLM model 
# last update: 07/29/2024
# Author: Georgia LIu 

import evaluate
import numpy as np
from scipy.special import softmax
from transformers import Trainer
from transformers import AutoModelForSequenceClassification
from transformers import TrainingArguments
from torch.utils.data import DataLoader
import torch.nn.functional as F
from transformers import AutoTokenizer, DataCollatorWithPadding, AutoModel
import os
from datasets import DatasetDict
from datasets import Dataset
from datasets import load_dataset
import pandas as pd
from pathlib import Path
import torch
from torch import nn

from subprocess import call
import torch
import sys
from imblearn.under_sampling import RandomUnderSampler

# !nvidia-smi

# Set up for GPU 
if torch.cuda.is_available():
    print("CUDA is available! 🎉")
    print("Number of CUDA devices:", torch.cuda.device_count())
else:
    print("CUDA is not available. 🙁")


# activate GPU device
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Activate GPU device: ", device)

# %% [markdown]
# # Load dataset
cwd = Path.cwd()
# Get the path to the parent directory
parent_dir = cwd.parent

# Add the parent directory to the Python path
sys.path.append(str(parent_dir))
parent_dir = Path(cwd).parent
# %%
# use "/" instead of "\" in the path in windows machine
# training_dataset_path = "C:/Users/GL665/Code/Phrame-MentalMaps/data/processed/SYNCH/training_set/training_set_0715_var_A0729.csv"
training_dataset_path = "C:/Users/GL665/Code/Phrame-MentalMaps/data/processed/SYNCH/training_set/training_set_0711_def.csv"

# %%
# When training and test set is in one dataset
my_dataset = pd.read_csv(training_dataset_path)
my_dataset = my_dataset[['sentence1', 'sentence2', 'label', 'idx']]
print("Read dataset.....")
print("Originial dataset head")
print(my_dataset.head())
# delete rows with missing values
my_dataset = my_dataset.dropna()
# print(my_dataset.isna().sum())

# %%
# delete rows if the row does not equal to "1" or "0"
# my_dataset = my_dataset[my_dataset['label'].isin(['0', '1'])]
# print("Dataset shape after deleting rows that are not 0 or 1:", my_dataset.shape)


# set datatype for label and idx as int
my_dataset['label'] = my_dataset['label'].astype(int)
my_dataset['idx'] = my_dataset['idx'].astype(int)

# Check if the dataset is balanced
print("Dataset label distribution:", my_dataset['label'].value_counts())

# # Under sampling
# rus = RandomUnderSampler(random_state=42, sampling_strategy="majority")
# X_resampled, y_X_resampled = rus.fit_resample(
#     my_dataset[['sentence1', 'sentence2']], my_dataset['label'])

# my_dataset_resampled = pd.concat(
#     [X_resampled, y_X_resampled], axis=1)

# my_dataset_resampled['idx'] = my_dataset_resampled.index
# print(my_dataset_resampled.head())

#%%


my_dataset = Dataset.from_pandas(my_dataset, preserve_index=False)
train_test_dataset = my_dataset.train_test_split(test_size=0.4, shuffle=True, seed=42)
test_valid = train_test_dataset['test'].train_test_split(
    test_size=0.5, shuffle=True, seed=42)

# raw_train_dataset = raw_datasets["train"]

# gather everyone if you want to have a single DatasetDict
raw_datasets = DatasetDict({
    'train': train_test_dataset['train'],
    'test': test_valid['test'],
    'validation': test_valid['train']})

print(raw_datasets)


# %%
checkpoint = 'sentence-transformers/all-mpnet-base-v2'
print("My NLP Pre-Trained model", checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModel.from_pretrained(checkpoint)

model.to(device)  # Move model to the device

# %%

def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)


tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
print(tokenized_datasets)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# %% [markdown]
# # prepare for training

# %%
tokenized_datasets = tokenized_datasets.remove_columns(
    ["sentence1", "sentence2", "idx"])

tokenized_datasets = tokenized_datasets.rename_column("label", "labels")

tokenized_datasets.set_format("torch")

tokenized_datasets['train'].column_names

# %%
tokenized_datasets

# %%
# samples = tokenized_datasets["train"][:8]
# samples = {k: v for k, v in samples.items() if k not in ["idx", "sentence1", "sentence2"]}
# [len(x) for x in samples["input_ids"]]

# %%

train_dataloader = DataLoader(
    tokenized_datasets["train"], shuffle=True, batch_size=8, collate_fn=data_collator
)
eval_dataloader = DataLoader(
    tokenized_datasets["test"], batch_size=8, collate_fn=data_collator
)

# %%
for batch in train_dataloader:
    break
{k: v.shape for k, v in batch.items()}

# %%
# Move the batch of data to the same device
for key in batch.keys():
    batch[key] = batch[key].to(device)

# %% [markdown]
# # train the model

# %% [markdown]
# ## train with trainer

# %%

training_args = TrainingArguments(
    output_dir=os.path.join(parent_dir, 'models/fine_tune_model'))

# %%

model = AutoModelForSequenceClassification.from_pretrained(
    checkpoint, num_labels=2)

# %%
# Change to CustomTrainer to use custom loss function instead of Trainer


class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.get("labels")
        # forward pass
        outputs = model(**inputs)
        logits = outputs.get('logits')
        
        # compute custom loss
        # class 0: when the model predicts 0, class 1: when the model predicts 1
        class_weights = [0.5, 0.5]
        loss_fct = nn.CrossEntropyLoss(
            weight=torch.tensor(class_weights), 
            reduction='mean').to(device) # move to device
        loss = loss_fct(
            logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss

trainer = CustomTrainer(
    model,
    training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    data_collator=data_collator,
    tokenizer=tokenizer,
)

# %%
print("Start training....")
trainer.train()
print("Finished training")

# %% [markdown]
# Transform the logits to real predictions

# %%
print("Start prediction....")
predictions = trainer.predict(tokenized_datasets["test"])
print("Finished prediction")
# print("prediction shape: ", predictions.predictions.shape)
# print("label shape: ", predictions.label_ids.shape)

# %% [markdown]
# using softmax to get the probability of the class. first column is when the class is 0, second column is when the class is 1..

# %%
probs = softmax(predictions.predictions, axis=1)
# print(probs[1:20])

# %% [markdown]
# use argmax to get the final predicted class (where the class would be either 0 or 1)

# %%

preds = np.argmax(predictions.predictions, axis=-1)
# print(preds[1:20])

# %% [markdown]
# ## Print validation set

# %%
validation_dataset = tokenized_datasets["validation"]

# %%
raw_validation_dataset = raw_datasets["validation"]
# raw_validation_dataset[0]

# %% [markdown]
# # evaluate

# %%
metric = evaluate.combine(["accuracy", "f1", "precision", "recall"])
# metric = evaluate.load("accuracy")#, "", "recall", "f1", "mape")
model.eval()
for batch in eval_dataloader:
    batch = {k: v.to(device) for k, v in batch.items()}
    with torch.no_grad():
        outputs = model(**batch)

    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)
    metric.add_batch(predictions=predictions, references=batch["labels"])

print("Evaluating...")
results = metric.compute()

s = pd.Series(results)
res = s.round(3).to_dict()
print("Results:", str(res))



# %% [markdown]
# # Inference
#
# Let's test the model on a new sentence:

# # %%
# raw_datasets['validation'][0]

# # %%
# sentence1 = "child welfare system intervention"
# sentence2 = "children removed from house"
# sentence3 = "I am climbing and looking for a climbing partner"

# # %%

# encoding = tokenizer(sentence1, sentence2, return_tensors="pt")
# encoding = {k: v.to(trainer.model.device) for k, v in encoding.items()}

# outputs = trainer.model(**encoding)
# print(outputs)

# %% [markdown]
# The logits that come out of the model are of shape (batch_size, num_labels). As we are only forwarding a single sentence through the model, the `batch_size` equals 1. The logits is a tensor that contains the (unnormalized) scores for every individual label.

# %% [markdown]
# To turn them into actual predicted labels, we first apply a sigmoid function independently to every score, such that every score is turned into a number between 0 and 1, that can be interpreted as a "probability" for how certain the model is that a given class belongs to the input text.
#
# Next, we use a threshold (typically, 0.5) to turn every probability into either a 1 (which means, we predict the label for the given example) or a 0 (which means, we don't predict the label for the given example).

# %% [markdown]
# # Save Pre-trained Model

# %%
# dataset_folder_path = 'models/fine_tune_model/03_training_set_0711_var'

# cwd = os.getcwd()

# parent_dir = Path(cwd).parent


# folder_path = str(parent_dir / dataset_folder_path)
# print(folder_path)

# %%
# trainer.save_model(folder_path)

# %%
# new_model = AutoModelForSequenceClassification.from_pretrained(folder_path)
