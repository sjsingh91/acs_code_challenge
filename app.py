import os
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template
from acs_code_challenge import acs_code
from datetime import date

UPLOAD_FOLDER = 'uploads/'
DOWNLOAD_FOLDER = 'downloads/'

#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("saved file successfully")

      #send file name as parameter to downlad
            return redirect('/downloadfile/'+ filename)
    return render_template('upload_file.html')
# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])

def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(file_path)
    p1 = acs_code()
    p2 = p1.final_group(file_path)
    p2.to_csv(f'downloads/{date.today()}_SearchKeywordPerformance.tab',sep = "\t", index = False)
    filename = f'{date.today()}_SearchKeywordPerformance.tab'
    return render_template('download.html',value=filename)
@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = DOWNLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

@app.route('/')
def homepage():
    return redirect('/uploadfile')
if __name__ == "__main__":
    app.run()

    # redirect('/uploadfile')