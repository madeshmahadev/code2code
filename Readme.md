# Code2Code

Code2Code is a simple code converter command line interface (CLI) that leverages state-of-the-art small language models (SLMs) to convert code from one programming language to another. Currently, it uses the Ollama library for code conversion but will be extended to support other libraries in the future. Redis is used to cache the code temporarily to improve performance.


## Features

- Convert code between different programming languages
- Caches code using Redis for improved performance
- Supports multiple programming languages

## Installation

### Prerequisites

- Python 3.9 or higher
- Redis
- Ollama

### Install Redis

To install Redis, follow the instructions for your operating system:

#### On macOS

```sh
brew install redis
brew services start redis
```

#### On Ubuntu

```sh
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server.service
sudo systemctl start redis-server.service
```

### Install Ollama

Ollama is a free, open-source tool that allows users to run large language models (LLMs) locally on their systems. [Click here](https://ollama.com/) to view the official documentation.

#### macOS

[Download](https://ollama.com/download/Ollama-darwin.zip)

#### Windows

[Download](https://ollama.com/download/OllamaSetup.exe)

#### Linux

```
curl -fsSL https://ollama.com/install.sh | sh
```

[Manual install instructions](https://github.com/ollama/ollama/blob/main/docs/linux.md)

#### Docker

The official [Ollama Docker image](https://hub.docker.com/r/ollama/ollama) `ollama/ollama` is available on Docker Hub.

#### Libraries

- [ollama-python](https://github.com/ollama/ollama-python)
- [ollama-js](https://github.com/ollama/ollama-js)

#### Pull the model

To run and chat with [Mistral-Nemo](https://ollama.com/library/mistral-nemo:12b), a state-of-the-art 12B model with 128k context length, built by Mistral AI in collaboration with NVIDIA.:

```
ollama run mistral-nemo:12b
```

### Install Code2Code

Clone the repository and install the required dependencies:

```sh
git clone https://github.com/madeshmahadev/code2code.git
cd code2code
```

Create a virtual environment and activate it:

```sh
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```sh
pip install -r requirements.txt
```

## Usage

To see the available options, run the following command:

```sh
python main.py --help
```

To convert code from one programming language to another, run the following command:

```sh
python main.py  <source_dir> <target_dir> <source_language> <target_language>
```
Replace the placeholders with the appropriate values:

- `<source_dir>`: The directory containing the source code
- `<target_dir>`: The directory where the converted code will be saved
- `<source_language>`: The source programming language (e.g., `js`, `py`, `java`)
- `<target_language>`: The target programming language (e.g., `js`, `py`, `java`)

for example, to convert Python code to JavaScript:

```sh
python main.py examples/js_to_py/input examples/js_to_py/output js py
```

License
This project is licensed under the MIT License. See the LICENSE file for details.