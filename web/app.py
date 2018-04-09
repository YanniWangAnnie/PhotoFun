from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.utils import secure_filename
import os
import time
from azure.storage.blob import BlockBlobService, ContentSettings
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

block_blob_service = BlockBlobService(account_name='photofunstorage', account_key='Br6qGU0woc+qOQtsneQ6XkgQx6gsmcvmbg9Eyh6+gpISHwmu48o+rmBzIQvOkYfho5FM3xsDP1TrKWVr08XQMg==')
table_service = TableService(account_name='photofunstorage', account_key='Br6qGU0woc+qOQtsneQ6XkgQx6gsmcvmbg9Eyh6+gpISHwmu48o+rmBzIQvOkYfho5FM3xsDP1TrKWVr08XQMg==')


UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = set(['jpg','jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'Thisisasecret'



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nextstep", methods=['GET','POST'])
def nextstep():
    styleid = request.args.get('styleid')
  

    if request.method == "POST":
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            blobname = str(time.time())
            block_blob_service.create_blob_from_path(
                'photos', blobname,'temp/'+filename, content_settings=ContentSettings(content_type='image/jpg')
            )
        art =  Entity()
        art.PartitionKey = 'seattle'
        art.RowKey = str(time.time())
        art.styleid = styleid
        art.blobid = blobname
        art.contact = request.form['emailaddr']
        art.state = 'new'
        table_service.insert_entity('photoart',art)  

        return "Congratulations!"
    return render_template("nextstep.html", styleid=styleid)


@app.route("/completion")
def congrt():
    return "congratulation"

if __name__ == '__main__':
    app.run(debug=True)
