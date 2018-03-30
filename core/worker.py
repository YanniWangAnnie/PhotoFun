import os
import threading
import shutil
import workerthread
from azure.storage.blob import BlockBlobService, ContentSettings
from logger import log, LogLevel

class Worker(threading.Thread):
    def __init__(self,x):
        self.worker_id = x
        threading.Thread.__init__(self)

        self.block_blob_service = BlockBlobService(
            account_name='photofunstorage', account_key='Br6qGU0woc+qOQtsneQ6XkgQx6gsmcvmbg9Eyh6+gpISHwmu48o+rmBzIQvOkYfho5FM3xsDP1TrKWVr08XQMg==')




    def run(self):
        try:
            self._work(self.task)
        except Exception as ex:
            self.status = ex
        else:
            self.status = 'success'


    def start_work(self,task):
        self.task = task
        self.status = None
        self.start() 


    def is_active(self):
        return self.is_alive()


    def is_success(self):
        if self.is_alive():
            return None
        else:
            if self.status == 'success':
                return True
            else:
                return False

    def get_id(self):
        return self.worker_id


    def _download(self,task):
        log("_download start", LogLevel.info)
        if not os.path.exists(self.work_directory):
            os.makedirs(self.work_directory)

        filename = "photo.jpg"
        stylename = "style.jpg"
        file_path = self.work_directory + "/" + filename
        style_path = self.work_directory + "/" + stylename
        self.block_blob_service.get_blob_to_path('photos',task.blobid,file_path)
        self.block_blob_service.get_blob_to_path('styles',task.styleid,style_path)

        log("_download end", LogLevel.info)
        return (file_path,style_path)


    def _transfer(self, file_path, style_path, target_path):
        log("transfer start", LogLevel.info)
        command_line = 'python neural_style_transfer.py ' +file_path + ' '+ style_path + ' ' + target_path
        os.system(command_line)
        log("transfer end", LogLevel.info)


    def _upload(self,task,merged_art):
        log("_upload_start", LogLevel.info)
        if os.path.exists(merged_art):
            
            blobname = "mergedart" + task.blobid
            self.block_blob_service.create_blob_from_path(
                'mergedarts', blobname, merged_art, content_settings=ContentSettings(content_type='image/jpg')
            )
            return True
        else:
            return False
            

    def _clean_up(self):
        log("delete " + self.work_directory, LogLevel.info)
        shutil.rmtree(self.work_directory, ignore_errors=True)


    def _work(self,task):
        log("_work start", LogLevel.info)
        self.work_directory = "../" +task.directory

        (file_path,style_path) = self._download(task)

        merged_art = self.work_directory + "/mergedart.jpg"

        self._transfer(file_path,style_path, merged_art)
        if self._upload(task,merged_art):
            self._clean_up()
        log("_work end", LogLevel.info)

        




   
        
