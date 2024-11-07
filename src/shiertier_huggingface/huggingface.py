from huggingface_hub import snapshot_download, HfApi, upload_folder
from os import environ, makedirs
import os.path
from shiertier_tar import pack_directory_to_tarfile, create_index_from_tarfile
from shiertier_logger import logger
from time import sleep

__all__ = ['HuggingfaceUtil', 'easy_huggingface']

class HuggingfaceUtil:

    creator = "shiertier"

    @property
    def help(self) -> str:
        help = """
        environment variables:
            HUGGINGFACE_TOKEN: 
                huggingface token, default is None
            HUGGINGFACE_TMPDIR: 
                temporary directory for huggingface, default is ~/.cache/huggingface
        
        functions:
            download_model(url_or_repo, repo_type='repo', local_dir=None, token=None)
                url_or_repo: str
                    it can be a huggingface model url or a repo name
                repo_type: str
                    it can be 'repo' or 'file', default is 'repo'
                local_dir: str | None
                    local directory, default is None, if None, it will be HUGGINGFACE_TMPDIR
                token: str | None
                    huggingface token, default is None

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
        print(help)

    def __init__(self, 
                 token: str | None = None, 
                 tmp_dir: str | None = None):
        if token is None:
            token = environ.get('HUGGINGFACE_TOKEN')
        if tmp_dir is None:
            tmp_dir = environ.get('HUGGINGFACE_TMPDIR', os.path.join(os.path.expanduser('~'), '.cache', 'huggingface'))
        self.token = token
        self.tmp_dir = tmp_dir

    def convert_huggingface_url_to_repo_name_and_file_path(self, 
                                                           url: str) -> tuple[str, str | None]:
        url.replace('hf-mirror.com', 'huggingface.co')
        if url.count('/') == 1:
            return url, None
        elif url.startswith('https://huggingface.co') and url.count('/') == 4:
            return url.splite('.co/')[1] , None
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
    
    def download_model(self, 
                       url_or_repo: str, 
                       repo_type: str = 'repo', 
                       local_dir: str | None = None, 
                       token: str | None = None):
        if local_dir is None:
            local_dir = self.tmp_dir
        if token is None:
            token = self.token
        if repo_type not in ['repo', 'file']:
            raise ValueError("repo_type must be 'repo' or 'file'")
        repo_name,file_path = self.convert_huggingface_url_to_repo_name_and_file_path(url_or_repo)
        local_dir = os.path.join(local_dir, os.path.basename(repo_name))
        if repo_type == 'repo':
            snapshot_download(repo_name, local_dir=local_dir, force_download=True,local_dir_use_symlinks=False, token=token)
        elif repo_type == 'file':
            snapshot_download(repo_name, local_dir=local_dir, filename=file_path, force_download=True, token=token)

    def upload_dataset(self, 
                        local_dir: str, 
                        repo_name: str, 
                        commit_message: str | None = None, 
                        token: str | None = None):
        if token is None:
            token = self.token

        if tmp_dir is None:
            tmp_dir = self.tmp_dir

        if token is None:
            raise ValueError("environment variable HUGGINGFACE_TOKEN is not set, and function argument token is not provided")
        
        tar_name_without_ext = os.path.basename(local_dir)
        for i in tar_name_without_ext:
            if i not in '0123456789':
                raise ValueError("local_dir must end with four digits")
        if len(tar_name_without_ext) != 4:
            raise ValueError("local_dir must end with four digits")
        
        archive_file_path = os.path.join(tmp_dir, 'shiertier_huggingface_client', "images", f"{tar_name_without_ext}.tar")
        makedirs(os.path.dirname(archive_file_path), exist_ok=True)
        pack_directory_to_tarfile(src_directory=local_dir,
                                archive_file=archive_file_path)
        
        index_file_path = os.path.join(tmp_dir, 'shiertier_huggingface_client', "index", f"{tar_name_without_ext}.json")
        makedirs(os.path.dirname(index_file_path), exist_ok=True)
        create_index_from_tarfile(archive_file_path, 
                                index_file_path=index_file_path)
        
        def easy_upload_dataset(tmp_dir, repo_name, tar_name_without_ext, commit_message=None):
            try:    
                if commit_message is None:
                    commit_message = f"Upload {tar_name_without_ext}"
                upload_folder(
                    folder_path=os.path.join(tmp_dir, 'shiertier_huggingface_client'),
                    path_in_repo=".",
                    repo_id=repo_name,
                    repo_type='dataset',
                    commit_message=commit_message,
                    token=token
                )
            except Exception as e:
                logger.error(f"Upload dataset failed: {e}")
                sleep(300)
                easy_upload_dataset(tmp_dir, repo_name, tar_name_without_ext, commit_message)

        easy_upload_dataset(tmp_dir, repo_name, tar_name_without_ext, commit_message)
        
        from shutil import rmtree
        rmtree(os.path.join(tmp_dir, 'shiertier_huggingface_client'))

easy_hf = HuggingfaceUtil()