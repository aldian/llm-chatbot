import argparse
import asyncio
import json
import re
import subprocess
from pathlib import Path


answer_re = re.compile(r"\[Answer\]:\s*(.*)\s*</s>\s*$", re.IGNORECASE)


async def main():
    config = {}
    config_path = Path('context/config.json')
    if config_path.exists():
        config = json.loads(config_path.read_text())

    models = []
    for model in Path('llms').iterdir():
        models.append(model.name)

    models_menu = '\n'.join(f"({i + 1}) {model}" for i, model in enumerate(models))

    config_path = Path('context/config.json')
    if config_path.exists():
        config = json.loads(config_path.read_text())

    parser = argparse.ArgumentParser()
    parser.add_argument("--sys", help="Set system message", type=str)
    parser.add_argument("--model", help=f"Choose the model:\n{models_menu}", type=int,  default=0)
    parser.add_argument("--prompt", help="Set the prompt", type=str)
    args = parser.parse_args()
    if args.sys:
        config["sys"] = args.sys
    if args.model:
        config["model"] = models[args.model - 1]

    config_path.write_text(json.dumps(config))
    if not args.prompt:
        parser.print_help()
        return
    elif args.model == 0 and not config.get("model"):
        print(f"Please choose a model:\n{models_menu}")
        return

    prompt = args.prompt 
    sys_message = config.get("sys", "")
    config["sys"] = ""
    config_path.write_text(json.dumps(config))

    conversation = ""
    conversation_path = Path('context/conversation.txt')
    if conversation_path.exists():
        conversation = conversation_path.read_text()

    conversation += "<s>[INST] "
    if sys_message:
        conversation += f"<<SYS>>{sys_message}<</SYS>> "

    conversation += f"{prompt} [/INST]"

    result = subprocess.run([
        "wasmedge",
        "--dir", ".:.",
        "--nn-preload", f"default:GGML:AUTO:llms/{config['model']}",
        "llama-simple.wasm",
        "--n-predict", "1024",
        "--prompt", conversation
    ], capture_output=True, text=True)

    output = result.stdout.strip()
    match = answer_re.search(output)
    if match:
        conversation += f" {match.group(1)} </s>"
        conversation_path.write_text(conversation)
        print(match.group(1))


if __name__ == "__main__":
    asyncio.run(main())