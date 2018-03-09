from flask import Flask, render_template, request
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

app = Flask(__name__)

@app.route("/")
def index():

    #art=Art()
    #art.style=request.form.get()
    #art.original=request.form.get()
    #art.contact=request.form.get("email")
    return render_template("index.html")

@app.route("/steps", methods=['post'])
def add_art():
    art =  Entity()
    art.PartitionKey 
    art.RowKey 
    art.style = request.form.get()
    art.origin = request.form.get()
    art.contact = request.form.get('email')
    art.status = New
    table_service.insert_entity('photoart',art)
    return render_template("congrt.html")

@app.route("/completion")
def congrt():
    return "congratulation"
