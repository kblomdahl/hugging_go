from transformers import Trainer, TrainingArguments
from transformers import MobileBertConfig, MobileBertForSequenceClassification

def _mobilebert_config(features):
    id2label = {idx: features['label'].int2str(idx) for idx in range(362)}
    label2id = {value: key for key, value in id2label.items()}

    config = MobileBertConfig(
        num_labels=362,
        id2label=id2label,
        label2id=label2id
    )
    return config

def _mobilebert_model(features):
    return MobileBertForSequenceClassification(_mobilebert_config(features))

def from_pretrained():
    pipe = pipeline(
        'text-classification',
        model='model/'
        return_all_scores=True
    )

def train(dataset, *, tokenizer):
    def _tokenize_text(examples):
        return tokenizer(examples['text'], truncation=True, max_length=512)

    dataset = dataset.map(_tokenize_text, remove_columns=['text'], batched=True)
    features = dataset['train'].features

    trainer = Trainer(
        model=_mobilebert_model(features),
        args=TrainingArguments(
            output_dir='model/',
            overwrite_output_dir=True,
            per_device_train_batch_size=32,
            fp16=True,
        ),
        train_dataset=dataset['train'],
        tokenizer=tokenizer
    )
    trainer.train()
