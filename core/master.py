import os
import time
import smtplib
import worker
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from azure.storage.blob import BlockBlobService, ContentSettings
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tablebatch import TableBatch

# should be property of master

class Master:
    def __init__(self, workers):
        self.workerid_worker = {}
        for worker in workers:
            self.workerid_worker[worker.get_id()] = worker

        self.block_blob_service = BlockBlobService(
            account_name='photofunstorage', account_key='Br6qGU0woc+qOQtsneQ6XkgQx6gsmcvmbg9Eyh6+gpISHwmu48o+rmBzIQvOkYfho5FM3xsDP1TrKWVr08XQMg==')
        self.table_service = TableService(account_name='photofunstorage',
                                     account_key='Br6qGU0woc+qOQtsneQ6XkgQx6gsmcvmbg9Eyh6+gpISHwmu48o+rmBzIQvOkYfho5FM3xsDP1TrKWVr08XQMg==')

    def handle_jobs(self):
        tasks = self.table_service.query_entities(
            'photoart', filter="state eq 'new' or state eq 'processing' or state eq 'processed")
        for task in tasks:
            if task.state == 'processing':   # define Enum for these states
                worker = self.workerid_worker[task.workerid]
                if not worker.is_active():
                    if not worker.is_success():
                        self.assign_job(task)
                    else:
                        task.state = 'processed'
            elif task.state == 'new':
                if self.assign_job(task):
                    task.state = 'processing'
            elif task.state == 'processed':
                if self.email_art(task):
                    task.state = 'emailed'

        self.update_states(tasks)


    def assign_job(self, task):
        has_assigned = False
        for workerid, worker in self.workerid_worker:
            if not worker.is_active():
                task.workerid = workerid
                task.directory = "tmp/" + task.blobid
                worker.work(task)
                has_assigned = True
                break
        return has_assigned


    def email_art(self, task):
        try:
            fromaddr = "photofunfunfun@gmail.com"
            toaddr = task.contact

            msg = MIMEMultipart()

            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Welcome to photo fun!"
            body = "Attached is the Chinese ancient style art you create."
            msg.attach(MIMEText(body, 'plain'))

            filename = "Photofun.jpg"
            attachment = open(self._download_art(task), "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            "attachment; filename= %s" % filename)
            msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "photofunfun")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            return True
        except Exception as ex:
            print(ex)
            return False


    def update_states(self, tasks):
        batch = TableBatch()
        for task in tasks:
            batch.insert_entity(task)
        self.table_service.commit_batch('photoart', batch)

    def run(self):
        while True:
            self.handle_jobs()
            time.sleep(6)
        
    """
    def _get_artname(self, task):
        return 'mergedart' + task.blobid
    """

    def _download_art(self,task):
        art_name = "mergedart" + task.blobid
        download_file_path = art_name

        self.block_blob_service.get_blob_to_path('mergedarts',art_name,download_file_path)
        return download_file_path

if __name__ == '__main__':
    workers = []
    for i in range(4):
        workers.append(worker.Worker(str(i)))
    master = Master(workers)
    master.run()
