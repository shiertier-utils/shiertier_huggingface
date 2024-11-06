# shiertier_huggingface

English | [中文](https://github.com/shiertier-utils/shiertier_huggingface/blob/main/README_zh.md)

## Introduction

`shiertier_huggingface` is a Python library designed to simplify interactions with the Hugging Face Hub. It provides a set of utility functions to download models, upload datasets, and manage Hugging Face repositories. This library is particularly useful for managing machine learning models and datasets on the Hugging Face platform.

## Installation

You can install `shiertier_huggingface` via `pip`:

```bash
pip install shiertier_huggingface
```

Please note that this project is still under development.

## Environment Variables and Direct Usage of `easy_huggingface_client`

### Environment Variables

- `HUGGINGFACE_TOKEN`: The token used for authentication with the Hugging Face Hub. If not provided during initialization, the client will attempt to retrieve it from this environment variable.

### Direct Usage of `easy_huggingface_client`

You can directly use the `easy_huggingface_client` object without manually initializing the `HuggingfaceClient`. This object will automatically retrieve the token from the environment variable.

```python
from shiertier_huggingface import easy_huggingface_client

# Download a model
easy_huggingface_client.download_model(url_or_repo='https://huggingface.co/bert-base-uncased', repo_type='repo', local_dir='./huggingface_models')

# Upload a dataset
easy_huggingface_client.upload_dataset(local_dir='path/to/local_dataset', repo_name='my_dataset_repo', tmp_dir='/root/.tmp')
```

## Usage

### Initialization

To use the `HuggingfaceClient`, you need to initialize it with your Hugging Face token. If the token is not provided during initialization, it will attempt to retrieve it from the `HUGGINGFACE_TOKEN` environment variable.

```python
from shiertier_huggingface import HuggingfaceClient

# Initialize with a token
client = HuggingfaceClient(token='your_huggingface_token')
```

### Downloading a Model

You can download a model from the Hugging Face Hub using the `download_model` method. This method allows you to specify the URL or repository name, the repository type, and the local directory where the model will be saved.

```python
# Download a model
client.download_model(url_or_repo='https://huggingface.co/bert-base-uncased', repo_type='repo', local_dir='./huggingface_models')
```

### Uploading a Dataset

You can upload a dataset to the Hugging Face Hub using the `upload_dataset` method. This method allows you to specify the local directory containing the dataset, the repository name, and an optional temporary directory.

```python
# Upload a dataset
client.upload_dataset(local_dir='path/to/local_dataset', repo_name='my_dataset_repo', tmp_dir='/root/.tmp')
```

## Dependencies

- `huggingface_hub`
- `shiertier_i18n`
- `shiertier_tar`

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.