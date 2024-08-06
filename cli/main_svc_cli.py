import argparse
import asyncio
import os
import sys
import uuid
from pathlib import Path

import requests


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--svc-port", help="Server port number", type=int)
    parser.add_argument("--init-conversation", help="Initialize conversation from a clean", action="store_true")
    parser.add_argument("--model", help="Choose model", type=int, default=0)
    parser.add_argument("--sys", help="System message", type=str)
    parser.add_argument("--prompt", help="Prompt", type=str)
    args = parser.parse_args()
    
    if args.init_conversation:
        response = requests.post(f"http://localhost:{args.svc_port}/init-conversation")
        response.raise_for_status()
        conversation_id = response.content.decode()
        print(conversation_id)
        return

    conversation_id = ""
    conversation_id_path = Path(f'context/conversation_id.txt')
    if conversation_id_path.exists():
        conversation_id = conversation_id_path.read_text()

    if not conversation_id:
        print("Please initialize conversation.", file=sys.stderr)
        parser.print_help()
        return

    response = requests.get(f"http://localhost:{args.svc_port}/models")
    response.raise_for_status()
    models = response.json()

    response = requests.get(f"http://localhost:{args.svc_port}/configuration", headers={"conversation_id": conversation_id})
    response.raise_for_status()
    configuration = response.json()
    if not (args.model or configuration.get("model")):
        print("Model selection is not configured. Please specify a model using MODEL. Choose one of the following numbers:", file=sys.stderr)
        print("\n".join(f"({i + 1}) {model}" for i, model in enumerate(models)), file=sys.stderr)
        return

    if args.model or args.sys:
        if args.model > len(models):
            print("Invalid model selection.", file=sys.stderr)
            return
        if args.model > 0:
            configuration["model"] = models[args.model - 1]
        if args.sys:
            configuration["sys"] = args.sys
        response = requests.post(
            f"http://localhost:{args.svc_port}/configuration", 
            headers={"conversation_id": conversation_id}, json=configuration
        )
        response.raise_for_status()

    if args.prompt:
        response = requests.post(
            f"http://localhost:{args.svc_port}/conversation", 
            headers={"conversation_id": conversation_id}, json={"prompt": args.prompt}
        )
        response.raise_for_status
        print(response.content.decode())


if __name__ == "__main__":
    asyncio.run(main())