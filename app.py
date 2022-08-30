from flask import Flask,request,render_template,session
import csv
import os
import re
import smtplib as s


app=Flask(__name__)
app.debug=True
email_condition=r"^[a-z]+[\._]?[A-Z 0-9]+[@]\w+[.]\w{2,3}$"
data1=[]
data2=[]
valid=[]
invalid=[]
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/upload",methods=['POST','GET']) 
def upload():
    data1.clear();
    data2.clear();
    valid.clear();
    invalid.clear();
    if(request.method=='POST'):
        file=request.files['file'];
        name=file.filename;
        savepath=os.path.join('UPLOADED_FILE',file.filename)
        file.save(savepath)
        with open(savepath,"r") as f:
            csvf=csv.reader(f)
            for row in csvf:
                data1.append(str(row)[2:-2]);
        # data2=data1[1:]
        for item in data1[1:]:
            if re.search(email_condition,item):
                valid.append(item)
            else:
                invalid.append(item)          

    return render_template("details.html",pure=valid,impure=invalid);    
@app.route('/sendmail',methods=['POST','GET'])
def info():
    return render_template('getinfo.html')
@app.route('/send',methods=['POST','GET'])
def mailsender():
    item=s.SMTP('smtp.gmail.com',587)
    item.ehlo()
    item.starttls()
    if request.method=='POST':
        mailaddres=request.form['email']
        password=request.form['password']
        subject=request.form['subject']
        body=request.form['message']
        msg="Subject:{0}\n\n{1}".format(subject,body)
        item.login(mailaddres,password)

        for m in valid:
            item.sendmail(mailaddres,m,msg)
            
        item.quit()
    return render_template('getinfo.html',status=True)
if __name__=="__main__":
    app.run(debug=True)    