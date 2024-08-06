IMAGE_NAME = llm-chatbot-api-image
IMAGE_NAME_BASE = llm-chatbot-api-image-base
CONTAINER_NAME = llm-chatbot-api
DOCKERFILE = Dockerfile
DOCKERFILE_BASE = Dockerfile.base
NETWORK_NAME = llm-chatbot-network

all: build run

api_port_defined:
ifndef API_PORT 
	$(error Please set API_PORT to the port number for the API)
endif

build-base:
	docker build -t $(IMAGE_NAME_BASE) -f $(DOCKERFILE_BASE) .
build: api_port_defined
	docker build --build-arg API_PORT=$(API_PORT) -t $(IMAGE_NAME) -f $(DOCKERFILE) .

llm_chatbot_base_url_defined:
ifndef LLM_CHATBOT_BASE_URL 
	$(error Please set LLM_CHATBOT_BASE_URL to the base URL of the LLM chatbot)
endif

run: api_port_defined llm_chatbot_base_url_defined
	@docker run --name=$(CONTAINER_NAME) \
		--network $(NETWORK_NAME) \
		-p $(API_PORT):$(API_PORT) \
		-e LLM_CHATBOT_BASE_URL=$(LLM_CHATBOT_BASE_URL) \
		-it --rm -d $(IMAGE_NAME)

clean:
	docker rm -f $(CONTAINER_NAME) || true

clean-image:
	docker rmi -f $(IMAGE_NAME) || true

clean-all: clean clean-image

.PHONY: all build run