import os
import threading
import shutil
import workerthread
from azure.storage.blob import BlockBlobService, ContentSettings


class Worker:
    def __init__(self,x):
        self.worker_id = x
        self.block_blob_service = BlockBlobService(
            account_name='photofunstorage', account_key='Br6qGU0woc+qOQtsneQ6XkgQx6gsmcvmbg9Eyh6+gpISHwmu48o+rmBzIQvOkYfho5FM3xsDP1TrKWVr08XQMg==')


    def start_work(self,task):
        self.thread = workerthread.WorkerTread(target=self._work, args=(task))
        self.thread.start() 


    def is_success(self):
        if self.is_active():
            return None
        else:
            if self.thread.status == 'success':
                return True
            else:
                return False
       

    def is_active(self):
        return self.thread.is_alive()
            


    def get_id(self):
        return self.worker_id


    def _download(self,task):
        
        if not os.path.exists(self.work_directory):
            os.makedirs(self.work_directory)

        file_path = self.work_directory + "/" + task.blobid
        style_path = self.work_directory + "/" + task.styleid
        self.block_blob_service.get_blob_to_path('photos',task.blobid,file_path)
        self.block_blob_service.get_blob_to_path('styles',task.styleid,style_path)

        return (file_path,style_path)


    def _transfer(self, file_path, style_path, target_path):
        command_line = 'python test.py ' +file_path + ' '+ style_path + ' ' + target_path
        os.system(command_line)


    def _upload(self,task,merged_art):
       
        if merged_art in self.work_directory:
            blobname = "mergedart" + task.blobid
            self.block_blob_service.create_blob_from_path(
                'mergedarts', blobname, merged_art, content_settings=ContentSettings(content_type='image/jpg')
            )
            return True
        else:
            return False
            

    def _clean_up(self):
        print("delete " + self.work_directory)
        #shutil.retree(self.work_directory, ignore_errors=True)


    def _work(self,task):
        self.work_directory = "../" +task.directory

        (file_path,style_path) = self._download(task)

        merged_art = self.work_directory + "/mergedart" +task.blobid

        self._transfer(file_path,style_path, merged_art)
        if self._upload(task,merged_art):
            self._clean_up()

        




   
        
