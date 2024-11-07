# shiertier_huggingface

[中文](https://github.com/shiertier-utils/shiertier_huggingface/blob/main/README.md) | English

## 1. Introduction

`shiertier_huggingface` is a Python utility library designed for interacting with the Hugging Face platform. It provides functionalities to download models and upload datasets, simplifying the process of interacting with the Hugging Face platform.

## 2. Installation

### Install via pip

```bash
pip install shiertier_huggingface
```

### Install via git (dev)

```bash
pip install git+https://github.com/shiertier-utils/shiertier_huggingface.git
```

## 3. Environment Variables Setup

Before using `shiertier_huggingface`, you need to set some environment variables.

`HUGGINGFACE_TOKEN` is required if you want to download private models or upload datasets.

`HF_HOME` is optional; if not set, it defaults to `~/.cache/huggingface`.

Here are examples of how to set environment variables in different environments.

### Bash

```bash
export HUGGINGFACE_TOKEN="your_huggingface_token"
export HF_HOME="~/.cache/huggingface"
```

### CMD

```cmd
set HUGGINGFACE_TOKEN=your_huggingface_token
set HF_HOME=C:\Users\YourUsername\.cache\huggingface
```

### PowerShell

```powershell
$env:HUGGINGFACE_TOKEN = "your_huggingface_token"
$env:HF_HOME = "C:\Users\YourUsername\.cache\huggingface"
```

### Python

```python
import os
os.environ['HUGGINGFACE_TOKEN'] = "your_huggingface_token"
os.environ['HF_HOME'] = "~/.cache/huggingface"
```

## 4. Function Usage and Examples

### Quick Start

```python
from shiertier_huggingface import ez_hf
# Alternatively, use the class
# from shiertier_huggingface import HuggingfaceUtil
# hf_util = HuggingfaceUtil(token="your_huggingface_token", hf_home="path/to/hf_home")

# Download model repository
model_repo_dir = ez_hf.download_model("shiertier/model")
# Or use URL
# model_repo_dir = ez_hf.download_model("https://huggingface.co/shiertier/model")

# Download model file, the passed parameter must be a URL
model_file_path = ez_hf.download_model("https://huggingface.co/shiertier/model/resolve/main/model.ckpt")
# If you need to download to a specified location
# model_file_path = ez_hf.download_model("https://huggingface.co/shiertier/model/resolve/main/model.ckpt", local_dir="path/to/local/dir")
# print(model_file_path)
# -> "path/to/local/dir/model.ckpt"

# Upload dataset, the directory must be a four-digit string
# You need to set the environment variable HUGGINFACE_TOKEN before importing shiertier_huggingface
ez_hf.upload_dataset("path/to/local/dir/0000", "shiertier/dataset")
# Or pass the token parameter directly
ez_hf.upload_dataset("path/to/local/dir/0000", "shiertier/dataset", token="your_huggingface_token")
```

### Detailed Function Introduction

#### `download_model(url_or_repo, local_dir=None, token=None)`

- `url_or_repo`: Hugging Face model URL or repository name.
- `local_dir`: Local directory, defaults to `None`. If `None`, it uses `HF_HOME`.
- `token`: Hugging Face token, defaults to `None`. If `None`, it uses the environment variable `HUGGINGFACE_TOKEN`.

#### `upload_dataset(local_dir, repo_name, commit_message=None, token=None, hf_home=None)`

- `local_dir`: Local directory to upload, must be a four-digit string.
- `repo_name`: Repository name to upload to.
- `commit_message`: Commit message, defaults to `None`. If `None`, it uses `'Upload {tar_name_without_ext}'`.
- `token`: Hugging Face token, defaults to `None`. If `None`, it uses the environment variable `HUGGINGFACE_TOKEN`.
- `hf_home`: Hugging Face temporary directory, defaults to `None`. If `None`, it uses the environment variable `HF_HOME`.

### Help

You can get help information by:

```python
from shiertier_huggingface import ez_hf

ez_hf.help  # Get English help
ez_hf.help_zh  # Get Chinese help
```

## 5. Dependencies

- `huggingface_hub`
- `shiertier_tar`
- `shiertier_logger`

## 6. License

This project is licensed under the [MIT License](https://github.com/shiertier-utils/shiertier_huggingface/blob/main/LICENSE).