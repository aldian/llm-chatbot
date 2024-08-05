# Variables
IMAGE_NAME = llm-chatbot-image
CONTAINER_NAME = llm-chatbot
DOCKERFILE = Dockerfile
LLMS_CONTAINER_DIR = /usr/app/llms
CONTEXT_CONTAINER_DIR = /usr/app/context

# Default target
all: build run

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) -f $(DOCKERFILE) .

llms_host_dir_defined:
ifndef LLMS_DIR
	$(error Please set LLMS_DIR to the directory containing LLM models)
endif

context_host_dir_defined:
ifndef CONTEXT_DIR
	$(error Please set CONTEXT_DIR to the directory that will store conversations)
endif

# Run the Docker container with the shared folder
run: llms_host_dir_defined context_host_dir_defined
	docker run --name=$(CONTAINER_NAME) -v $(LLMS_DIR):$(LLMS_CONTAINER_DIR) -v $(CONTEXT_DIR):$(CONTEXT_CONTAINER_DIR) -it --rm $(IMAGE_NAME)

# Remove the Docker container
clean:
	docker rm -f $(CONTAINER_NAME) || true

# Remove the Docker image
clean-image:
	docker rmi -f $(IMAGE_NAME) || true

# Full cleanup
clean-all: clean clean-image

.PHONY: all build run clean clean-image clean-all
