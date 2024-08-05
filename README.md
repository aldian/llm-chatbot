# llm-chatbot

As I am using the [GitHub Free](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage) plan, the largest file I store can only have size 2GB.
When I tried to store a 4 GB LLM model in this repo, I got this error:
```
Size must be less than or equal to 2147483648: [422] Size must be less than or equal to 2147483648
```
Please provide the LLM model yourself, or you can download it [here](https://drive.google.com/drive/folders/1cvIeDSwH1IzN7ouvwmb1vgg6UTcJIBdq?usp=drive_link).
After checking out this repo, create a folder named `llms`, and copy/move the LLM models to it.
After downloading the models, the `llms` folder should like like this:
```
llms/
├── Llama-2-7B-chat-q5_k_m.gguf
└── Mistral-Instruct-7.2B-q5_k_m.gguf
```