# llm-chatbot

An LLM chat bot that is installed on local machine and accessed via command line.

## Set up the LLM models

As I am using the [GitHub Free](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage) plan, the largest file I store can only have size 2GB.
When I tried to store a 4 GB LLM model in this repo, I got this error:
```
[422] Size must be less than or equal to 2147483648
```
Therefore, please provide the quantized LLM models yourself, or you can download them [here](https://drive.google.com/drive/folders/1cvIeDSwH1IzN7ouvwmb1vgg6UTcJIBdq?usp=drive_link). That Google Drive folder contains Llama 2 and Mistral models.
After checking out this repo, create a folder named `llms`, and copy the LLM models to it.
After downloading the models from the Google Drive folder, the `llms` folder should look like this:
```
llms/
├── Llama-2-7B-chat-q5_k_m.gguf
└── Mistral-Instruct-7.2B-q5_k_m.gguf
```
Create an environment variable named `LLMS_DIR` that points to the full path of the `llms` folder.

## Set up the conversation context folder

Create a folder named `context` and create an environment variable named `CONTEXT_DIR` that points to the full path of
the `context` folder.

## Running the script

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
### Using Flask server

Use this mode if you need the chatbot to be used by a frontend app.

#### Build the docker container
```
make build-svc-base
make build-svc
```
#### Start the Flask server
```
make start-svc
```
```
make svc-init-conversation
```