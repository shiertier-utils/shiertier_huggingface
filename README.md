# shiertier_huggingface

中文 | [English](https://github.com/shiertier-utils/shiertier_huggingface/blob/main/README_en.md)

## 1. 简介

`shiertier_huggingface` 是一个用于与 Hugging Face 平台进行交互的 Python 工具库。它提供了下载模型和上传数据集的功能，简化了与 Hugging Face 平台的交互过程。

## 2. 安装

### 通过 pip 安装

```bash
pip install shiertier_huggingface
```

### 通过 git 安装（开发版）

```bash
pip install git+https://github.com/shiertier-utils/shiertier_huggingface.git
```

## 3. 环境变量设置

在使用 `shiertier_huggingface` 之前，您需要设置一些环境变量。
`HUGGINGFACE_TOKEN` 如果为 `None`，则仅可下载公开模型。
`HF_HOME` 如果为 `None`，则默认是 `~/.cache/huggingface`。
以下是如何在不同环境中设置环境变量的示例。

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

## 4. 函数用法与示例

### 快速使用

```python
from shiertier_huggingface import ez_hf
# 或者使用类
# from shiertier_huggingface import HuggingfaceUtil
# hf_util = HuggingfaceUtil(token="your_huggingface_token", hf_home="path/to/hf_home")

# 下载模型仓库
model_repo_dir = ez_hf.download_model("shiertier/model")
# 或者使用url
# model_repo_dir = ez_hf.download_model("https://huggingface.co/shiertier/model")

# 下载模型文件, 传递的必须为url
model_file_path = ez_hf.download_model("https://huggingface.co/shiertier/model/resolve/main/file")
# 如果需要下载到指定位置
# model_file_path = ez_hf.download_model("https://huggingface.co/shiertier/model/resolve/main/model.ckpt", local_dir="path/to/local/dir")
# print(model_file_path)
# -> "path/to/local/dir/model.ckpt"

# 上传数据集，需要为四位数字字符串的目录
# 需要导入shiertier_huggingface之前设置环境变量HUGGINFACE_TOKEN
ez_hf.upload_dataset("path/to/local/dir/0000", "shiertier/dataset")
# 或者直接传递token参数
ez_hf.upload_dataset("path/to/local/dir/0000", "shiertier/dataset", token="your_huggingface_token")
```

### 详细函数介绍

#### `download_model(url_or_repo, local_dir=None, token=None)`

- `url_or_repo`: Hugging Face 模型 URL 或仓库名称。
- `local_dir`: 本地目录，默认为 `None`，如果为 `None`，则使用 `HF_HOME`。
- `token`: Hugging Face 令牌，默认为 `None`，如果为 `None`，则使用环境变量 `HUGGINGFACE_TOKEN`。

#### `upload_dataset(local_dir, repo_name, commit_message=None, token=None)`

- `local_dir`: 要上传的本地目录，必须是四位数字。
- `repo_name`: 上传到的仓库名称。
- `commit_message`: 提交信息，默认为 `None`，如果为 `None`，则使用 `'Upload {tar_name_without_ext}'`。
- `token`: Hugging Face 令牌，默认为 `None`，如果为 `None`，则使用环境变量 `HUGGINGFACE_TOKEN`。

### 帮助

您可以通过以下方式获取帮助信息：

```python
from shiertier_huggingface import ez_hf

ez_hf.help()  # 获取英文帮助
ez_hf.help_zh()  # 获取中文帮助
```

## 5. 依赖

- `huggingface_hub`
- `shiertier_tar`
- `shiertier_logger`

## 6. 许可证

本项目采用 [MIT 许可证](https://github.com/shiertier-utils/shiertier_huggingface/blob/main/LICENSE)。