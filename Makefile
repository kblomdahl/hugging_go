TESTS = $(wildcard tests/test*.py)

test: build-test-image $(TESTS)
	docker run -v $(CURDIR):/app -w /app `docker build -qf Dockerfile.test .` python3 -m unittest $(TESTS)

build-test-image:
	DOCKER_BUILDKIT=1 docker build -f Dockerfile.test .

build-image: dist/hugging_go-0.0.0-py3-none-any.whl
	docker build -f Dockerfile .

clean:
	rm -rf model/checkpoint-*

dist/hugging_go-0.0.0-py3-none-any.whl: pyproject.toml setup.cfg
	python3 -m build --wheel
