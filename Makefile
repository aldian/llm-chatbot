# Variables
IMAGE_NAME = llm-chatbot-image
CONTAINER_NAME = ubuntu2204
DOCKERFILE = Dockerfile
LLMS_DIR = llms

# Default target
all: build run

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) -f $(DOCKERFILE) .

# Run the Docker container with the shared folder
run:
	docker run --name=$(CONTAINER_NAME) -v $(LLMS_DIR):/mnt/llms -it $(IMAGE_NAME)

# Remove the Docker container
clean:
	docker rm -f $(CONTAINER_NAME) || true

# Remove the Docker image
clean-image:
	docker rmi -f $(IMAGE_NAME) || true

# Full cleanup
clean-all: clean clean-image

.PHONY: all build run clean clean-image clean-all