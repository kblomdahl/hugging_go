# Transformers for Go

A little experiment at using transformers to play go. The basic concept is to feed a sequence of moves to the transformer and predict the next move.

## Run

A GTP interface can be started from the command-line, or if you prefer you can build a docker image that runs the bot in an isolated environment:

```
python3 -m hugging_go
```

### Docker

```
make build-image
docker run -it `docker build -q .`
```

## Build

```
pip install -r requirements.txt
```

## Training

### Tokenizer

You can train a tokenizer from scratch on a given dataset, which should consist of one-line SGF files. The resulting tokenizer will be saved to `model/tokenizer.json`:

```
python3 -m hugging_go train-tokenizer data/kgs_big.sgf
```

### Model

After training the tokenizer the main model can be trained using the same one-line SGF files. This will probably take a long time:

```
python3 -m hugging_go train-model data/kgs_big.sgf
```
