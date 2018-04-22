import os
import time
import smtplib
import worker
from logger import log, LogLevel
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

        self.block_blob_service = BlockBlobService(account_name='photofunstorage', account_key=os.environ['ACCOUNT_KEY'])
        self.table_service = TableService(account_name='photofunstorage', account_key=os.environ['ACCOUNT_KEY'])

    def handle_jobs(self):
        log("handle job",LogLevel.info)
        tasks = self.table_service.query_entities(
            'photoart', filter="state eq 'new' or state eq 'processing' or state eq 'processed'")
        for task in tasks:
            if task.state == 'processing':   # define Enum for these states
                log("master: processing task " + task.RowKey, LogLevel.info)
                worker = self.workerid_worker[task.workerid]
                if not worker.is_active():
                    if not worker.is_success():
                        self.assign_job(task)
                    else:
                        task.state = 'processed'
            elif task.state == 'new':
                log("master new task " + task.RowKey, LogLevel.info)
                if self.assign_job(task):
                    task.state = 'processing'
            elif task.state == 'processed':
                log("master processed " + task.RowKey, LogLevel.info)
                if self.email_art(task):
                    task.state = 'emailed'

        self.update_states(tasks)


    def assign_job(self, task):
        log("assign job", LogLevel.info)
        has_assigned = False
        for workerid, worker in self.workerid_worker.items():
            if not worker.is_active():
                task.workerid = workerid
                task.directory = "tmp/" + task.blobid
                worker.start_work(task)
                has_assigned = True
                break
        return has_assigned


    def email_art(self, task):
        log("email art", LogLevel.info)
        try:
            download_file = self._download_art(task)

            fromaddr = "photofunfunfun@gmail.com"
            toaddr = task.contact

            msg = MIMEMultipart()

            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Welcome to photo fun!"
            body = "Attached is the Chinese ancient style art you create."
            msg.attach(MIMEText(body, 'plain'))

            filename = "Photofun.jpg"
            attachment = open(download_file, "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            "attachment; filename= %s" % filename)
            msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, os.environ['EMAIL_PASSWORD'])
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            
            os.remove(download_file)
            log("email done", LogLevel.info)
            return True
        except Exception as ex:
            log(ex, LogLevel.error)
            return False


    def update_states(self, tasks):
        batch = TableBatch()
        for task in tasks:
            batch.insert_or_merge_entity(task)
        self.table_service.commit_batch('photoart', batch)

    def run(self):
        while True:
            try:
                self.handle_jobs()
                time.sleep(60)
            except Exception as ex:
                log(ex, LogLevel.error)


    def _download_art(self,task):
        art_name = "mergedart" + task.blobid
        download_file_path = art_name

        self.block_blob_service.get_blob_to_path('mergedarts',art_name,download_file_path)
        return download_file_path

if __name__ == '__main__':
    workers = []
    for i in range(2):
        workers.append(worker.Worker(str(i)))
    master = Master(workers)
    master.run()
