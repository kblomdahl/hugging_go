from .tokenizer import VOCAB_SIZE

from transformers.trainer_utils import get_last_checkpoint
from transformers import Trainer, TrainingArguments
from transformers import MistralConfig, MistralForCausalLM
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np

_MODEL_PATH = 'model/'


def _model_config():
    return MistralConfig(
        vocab_size=VOCAB_SIZE,

        # Numbers just made up by me ¯\_(ツ)_/¯
        hidden_size=224,
        intermediate_size=784,

        num_hidden_layers=8,
        num_attention_heads=8,
        num_key_value_heads=2,
    )

def _model():
    return MistralForCausalLM(_model_config())

def _softmax(x):
    delta = x - np.max(x)
    return np.exp(delta) / np.exp(delta).sum()

def pretrained_model():
    latest_checkpoint = get_last_checkpoint(_MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(latest_checkpoint)
    tokenizer = AutoTokenizer.from_pretrained(latest_checkpoint)

    def _pipeline(text, next_color):
        tokens = tokenizer(
            f'{tokenizer.bos_token} {text}',
            return_tensors='pt',
            add_special_tokens=False
        )
        result = model.forward(input_ids=tokens['input_ids'])
        logits = result.logits[0, -1, :].detach().numpy()
        non_special_tokens = {
            token: index for token, index in tokenizer.get_added_vocab().items()
            if token.startswith(str(next_color))
        }
        scores = _softmax(logits[list(non_special_tokens.values())])
        candidates = [
            { 'label': label, 'score': score }
            for label, score in zip(non_special_tokens.keys(), scores)
        ]

        return [candidates]

    return _pipeline

def train(dataset, *, tokenizer):
    dataset = dataset.shuffle()

    trainer = Trainer(
        model=_model(),
        args=TrainingArguments(
            output_dir=_MODEL_PATH,
            overwrite_output_dir=True,
            per_device_train_batch_size=128,
            fp16=True,
        ),
        train_dataset=dataset['train'],
        tokenizer=tokenizer
    )
    trainer.train()
