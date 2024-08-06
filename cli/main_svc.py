import json
import os
import subprocess
import time
from pathlib import Path
from flask import Flask, jsonify, request


app = Flask(__name__)


def _read_configuration(conversation_id):
    config = {}
    config_path = Path(f'context/config_{conversation_id}.json')
    if config_path.exists():
        config = json.loads(config_path.read_text())
    return config


def _write_configuration(conversation_id, config):
    config_path = Path(f'context/config_{conversation_id}.json')
    config_path.write_text(json.dumps(config))


@app.route("/configuration", methods=["GET", "POST"])
def configuration():
    conversation_id = request.headers.get("conversation_id")

    config = _read_configuration(conversation_id)

    if request.method == "GET":
        return json.dumps(config)

    # Make sure the POST body contains JSON
    if not request.is_json:
        return "Request must be JSON", 400

    # Get JSON from request body
    config.update(request.get_json())

    # Write configuration
    _write_configuration(conversation_id, config)
    return ""


@app.route("/models")
def models():
    models = []
    for model in Path('llms').iterdir():
        models.append(model.name)

    return jsonify(models)


@app.route("/init-conversation", methods=["POST"])
def init_conversation():
    conversation_id = str(int(time.time() * 10_000_000_000))
    with open("context/conversation_id.txt", "w") as f:
        f.write(conversation_id)
    return conversation_id


answer_begin_marker = "[Answer]:"
answer_end_marker = "</s>"


@app.route("/conversation", methods=["POST"])
def post_conversation():
    conversation_id = request.headers.get("conversation_id")

    # Make sure the POST body contains JSON
    if not request.is_json:
        return "Request must be JSON", 400

    # Get JSON from request body
    prompt = request.get_json().get("prompt")

    config = _read_configuration(conversation_id)

    sys_message = config.get("sys", "")

    conversation = ""
    conversation_path = Path(f'context/conversation_{conversation_id}.txt')
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
    idx = output.index(answer_begin_marker)
    if idx == -1:
        return output, 400

    begin_idx = idx + len(answer_begin_marker)
    end_idx = output.index(answer_end_marker, begin_idx)
    if end_idx == -1:
        end_idx = len(output)

    config["sys"] = ""
    _write_configuration(conversation_id, config)

    output = output[begin_idx:end_idx].strip()
    conversation += f" {output} </s>"
    conversation_path.write_text(conversation)
    return output


@app.route("/conversation", methods=["GET"])
def get_conversation():
    conversation_id = request.headers.get("conversation_id")

    conversation = ""
    conversation_path = Path(f'context/conversation_{conversation_id}.txt')
    if conversation_path.exists():
        conversation = conversation_path.read_text()

    turns = []
    # Each turn is separated by "</s>"
    raw_turns = [turn.strip('<s>').strip() for turn in 
                    [turn.strip() for turn in conversation.split("</s>")] 
                if turn]
    for turn in raw_turns:
        # Each turn has `[INUST] prompt [/INST] answer` structure
        prompt, answer = (x.strip() for x in turn.split("[/INST]", 1))

        # Each prompt can have `<<SYS>> system message <</SYS>> prompt` structure
        sys_prompt_pair = prompt.split("<</SYS>>", 1)
        if len(sys_prompt_pair) == 2:
            sys_message, prompt = (x.strip() for x in sys_prompt_pair)
            sys_message = sys_message.lstrip("[INST]").lstrip().lstrip("<<SYS>>").lstrip()
        else:
            sys_message = ""
            prompt = sys_prompt_pair[0].strip().lstrip("[INST]").lstrip()

        turns.append({
            "sys": sys_message,
            "prompt": prompt,
            "answer": answer
        })

    return jsonify(turns)


def _is_number(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


@app.route("/conversations", methods=["GET"])
def get_conversations():
    # Get all files in the `context` directory whose names has format `conversation_*.txt`
    conversation_files = [file for file in Path('context').iterdir() if file.name.startswith("conversation_")]
    # Get the file name part after `conversation_` and before `.txt`
    conversation_ids = [x for x in [file.name[13:-4] for file in conversation_files] if _is_number(x)]
    # Order the conversation_ids in descending order
    conversation_ids.sort(reverse=True)

    return jsonify(conversation_ids)


if __name__ == "__main__":
    app.run(port=int(os.environ.get("SVC_PORT")))