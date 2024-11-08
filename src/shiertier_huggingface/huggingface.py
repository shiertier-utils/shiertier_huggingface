from huggingface_hub import snapshot_download, upload_folder
from os import environ, makedirs
import os.path
from shiertier_tar import pack_directory_to_tarfile, create_index_from_tarfile
from shiertier_logger import logger
from time import sleep

__all__ = ['HuggingfaceUtil', 'ez_hf']

class HuggingfaceUtil:

    author = "shiertier"

    @property
    def help(self):
        help = """
        environment variables:
            HUGGINGFACE_TOKEN: 
                huggingface token, default is None
            HF_HOME: 
                temporary directory for huggingface, default is ~/.cache/huggingface
        
        functions:
            download_model(url_or_repo, local_dir=None, token=None) -> str | None
                url_or_repo: str
                    it can be a huggingface model url or a repo name
                local_dir: str | None
                    local directory, default is None, if None, it will be HF_HOME
                token: str | None
                    huggingface token, default is None
            return: str
                local directory or file path

            upload_dataset(local_dir, repo_name, commit_message=None, token=None)
                local_dir: str
                    local directory, it must be four digits
                repo_name: str
                    repo name to upload, it must be a valid repo name
                commit_message: str | None
                    commit message, default is None, if None, it will be 'Upload {tar_name_without_ext}'
                token: str | None
                    huggingface token, default is None
        """
        for line in help[1:-1].split('\n'):
            print(line.replace('        ', '', 1))

    @property
    def help_zh(self):
        help_zh = """
        环境变量:
            HUGGINGFACE_TOKEN: 
                huggingface token, 默认 None
            HF_HOME: 
                huggingface临时目录, 默认~/.cache/huggingface
        
        函数:
            download_model(url_or_repo, local_dir=None, token=None) -> str | None
                url_or_repo: str
                    huggingface模型url或repo名
                local_dir: str | None
                    本地目录, 默认None, 如果为None, 则使用HF_HOME
                token: str | None
                    huggingface token, 默认None, 如果为None, 则使用环境变量HUGGINGFACE_TOKEN
            return: str
                下载到的本地目录或文件路径

            upload_dataset(local_dir, repo_name, commit_message=None, token=None)
                local_dir: str
                    要上传的本地目录, 必须是四位数字
                repo_name: str
                    上传到的repo仓库
                commit_message: str | None
                    提交信息, 默认None, 如果为None, 则使用'Upload {tar_name_without_ext}'
                token: str | None
                    huggingface token, 默认None, 如果为None, 则使用环境变量HUGGINGFACE_TOKEN
        """
        for line in help_zh[1:-1].split('\n'):
            print(line.replace('        ', '', 1))

    def __init__(
        self, 
        token: str | None = None, 
        hf_home: str | None = None
    ):
        self.token = token or environ.get('HUGGINGFACE_TOKEN')
        default_hf_home = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface')
        self.hf_home = hf_home or default_hf_home

    def convert_huggingface_url_to_repo_name_and_file_path(
        self, 
        url: str
    ) -> tuple[str, str | None]:
        url = url.replace('hf-mirror.com', 'huggingface.co')
        if url.count('/') == 1:
            return url, None
        elif url.startswith('https://huggingface.co') and url.count('/') == 4:
            return url.split('.co/')[1], None
        elif url.startswith('https://huggingface.co') and url.count('/') > 4:
            url = url.replace('?download=true', '')
            url_body = url.split('.co/')[1]
            if '/resolve/main' in url_body:
                repo, file_path = url_body.split('/resolve/main')
            elif '/blob/main' in url_body:
                repo, file_path = url_body.split('/blob/main')
            else:
                raise ValueError("url is not valid")
            return repo, file_path
        else:
            raise ValueError("url is not valid")
    
    def download_model(
        self, 
        url_or_repo: str, 
        local_dir: str | None = None, 
        token: str | None = None
    ) -> str | None:
        if local_dir is None:
            local_dir = self.hf_home

        if token is None:
            token = self.token

        repo_name, file_path = self.convert_huggingface_url_to_repo_name_and_file_path(url_or_repo)

        if repo_name and not file_path:
            local_dir = os.path.join(local_dir, os.path.basename(repo_name))
            return snapshot_download(
                repo_name, 
                local_dir=local_dir, 
                force_download=False, 
                local_dir_use_symlinks=False, 
                token=token
            )

        elif repo_name and file_path:
            local_dir = os.path.join(local_dir, os.path.basename(file_path))
            return snapshot_download(
                repo_name, 
                local_dir=local_dir, 
                filename=file_path, 
                force_download=False, 
                token=token
            )
        else:
            raise ValueError("url_or_repo is not valid")

    def upload_dataset(
        self, 
        local_dir: str, 
        repo_name: str, 
        commit_message: str | None = None, 
        token: str | None = None,
        hf_home: str | None = None
    ) -> None:
        """upload_dataset to huggingface

        Args:
            local_dir: str
                local directory path, must end with four digits
            repo_name: str
                target repo name
            commit_message: str | None
                commit message, default is None, if None, it will be 'Upload {tar_name_without_ext}'
            token: str | None
                huggingface token, default is None, if None, it will be environment variable HUGGINGFACE_TOKEN
            hf_home: str | None
                huggingface cache directory, default is None, if None, it will be ~/.cache/huggingface

        Raises:
            ValueError: when token is not set or local_dir is not valid
        """
        if token is None:
            token = self.token

        if hf_home is None:
            hf_home = self.hf_home

        if token is None:
            raise ValueError("environment variable HUGGINGFACE_TOKEN is not set, and function argument token is not provided")
        
        tar_name_without_ext = os.path.basename(local_dir)
        if not tar_name_without_ext.isdigit() or len(tar_name_without_ext) != 4:
            raise ValueError("local_dir must end with four digits")
        
        archive_file_path = os.path.join(
                                hf_home, 
                                'shiertier_huggingface_client', 
                                "images", 
                                f"{tar_name_without_ext}.tar"
                            )
        makedirs(os.path.dirname(archive_file_path), exist_ok=True)
        pack_directory_to_tarfile(src_directory=local_dir, archive_file=archive_file_path)
        
        index_file_path = os.path.join(
            hf_home, 
            'shiertier_huggingface_client', 
            "index", 
            f"{tar_name_without_ext}.json"
        )

        makedirs(os.path.dirname(index_file_path), exist_ok=True)
        create_index_from_tarfile(
            archive_file_path, 
            index_file_path=index_file_path
        )
        
        def _retry_upload_dataset(
            hf_home: str, 
            repo_name: str, 
            tar_name_without_ext: str, 
            commit_message: str | None = None,
            token: str | None = None,
            max_retries: int = 3,
            retry_delay: int = 300
        ) -> None:
            """retry upload dataset to huggingface

            Args:
                hf_home: str
                    huggingface cache directory
                repo_name: str
                    target repo name
                tar_name_without_ext: str
                    tar file name without extension
                commit_message: str | None
                    commit message, default is None, if None, it will be 'Upload {tar_name_without_ext}'
                max_retries: int
                    max retries, default is 3
                retry_delay: int
                    retry delay, default is 300 seconds
            """
            try:    
                if commit_message is None:
                    commit_message = f"Upload {tar_name_without_ext}"
                upload_folder(
                    folder_path=os.path.join(hf_home, 'shiertier_huggingface_client'),
                    path_in_repo=".",
                    repo_id=repo_name,
                    repo_type='dataset',
                    commit_message=commit_message,
                    token=token
                )
            except Exception as e:
                logger.error(f"upload dataset failed: {e}")
                if max_retries > 0:
                    sleep(retry_delay)
                    self._retry_upload_dataset(
                        hf_home,
                        repo_name,
                        tar_name_without_ext,
                        commit_message,
                        token,
                        max_retries - 1
                    )
                else:
                    raise

        _retry_upload_dataset(
            hf_home, 
            repo_name, 
            tar_name_without_ext, 
            commit_message,
            token
        )
        
        from shutil import rmtree
        rmtree(os.path.join(hf_home, 'shiertier_huggingface_client'))

ez_hf = HuggingfaceUtil()