from flask import Flask, jsonify, render_template, request,redirect,url_for
from keras.models import load_model
import joblib
import os
import sys
import numpy as np
from pathlib import Path
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/Contact")
def Contact():
    return render_template("contact_us.html")

@app.route("/source")
def source():
    return render_template("src.html")
@app.route("/gmail")
def gmail():
    return redirect("https://accounts.google.com/signin/v2/identifier?service=mail&passive=true&rm=false&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F%26ogbl%2F&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin",code=302)

@app.route('/predict',methods=['POST','GET'])
def result():

    src_bytes= int(request.form['src_bytes'])

    dst_bytes=int(request.form['dst_bytes'])
    hot=int(request.form['hot'])
    logged_in=int(request.form['log_in'])
    count=int(request.form['count'])
    serror_rate=float(request.form['serror_rate'])
    dst_host_same_srv_rate=float(request.form['dst_host_same_srv_rate'])
    dst_host_srv_diff_host_rate=float(request.form['dst_host_srv_diff_host_rate'])
    dst_host_srv_serror_rate=float(request.form["dst_host_srv_serror_rate"])
    last_flag=int(request.form['last_flag'])
    protocol_type=str(request.form['protocol_type'])
    service=str(request.form['service'])
    flag=str(request.form['flag'])
    model_nm=str(request.form['model'])
    if flag=="flag_S0":
                flag_S0=1
                flag_S1=0
    elif flag=="flag_S1":
                flag_S1=1
                flag_S0=0   
    else:
                flag_S0=0
                flag_S1=0
            
    if service=="ecr_i":
                service_ecr_i=1
                service_http=0
                service_other=0

    elif service=="http":
                service_ecr_i=0
                service_http=1
                service_other=0
    elif service=="other":
                service_ecr_i=0
                service_http=0
                service_other=1
            
    else:
                
                service_ecr_i=0
                service_http=0
                service_other=0

    if protocol_type=="tcp":
                protocol_type_tcp=1
    else:
                protocol_type_tcp=0








            
    X= np.array([[ src_bytes, dst_bytes, hot, logged_in, count, serror_rate,
            dst_host_same_srv_rate, dst_host_srv_diff_host_rate,
            dst_host_srv_serror_rate, last_flag, protocol_type_tcp,
            service_ecr_i, service_http, service_other, flag_S0, flag_S1 ]])



    path_current = app.instance_path
    path_current=path_current[:-8]
    print(path_current)
    
    #scaler_path= path_current.joinpath('/models/sc.sav')
    #scaler_path=os.path.join(path_current, 'models\sc.sav')
    scaler_path=os.path.join(path_current, 'models\\sc.sav')

    print("Scalar path is **********")
    print(scaler_path)
    print(app.instance_path)
    #scaler_path=scaler_path.as_posix()

    sc=joblib.load(scaler_path)

    X_std= sc.transform(X)


    if model_nm=="logistic":
        model_path=os.path.join(path_current, 'models\\LogisticRegressionStdSc.sav')
    elif model_nm=="Adaboost":
        model_path=os.path.join(path_current, 'models\\Adboost_SC2.sav')
    elif model_nm=="XGBoost":
        model_path=os.path.join(path_current, 'models\\XGBClassifierStdSc.sav')
    elif model_nm=="DecisionTree":
        model_path=os.path.join(path_current, 'models\\DecisionTreeClassifierStdSc.sav')
    elif model_nm=="Gradboost":
        model_path=os.path.join(path_current, 'models\\GradientBoostingClassifierStdSc.sav')

    elif model_nm=="Catboost":
        model_path=os.path.join(path_current, 'models\\CatBoostClassifierStdSc.sav')
    
    elif model_nm=="SVC":
        model_path=os.path.join(path_current, 'models\\SVCStdSc.sav')

    elif model_nm=="ANN":
        model_path=os.path.join(path_current, 'models\\ANN.h5')

        

    else:
        model_path=os.path.join(path_current, 'models\\RandomForestClassifierStdSc.sav')

        




    


    #model_path=os.path.join(path_current, 'models\\rf.sav')
    #model_path=path_current.joinpath('/models/rf.sav')
    
    #model_path=model_path.as_posix()
#model_path=r'F:\Project\Network Anamoly Detection\Network Anamoly Detection\models\rf.sav'
    print("*****",model_path)

    if model_nm=="ANN":
        model=load_model(model_path)
    else:
        model= joblib.load(model_path)

    #Y_pred=model.predict(X_std)
    Y_pred=np.round(model.predict(X_std))


    if Y_pred==0:
                result="Normal"
    else:
                result="Attack"
                
        
    #return jsonify({'Prediction': result})
    return render_template("predict.html",result=result)

if __name__ == "__main__":
    app.run(debug=True, port=9457)
