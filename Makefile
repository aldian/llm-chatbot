# Variables
IMAGE_NAME_CLI = llm-chatbot-image-cli
IMAGE_NAME_SVC_BASE = llm-chatbot-image-svc-base
IMAGE_NAME_SVC = llm-chatbot-image-svc
CONTAINER_NAME_CLI = llm-chatbot-cli
CONTAINER_NAME_SVC = llm-chatbot-svc
DOCKERFILE_CLI = Dockerfile.cli
DOCKERFILE_SVC_BASE = Dockerfile.svc_base
DOCKERFILE_SVC = Dockerfile.svc
LLMS_CONTAINER_DIR = /usr/app/llms
CONTEXT_CONTAINER_DIR = /usr/app/context

# Default target
all: build-svc run-cli

svc_port_defined:
ifndef SVC_PORT
	$(error Please set SVC_PORT to the port number for the service)
endif

# Build the Docker image
build-cli:
	docker build -t $(IMAGE_NAME_CLI) -f $(DOCKERFILE_CLI) .
build-svc-base:
	docker build -t $(IMAGE_NAME_SVC_BASE) -f $(DOCKERFILE_SVC_BASE) .
build-svc: svc_port_defined
	docker build --build-arg SVC_PORT=$(SVC_PORT) -t $(IMAGE_NAME_SVC) -f $(DOCKERFILE_SVC) .

llms_host_dir_defined:
ifndef LLMS_DIR
	$(error Please set LLMS_DIR to the full path of the directory containing LLM models)
endif

context_host_dir_defined:
ifndef CONTEXT_DIR
	$(error Please set CONTEXT_DIR to the full path of the directory that will store conversations)
endif

prompt_defined:
ifndef PROMPT
	$(error Please set PROMPT to communicate with the chatbot)
endif

# Run the Docker container with the shared folder
run-cli: llms_host_dir_defined context_host_dir_defined
	@docker run --name=$(CONTAINER_NAME_CLI) \
		-v $(LLMS_DIR):$(LLMS_CONTAINER_DIR) \
		-v $(CONTEXT_DIR):$(CONTEXT_CONTAINER_DIR) \
		-it --rm $(IMAGE_NAME_CLI) python main_cli.py \
		$(if "$(SYS)",--sys "$(SYS)") \
		$(if $(MODEL),--model $(MODEL)) \
		$(if "$(PROMPT)",--prompt "$(PROMPT)")

start-svc: llms_host_dir_defined context_host_dir_defined svc_port_defined
	@docker run --name=$(CONTAINER_NAME_SVC) \
		-v $(LLMS_DIR):$(LLMS_CONTAINER_DIR) \
		-v $(CONTEXT_DIR):$(CONTEXT_CONTAINER_DIR) \
		-p $(SVC_PORT):$(SVC_PORT) \
		-it --rm -d $(IMAGE_NAME_SVC)

svc-init-conversation: svc_port_defined
	@#python main_svc_cli.py --svc-port $(SVC_PORT) --init-conversation
	@docker exec -it $(CONTAINER_NAME_SVC) python3 main_svc_cli.py --svc-port $(SVC_PORT) --init-conversation

svc-prompt: svc_port_defined prompt_defined
	@docker exec -it $(CONTAINER_NAME_SVC) python3 main_svc_cli.py --svc-port $(SVC_PORT) \
		$(if "$(SYS)",--sys "$(SYS)") \
		$(if $(MODEL),--model $(MODEL)) \
		$(if "$(PROMPT)",--prompt "$(PROMPT)")

# Remove the Docker container
clean-cli:
	docker rm -f $(CONTAINER_NAME_CLI) || true
clean-svc:
	docker rm -f $(CONTAINER_NAME_SVC) || true

# Remove the Docker image
clean-image-cli:
	docker rmi -f $(IMAGE_NAME_CLI) || true
clean-image-svc:
	docker rmi -f $(IMAGE_NAME_SVC) || true

# Full cleanup
clean-all-cli: clean-cli clean-image-cli
clean-all-svc: clean-svc clean-image-svc

.PHONY: all-cli all-svc build-cli build-svc run-cli run-svc clean-cli clean-svc clean-image-cli clean-image-svc clean-all-cli clean-all-svc
