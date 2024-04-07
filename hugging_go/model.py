from .tokenizer import VOCAB_SIZE

from dataclasses import dataclass
from transformers.trainer_utils import get_last_checkpoint
from transformers import AutoTokenizer, Trainer, TrainingArguments, Cache
from transformers import MistralConfig, MistralModel, MistralPreTrainedModel
from transformers.modeling_outputs import ModelOutput
from torch import nn
from typing import Tuple, Optional
import torch
import numpy as np

_MODEL_PATH = 'model/'

@dataclass
class CasualLMAndSequenceClassifierOutputWithPast(ModelOutput):
    loss: Optional[torch.FloatTensor] = None
    lm_logits: Optional[torch.FloatTensor] = None
    class_logits: Optional[torch.FloatTensor] = None
    past_key_values: Optional[Tuple[Tuple[torch.FloatTensor]]] = None
    hidden_states: Optional[Tuple[torch.FloatTensor, ...]] = None
    attentions: Optional[Tuple[torch.FloatTensor, ...]] = None
    cross_attentions: Optional[Tuple[torch.FloatTensor, ...]] = None


class MistralForCausalLMAndSequenceClassification(MistralPreTrainedModel):
    _tied_weights_keys = ["lm_head.weight", "score.weights"]

    def __init__(self, config):
        super().__init__(config)
        self.model = MistralModel(config)
        self.num_labels = config.num_labels
        self.vocab_size = config.vocab_size
        self.lm_head = nn.Linear(config.hidden_size, self.vocab_size, bias=False)
        self.score = nn.Linear(config.hidden_size, self.num_labels, bias=False)
        self.post_init()

    def get_input_embeddings(self):
        return self.model.embed_tokens

    def set_input_embeddings(self, value):
        self.model.embed_tokens = value

    def get_output_embeddings(self):
        return self.lm_head

    def set_output_embeddings(self, new_embeddings):
        self.lm_head = new_embeddings

    def set_decoder(self, decoder):
        self.model = decoder

    def get_decoder(self):
        return self.model

    def forward(
        self,
        input_ids = None,
        attention_mask = None,
        position_ids = None,
        past_key_values = None,
        inputs_embeds = None,
        labels = None,
        use_cache = None,
        output_attentions = None,
        output_hidden_states = None
    ):
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )

        transformer_outputs = self.model(
            input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
        )
        hidden_states = transformer_outputs[0]
        class_logits = self.score(hidden_states)
        lm_logits = self.lm_head(hidden_states)
        lm_logits = lm_logits.float()

        lm_loss = 0.0
        if labels is not None:
            # Shift so that tokens < n predict n
            shift_logits = lm_logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 2:].contiguous()
            # Flatten the tokens
            shift_logits = shift_logits.view(-1, self.config.vocab_size)
            shift_labels = shift_labels.view(-1)
            # Ensure tensors are on the same device
            shift_labels = shift_labels.to(shift_logits.device)
            loss_fct = nn.CrossEntropyLoss()
            lm_loss = loss_fct(shift_logits, shift_labels)

        if input_ids is not None:
            batch_size = input_ids.shape[0]
        else:
            batch_size = inputs_embeds.shape[0]

        if self.config.pad_token_id is None and batch_size != 1:
            raise ValueError("Cannot handle batch sizes > 1 if no padding token is defined.")
        if self.config.pad_token_id is None:
            sequence_lengths = -1
        else:
            if input_ids is not None:
                # if no pad token found, use modulo instead of reverse indexing for ONNX compatibility
                sequence_lengths = torch.eq(input_ids, self.config.pad_token_id).int().argmax(-1) - 1
                sequence_lengths = sequence_lengths % input_ids.shape[-1]
                sequence_lengths = sequence_lengths.to(class_logits.device)
            else:
                sequence_lengths = -1

        pooled_logits = class_logits[torch.arange(batch_size, device=class_logits.device), sequence_lengths]

        class_loss = 0.0
        if labels is not None:
            class_labels = labels[..., :1].to(class_logits.device)
            loss_fct = nn.CrossEntropyLoss()
            class_loss = loss_fct(pooled_logits.view(-1, self.num_labels), class_labels.view(-1))

        return CasualLMAndSequenceClassifierOutputWithPast(
            loss=lm_loss + class_loss,
            lm_logits=lm_logits,
            class_logits=pooled_logits,
            past_key_values=transformer_outputs.past_key_values,
            hidden_states=transformer_outputs.hidden_states,
            attentions=transformer_outputs.attentions,
        )

    def prepare_inputs_for_generation(
        self, input_ids, past_key_values=None, attention_mask=None, inputs_embeds=None, **kwargs
    ):
        # Omit tokens covered by past_key_values
        if past_key_values is not None:
            if isinstance(past_key_values, Cache):
                cache_length = past_key_values.get_seq_length()
                past_length = past_key_values.seen_tokens
                max_cache_length = past_key_values.get_max_length()
            else:
                cache_length = past_length = past_key_values[0][0].shape[2]
                max_cache_length = None

            # Keep only the unprocessed tokens:
            # 1 - If the length of the attention_mask exceeds the length of input_ids, then we are in a setting where
            # some of the inputs are exclusively passed as part of the cache (e.g. when passing input_embeds as
            # input)
            if attention_mask is not None and attention_mask.shape[1] > input_ids.shape[1]:
                input_ids = input_ids[:, -(attention_mask.shape[1] - past_length) :]
            # 2 - If the past_length is smaller than input_ids', then input_ids holds all input tokens. We can discard
            # input_ids based on the past_length.
            elif past_length < input_ids.shape[1]:
                input_ids = input_ids[:, past_length:]
            # 3 - Otherwise (past_length >= input_ids.shape[1]), let's assume input_ids only has unprocessed tokens.

            # If we are about to go beyond the maximum cache length, we need to crop the input attention mask.
            if (
                max_cache_length is not None
                and attention_mask is not None
                and cache_length + input_ids.shape[1] > max_cache_length
            ):
                attention_mask = attention_mask[:, -max_cache_length:]

        position_ids = kwargs.get("position_ids", None)
        if attention_mask is not None and position_ids is None:
            # create position_ids on the fly for batch generation
            position_ids = attention_mask.long().cumsum(-1) - 1
            position_ids.masked_fill_(attention_mask == 0, 1)
            if past_key_values:
                position_ids = position_ids[:, -input_ids.shape[1] :]

        # if `inputs_embeds` are passed, we only want to use them in the 1st generation step
        if inputs_embeds is not None and past_key_values is None:
            model_inputs = {"inputs_embeds": inputs_embeds}
        else:
            model_inputs = {"input_ids": input_ids}

        model_inputs.update(
            {
                "position_ids": position_ids,
                "past_key_values": past_key_values,
                "use_cache": kwargs.get("use_cache"),
                "attention_mask": attention_mask,
            }
        )
        return model_inputs

    @staticmethod
    def _reorder_cache(past_key_values, beam_idx):
        reordered_past = ()
        for layer_past in past_key_values:
            reordered_past += (
                tuple(past_state.index_select(0, beam_idx.to(past_state.device)) for past_state in layer_past),
            )
        return reordered_past

def _model_config(tokenizer):
    return MistralConfig(
        vocab_size=VOCAB_SIZE,
        num_labels=2,
        pad_token_id=tokenizer.convert_tokens_to_ids('[PAD]'),

        # Numbers just made up by me ¯\_(ツ)_/¯
        hidden_size=724,
        intermediate_size=2534,

        num_hidden_layers=8,
        num_attention_heads=8,
        num_key_value_heads=2,
    )

def _model(tokenizer):
    return MistralForCausalLMAndSequenceClassification(_model_config(tokenizer))

def _softmax(x):
    delta = x - np.max(x)
    return np.exp(delta) / np.exp(delta).sum()

def pretrained_model():
    latest_checkpoint = get_last_checkpoint(_MODEL_PATH)
    model = MistralForCausalLMAndSequenceClassification.from_pretrained(latest_checkpoint)
    tokenizer = AutoTokenizer.from_pretrained(latest_checkpoint)

    def _pipeline(text, next_color, past_key_values=None):
        tokens = tokenizer(
            f'{tokenizer.bos_token} {text}',
            return_tensors='pt',
            add_special_tokens=False
        )
        result = model.forward(
            input_ids=tokens['input_ids'],
            use_cache=past_key_values is not None,
            past_key_values=past_key_values
        )
        class_logits = result.class_logits[0, :].detach().numpy()
        lm_logits = result.lm_logits[0, -1, :].detach().numpy()
        non_special_tokens = {
            token: index for token, index in tokenizer.get_added_vocab().items()
            if token.startswith(str(next_color))
        }
        classes = _softmax(class_logits)
        scores = _softmax(lm_logits[list(non_special_tokens.values())])
        candidates = [
            { 'label': label, 'score': score }
            for label, score in zip(non_special_tokens.keys(), scores)
        ]

        if str(next_color) == 'B':
            winner = 1.0 * classes[0] + -1.0 * classes[1]
        else:
            winner = -1.0 * classes[0] + 1.0 * classes[1]

        return [candidates, winner, result.past_key_values]

    return _pipeline

def train(dataset, *, tokenizer):
    dataset = dataset.shuffle()

    trainer = Trainer(
        model=_model(tokenizer),
        args=TrainingArguments(
            output_dir=_MODEL_PATH,
            overwrite_output_dir=True,
            save_total_limit=5,
            per_device_train_batch_size=128,
            bf16=True,
        ),
        train_dataset=dataset['train'],
        tokenizer=tokenizer
    )
    trainer.train()
