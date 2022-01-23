TESTS = $(wildcard tests/test*.py)

test: build-image $(TESTS)
	docker run -v $(CURDIR):/app -w /app `docker build -q .` python3 -m unittest $(TESTS)

build-image:
	docker build .

clean:
	rm -rf model/checkpoint-*

