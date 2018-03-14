from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entit

block_blob_service = BlockBlobService(account_name='photofunstorage', account_key='Br6qGU0woc+qOQtsneQ6XkgQx6gsmcvmbg9Eyh6+gpISHwmu48o+rmBzIQvOkYfho5FM3xsDP1TrKWVr08XQMg==')
table_service = TableService(account_name='photofunstorage', account_key='Br6qGU0woc+qOQtsneQ6XkgQx6gsmcvmbg9Eyh6+gpISHwmu48o+rmBzIQvOkYfho5FM3xsDP1TrKWVr08XQMg==')

class Master:
    def __init__(self):
        self.worker_states = {}
        self.rowkey_worker = {}

    def get_jobs(self):
        

    def kick_off(self):


    def check_states(self):


    def update_states(self):


    def run(self)

