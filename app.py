from flask import Flask, render_template, url_for, flash, redirect,request,send_file
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
import os
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
from img_to_text import call_img
import csv
from os.path import exists

# Create the app object
app = Flask(__name__)

app.config['SECRET_KEY'] = 'e6de11d424feadf290292c7124de34'
app.config['UPLOAD_FOLDER'] = 'static/files'

#import img_to_text

class inputForm(FlaskForm):
    search = StringField('search',validators=[DataRequired()])
    submit = SubmitField('Get Text')

class fileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField('Get Text')

@app.route('/',methods=['POST','GET'])
@app.route('/image-to-text',methods=['GET',"POST"])
def home():
    form = inputForm()
    if form.validate_on_submit():
        return redirect(url_for('output'))    
    return render_template('index.html',form=form)

@app.route('/output',methods=['POST','GET'])
def output():
    a = request.form['search']
    print('-----------------',a)
    result =call_img(a)
    print("result==",result)
    return render_template('output.html', output_text=str(result))




@app.route('/download')
def download():
    p="bilal.csv"
    return send_file(p,as_attachment=True)
    

def save_in_csv(wr): 
    with open('bilal.csv', 'a',encoding='utf-8',errors='ignore',newline='') as file:
        writer = csv.writer(file,delimiter='|')
        writer.writerow(wr)



@app.route('/csv-to-text',methods=['POST','GET'])
def file():
    csv_exist= exists('static/files/myfile.csv')
    if(csv_exist==False):
        with open('static/files/myfile.csv','a',encoding='utf-8',errors='ignore',newline='') as f:
            writer = csv.writer(f,delimiter='|')
            writer.writerow(["image_url"])
        print("yes")
    else:
        os.remove("static/files/myfile.csv")
        with open('static/files/myfile.csv','a',encoding='utf-8',errors='ignore',newline='') as f:
            writer = csv.writer(f,delimiter='|')
            writer.writerow(["image_url"])
    csv_exist= exists('bilal.csv')
    if(csv_exist==False):
        with open('bilal.csv','a',encoding='utf-8',errors='ignore',newline='') as f:
            writer = csv.writer(f,delimiter='|')
            writer.writerow(["image_url","text"])
        print("yes")
    else:
        os.remove("bilal.csv")
        with open('bilal.csv','a',encoding='utf-8',errors='ignore',newline='') as f:
            writer = csv.writer(f,delimiter='|')
            writer.writerow(["image_url","text"])

    form = fileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename("myfile.csv")))
        output=[]
        with open('static/files/myfile.csv', mode ='r')as file:
            csvFile = csv.reader(file)
            
            for lines in csvFile:
                a = lines[0]
                #print(a)
                result=""
                result =call_img(a)
                #result= str(result)
                print(type(result))
                print (a , result)
                wr=[a,result]
                print(wr)
                save_in_csv(wr)
        return redirect(url_for('download'))
        return redirect('file') 
        
        #return redirect(url_for('download')) 
        #return redirect('file')


    return render_template('file.html',form=form)



if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')