# shiertier_huggingface

[English](https://github.com/shiertier-utils/shiertier_huggingface/blob/main/README.md) | 中文

## 简介

`shiertier_huggingface` 是一个 Python 库，旨在简化与 Hugging Face Hub 的交互。它提供了一组实用函数，用于下载模型、上传数据集和管理 Hugging Face 仓库。该库特别适用于在 Hugging Face 平台上管理机器学习模型和数据集。

## 安装

您可以通过 `pip` 安装 `shiertier_huggingface`：

```bash
pip install shiertier_huggingface
```

请注意，该项目仍在开发中。

## 环境变量和直接使用 `easy_huggingface_client`

### 环境变量

- `HUGGINGFACE_TOKEN`: 用于与 Hugging Face Hub 进行身份验证的令牌。如果在初始化时未提供，客户端将尝试从该环境变量中检索。

### 直接使用 `easy_huggingface_client`

您可以直接使用 `easy_huggingface_client` 对象，而无需手动初始化 `HuggingfaceClient`。该对象会自动从环境变量中检索令牌。

```python
from shiertier_huggingface import easy_huggingface_client

# 下载模型
easy_huggingface_client.download_model(url_or_repo='https://huggingface.co/bert-base-uncased', repo_type='repo', local_dir='./huggingface_models')

# 上传数据集
easy_huggingface_client.upload_dataset(local_dir='path/to/local_dataset', repo_name='my_dataset_repo', tmp_dir='/root/.tmp')
```

## 使用方法

### 初始化

要使用 `HuggingfaceClient`，您需要使用您的 Hugging Face 令牌进行初始化。如果在初始化时未提供令牌，它将尝试从 `HUGGINGFACE_TOKEN` 环境变量中检索。

```python
from shiertier_huggingface import HuggingfaceClient

# 使用令牌初始化
client = HuggingfaceClient(token='your_huggingface_token')
```

### 下载模型

您可以使用 `download_model` 方法从 Hugging Face Hub 下载模型。该方法允许您指定 URL 或仓库名称、仓库类型和本地目录，模型将保存在该目录中。

```python
# 下载模型
client.download_model(url_or_repo='https://huggingface.co/bert-base-uncased', repo_type='repo', local_dir='./huggingface_models')
```

### 上传数据集

您可以使用 `upload_dataset` 方法将数据集上传到 Hugging Face Hub。该方法允许您指定包含数据集的本地目录、仓库名称和可选的临时目录。

```python
# 上传数据集
client.upload_dataset(local_dir='path/to/local_dataset', repo_name='my_dataset_repo', tmp_dir='/root/.tmp')
```

## 依赖

- `huggingface_hub`
- `shiertier_i18n`
- `shiertier_tar`

## 许可证

本项目基于 MIT 许可证发布。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。