TESTS = $(wildcard tests/test*.py)

test: build-test-image $(TESTS)
	docker run -v $(CURDIR):/app -w /app `docker build -qf Dockerfile.test .` python3 -m unittest $(TESTS)

build-test-image:
	docker build -f Dockerfile.test .

clean:
	rm -rf model/checkpoint-*

