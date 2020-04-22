.DEFAULT: build

PWD = $(shell pwd)

DOCKER_IMAGE = genus-codice
TRAIN_DOCKER_IMAGE = genus-codice-train

.PHONY: build
build:
	docker build -t $(DOCKER_IMAGE) .

.PHONY: train
train:
	docker build -f Dockerfile.train -t $(TRAIN_DOCKER_IMAGE) .
	docker run --rm -it \
		-v $(PWD)/data:/usr/src/data \
		$(TRAIN_DOCKER_IMAGE)
