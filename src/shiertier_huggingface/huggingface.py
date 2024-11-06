from huggingface_hub import snapshot_download, HfApi, upload_folder
from os import environ, makedirs
import os.path
from shiertier_tar import pack_directory_to_tarfile, create_index_from_tarfile
from shiertier_logger import logger
from time import sleep

__all__ = ['HuggingfaceClient', 'easy_huggingface_client']

class HuggingfaceClient:
    def __init__(self, token: str | None = None):
        if token is None:
            self.token = environ.get('HUGGINGFACE_TOKEN')
        else:
            self.token = token
    
    def login(self):
        # auto login, don't need to call login() before other functions
        if not self.token:
            raise ValueError("huggingface token is not set")
        self.hf_client = HfApi(token=self.token)
    
    def download_model(self, url_or_repo, repo_type='repo', local_dir='./huggingface_models'):
        repo_name,file_path = self.convert_huggingface_url(url_or_repo)

        if repo_type == "repo":
            snapshot_download(repo_name, local_dir=local_dir, force_download=True,local_dir_use_symlinks=False)

        elif repo_type == "file":
            snapshot_download(repo_name, local_dir=local_dir, filename=file_path, force_download=True)
        else:
            raise ValueError("repo_type must be 'repo' or 'file'")

    def convert_huggingface_url(self, url):
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
    
    def upload_dataset(self, local_dir, repo_name, tmp_dir='/root/.tmp'):
        self.login()
        tar_name_without_ext = os.path.basename(local_dir)
        for i in tar_name_without_ext:
            if i not in '0123456789':
                raise ValueError("local_dir must end with four digits")
            
        archive_file_path = os.path.join(tmp_dir, 'huggingface_client', "images", f"{tar_name_without_ext}.tar")
        makedirs(os.path.dirname(archive_file_path), exist_ok=True)
        pack_directory_to_tarfile(src_directory=local_dir,
                                  archive_file=archive_file_path)
        
        index_file_path = os.path.join(tmp_dir, 'huggingface_client', "index", f"{tar_name_without_ext}.json")
        makedirs(os.path.dirname(index_file_path), exist_ok=True)
        create_index_from_tarfile(archive_file_path, 
                                  index_file_path=index_file_path)
                
        def _easy_upload_dataset(self, tmp_dir, repo_name, tar_name_without_ext):
            upload_folder(
                folder_path=os.path.join(tmp_dir, 'huggingface_client'),
                path_in_repo=".",
                repo_id=repo_name,
                repo_type='dataset',
                commit_message=f"Upload {tar_name_without_ext}",
                token=self.token
            )

        try:
            _easy_upload_dataset(tmp_dir, repo_name, tar_name_without_ext)
        except Exception as e:
            logger.error("Upload dataset failed: $$e$$", {"$$e$$": e})
            sleep(300)
            _easy_upload_dataset(tmp_dir, repo_name, tar_name_without_ext)
        
        from shutil import rmtree
        rmtree(os.path.join(tmp_dir, 'huggingface_client'))

easy_huggingface_client = HuggingfaceClient()
