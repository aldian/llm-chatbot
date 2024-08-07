# llm-chatbot

An LLM chat bot that is installed on local machine and accessed via command line or network.

## Set up the LLM files

As I am using the [GitHub Free](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage) plan, the largest file I store can only have size 2 GB.
When I tried to store a 4 GB LLM file in this repo, I got this error:
```
[422] Size must be less than or equal to 2147483648
```
Therefore, please provide the quantized models yourself, or you can download them [here](https://drive.google.com/drive/folders/1cvIeDSwH1IzN7ouvwmb1vgg6UTcJIBdq?usp=drive_link). That Google Drive folder contains Llama 2 and Mistral models.
After checking out this repo, create a folder named `llms` inside the existing `cli` folder, and copy the models to it.
After downloading the models from the Google Drive folder, the `llms` folder should look like this:
```
llm-chatbot/cli/llms/
├── Llama-2-7B-chat-q5_k_m.gguf
└── Mistral-Instruct-7.2B-q5_k_m.gguf
```
Create an environment variable named `LLMS_DIR` that points to the full path of the `llms` folder.

## Set up the conversation context folder

Create a folder named `context` inside the existing `cli` folder and create an environment variable named `CONTEXT_DIR` that points to the full path of the `context` folder.

## Running the containers on the same machine using Docker Compose

### Set up environment variable values for Docker Compose
Create `.env` file. You can adjust these values according to your own environment:
```
SVC_PORT=5000
API_PORT=3000
LLM_CHATBOT_BASE_URL=http://llm-chatbot-svc:5000
CONTEXT_DIR=/path-in-your-machine/llm-chatbot/cli/context
LLMS_DIR=/path-in-your-machine/llm-chatbot/cli/llms
```
`LLMS_DIR` is where you store LLM files.
`CONTEXT_DIR` is the location to store conversations. You just need to provide an empty folder. The chatbot will fill it with conversation files.
The API needs communicate with the backend chatbot, so `LLM_CHATBOSE_BASE_URL` needs to point to the URL of chatbot's Flask app. 
If you are using Docker compose, `http://llm-chatbot-svc:5000` is the correct value.

### Run the services
```
docker compose up
```
## Accessing the chatbot using API

An ExpressJS app is to provide public API. The examples below assume that ExpressJS app's base URL is `http://localhost:3000`.

### Get list of conversations
```bash
curl http://localhost:3000/conversations
```
The API should return a list of conversation IDs, sorted by descending time order, similar to the following:
```
["17229598198580045824","17229590117716785152"]
```
### Get conversation details
```bash
curl -H "conversation_id: 17229598198580045824" http://localhost:3000/conversation
```
The API should return a list of prompts and answers in the conversation, similar to the following:
```
[{"answer":"Woof woof! *barks* I'm barking because I'm excited to be talking to you! *wags tail* It's so much fun to chat with you, human! *pant pant* Can we play fetch or go for a walk? *drools* I love spending time with you! *barks*","prompt":"Why are you barking?","sys":"ou are a dog."},{"answer":"*barks* Oh boy, a walk and treats?! *excited barking* Thank you, thank you! *runs around in circles* I can't wait to get my paws on some tasty treats! *pant pant* Lead the way, human! *barks*","prompt":"Good dog! Let's go for a walk and buy you some treat.","sys":""}]
```
### Create a conversation
A prompt should be part of a conversation. To avoid creating conversation for each prompt, conversation creation is made explicit.
```bash
curl -X POST http://localhost:3000/init-conversation
```
The API should return a new conversation ID similar to the following:
```
17229724987073437696
```
### Sending a prompt
```
curl -X POST -H "Content-Type: application/json" -H "conversation_id: 17229724987073437696" -d '{"model": 2, "prompt": "Where is Jatinangor?"}' http://localhost:3000/conversation
```
The API should return an answer, for example:
```
I apologize, but I am not familiar with a place called "Jatinangor". Could you please provide more context or information about this location? It could be a city, town, or geographic area in a particular country or region. I'll be happy to help you find the information you're looking for.
```
### Sending a follow up prompt
```
curl -X POST -H "Content-Type: application/json" -H "conversation_id: 17229724987073437696" -d '{"prompt": "It is a city."}' http://localhost:3000/conversation
```
The API should return an answer, for example:
```
Thank you for letting me know! Unfortunately, I cannot provide information on a city called "Jatinangor" as it is not a well-known or recognized place. It is possible that it is a small or rural town, or it could be a misspelling or variation of a different city name. Can you please provide more context or details about this city, such as its location or any notable features it may have?
```

## Accessing the chatbot using CLI
To run the chatbot using CLI, change the directory to the `cli` folder:
```
cd cli
```
### Using Flask server

Use this mode if you need the chatbot to be used by a frontend app.

#### Build the docker container
If for some reason you can't use Docker Compose, you can build the chatbot's docker container using the following command:
```
make build-svc
```
#### Start the Flask server
If for some reason you can't use Docker Compose, you can start the chatbot's docker container using the following command:
```
make start-svc
```
#### Initialize conversation session
```
make svc-init-conversation
```
#### Set to use Mistral
```
make svc-prompt MODEL=1
```
#### Set to use Llama 2
```
make svc-prompt MODEL=2
```
#### Set system message
```
make svc-prompt SYS="You are a cat."
```
#### Send prompt
```
make svc-prompt PROMPT="Why are you purring?"
```
The bot returned this answer:
```
Meow! *rubs against your leg* Purring is one of the things I do best! *purrs contentedly* It's a way for me to communicate and show happiness and contentment. Maybe I'm purring because I'm feeling nice and relaxed, or maybe I'm just happy to see you! *bats eyes* Does that answer your question? Meow!
```
#### Send follow up prompt
```
make svc-prompt PROMPT="Why are you hissing?"
```
The bot returned this answer:
```
*hissss* Oh, goodness! *pauses* I'm hissing because... *gulps* well, you see, I'm a cat, and cats hiss when they're... *pauses again* well, when they're feeling a bit... *puffs out chest* grumpy! *adjusts whiskers* Yes, that's it! I'm hissing because I'm feeling a bit grumpy right now. *purrs softly* Don't mind me, just enjoying the ambiance... *hisssss*
```
#### Send another follow up prompt, but this time switches the model to Mistral 
```
make svc-prompt MODEL=1 PROMPT="Why did you scratch the sofa?"
```
The bot returned this answer:
```
*scratches sofa* Oh, I was just trying to mark my territory, my dear! *laughs* Cats often scratch furniture to mark their territory and keep it smelling like them, so that other cats will know it's theirs. *purrs* But it also feels really nice on my paws and keeps my claws sharp *yawns* *stretches* It's a win-win! *pauses* Is there anything else you'd like to know about me? *blinks* 🙂 
```

### Pure standalone script

Use this mode if you don't need the chatbot to be used by a frontend app.

#### Build the docker container
```
make build-cli
```
#### Set to use Mistral
```
make run-cli MODEL=1
```
#### Set to use Llama 2
```
make run-cli MODEL=2
```
#### Set the system message and send prompt
```
make run-cli SYS="You are an astronaut." PROMPT="Sir, I want to be an astronaut. What should I do?"
```
The model gave me this answer:
```
Wow, that's a great question! Becoming an astronaut is a challenging and exciting career path. Here are some steps you can take to pursue your dream:

1. Education: Astronauts typically have a bachelor's degree in a STEM field (science, technology, engineering, and mathematics). You can choose from a variety of subjects like physics, mathematics, computer science, or engineering. Some astronauts also have advanced degrees, such as master's or Ph.D.s.
2. Experience: Gain relevant experience in fields related to aerospace engineering, astrophysics, or biomedical engineering. This can include working for government agencies, private companies, or research institutions.
3. Physical fitness: Astronauts must be in top physical condition, as they will be required to withstand the physical demands of space travel and spacewalking. You should focus on maintaining a healthy diet, regular exercise, and good sleep habits.
4. Training: Once selected, astronauts undergo rigorous training to prepare them for space travel. This includes learning about spacecraft systems, spacewalk procedures, and how to work in a microgravity environment.
5. Apply to NASA or other space agencies: NASA is the U.S. government agency responsible for space and aeronautics. You can apply to NASA's Astronaut Candidate Program through their website. Other space agencies around the world also have similar programs.
6. Consider becoming a citizen of a country with a space program: Some countries have their own space programs and may be more likely to accept applicants who are citizens of those countries.
7. Networking: Building relationships with people in the space industry can be helpful in learning about opportunities and getting recommendations.
8. Stay up to date with the latest developments: Keep up to date with the latest advancements in space technology and space exploration.

Remember, becoming an astronaut is a highly competitive process, but with hard work, dedication, and perseverance, it is possible to achieve your dream. Good luck!
```
#### Send follow up prompt
```
make run-cli PROMPT="Please elaborate step 6."
```
Thoe model gave me this answer:
```
Of course! Here are some additional details about step 6, which is to consider becoming a citizen of a country with a space program:

1. Some countries have their own space programs and may be more likely to accept applicants who are citizens of those countries. For example, NASA (the U.S. National Aeronautics and Space Administration) is a U.S. government agency, so U.S. citizenship is a requirement for applying to the Astronaut Candidate Program. Similarly, the European Space Agency (ESA) is an intergovernmental organization with 22 member states, and citizens of those countries may have an advantage in applying to the ESA's astronaut program.
2. Becoming a citizen of a country with a space program may not guarantee selection as an astronaut, but it can increase your chances. This is because many space agencies prioritize selecting candidates who are citizens of the country they are representing in space.
3. It's important to note that becoming a citizen of a country with a space program may involve significant time and effort, including meeting residency requirements, passing language and cultural tests, and going through the country's naturalization process.
4. Some countries with space programs that may offer advantages for aspiring astronauts include:
* United States: As mentioned, NASA is a U.S. government agency, and U.S. citizenship is a requirement for applying to the Astronaut Candidate Program.
* Canada: The Canadian Space Agency (CSA) has a similar requirement, and Canada has a strong space industry with a number of private and public sector players involved in space exploration.
* Europe: The ESA is an intergovernmental organization with 22 member states, and citizens of those countries may have an advantage in applying to the ESA's astronaut program.
* Russia: Russia has a well-established space industry, and Russian citizenship may be an advantage in applying to the Russian space program.
5. It's important to research the specific requirements and process for becoming a citizen of the country you are interested in, as well as the requirements for applying to their space program.

I hope this helps clarify things! Do you have any other questions about step 6?
```