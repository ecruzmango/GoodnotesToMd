'''
REQUIREMENTS:
1. requirements to run pretrained model: pip install transformers datasets evaluate torch
2. Create a hugging face account + Token || go to https://huggingface.co/join || After signing up, go to Settings > Access Tokens || Generate a token with write permissions || Save it securely
3. TrOCR is ideal for handwritten or digital text from image. EXAMPLE MODEL: microsoft/trocr-base-handwritten
'''

'''
HEADERS:
1. transformers library is an open-source Python library that provides a unified interface for working w/ thousands of pre trained models
2. TroOCRProcessor - combines a feature extractor and tokenizer || it handles converting images into pixel vals for the model and converts pred. token IDs into readable text
3. VisionEncoderDecoderModel - 

'''
import os
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from datasets import load_metric

from src.utils import GoodnotesDataset
from torch.utils.data import random_split

# load model/processor
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

# load your data
image_paths = [...]
texts = [...]

# split dataset
dataset = GoodnotesDataset(image_paths,texts, processor)
train_size = int(0.9* len(dataset))
train_dataset, val_dataset = random_split(dataset, [train_size, len(dataset) - train_size])

# training args
training_args = Seq2SeqTrainingArguments(
    output_dir="./models/trocr_finetuned",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    predict_with_generate=True,
    logging_dir="./logs",
    save_strategy="epoch",
    evaluation_strategy="epoch",
    num_train_epochs=5,
    fp16=True,
    push_to_hub=False,
)

# Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=processor,
)

trainer.train()

# Save model
model.save_pretrained("models/trocr_finetuned")
processor.save_pretrained("models/trocr_finetuned")