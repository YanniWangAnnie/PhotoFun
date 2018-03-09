from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

table_service =  TableService(account_name="photofunstorage",account_key="###")
table_service.create_table('photoart')
