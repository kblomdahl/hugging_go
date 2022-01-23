FROM huggingface/transformers-pytorch-cpu
COPY requirements.txt /tmp/requirements.txt
COPY dist/hugging_go-0.0.0-py3-none-any.whl /tmp/hugging_go-0.0.0-py3-none-any.whl
COPY model/ /workspace/model
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt
RUN python3 -m pip install /tmp/hugging_go-0.0.0-py3-none-any.whl
CMD python3 -m hugging_go
