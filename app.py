from flask import Flask,render_template,request, url_for
import pandas as pd
import pickle
app =Flask(__name__)

df_1=pd.read_csv("../Project/Telco-Customer-Churn-Prediction/first_telc.csv")
@app.route("/")
def loadPage():
	return render_template('index.html', query="")

@app.route("/", methods=['POST'])
def predict():

    '''
    SeniorCitizen
    MonthlyCharges
    TotalCharges
    gender
    Partner
    Dependents
    PhoneService
    MultipleLines
    InternetService
    OnlineSecurity
    OnlineBackup
    DeviceProtection
    TechSupport
    StreamingTV
    StreamingMovies
    Contract
    PaperlessBilling
    PaymentMethod
    tenure
    '''
    inputQuery1 = request.form['SeniorCitizen']
    inputQuery2 = request.form['MonthlyCharges']
    inputQuery3 = request.form['TotalCharges']
    inputQuery4 = request.form['Gender']
    inputQuery5 = request.form['Partner']
    inputQuery6 = request.form['Dependents']
    inputQuery7 = request.form['PhoneService']
    inputQuery8 = request.form['MultipleLines']
    inputQuery9 = request.form['InternetService']
    inputQuery10 = request.form['OnlineSecurity']
    inputQuery11 = request.form['OnlineBackup']
    inputQuery12 = request.form['DeviceProtection']
    inputQuery13 = request.form['TechSupport']
    inputQuery14 = request.form['StreamingTV']
    inputQuery15 = request.form['StreamingMovies']
    inputQuery16 = request.form['Contract']
    inputQuery17 = request.form['PaperlessBilling']
    inputQuery18 = request.form['PaymentMethod']
    inputQuery19 = request.form['tenure']
    # model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modeldt.sav", "rb"))
    # model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modellog.sav", "rb"))
    # model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modelrf.sav", "rb"))
    model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modelsvm.sav", "rb"))
    
    data = [[inputQuery1, inputQuery2, inputQuery3, inputQuery4, inputQuery5, inputQuery6, inputQuery7, 
             inputQuery8, inputQuery9, inputQuery10, inputQuery11, inputQuery12, inputQuery13, inputQuery14,
             inputQuery15, inputQuery16, inputQuery17, inputQuery18, inputQuery19]]
    new_df = pd.DataFrame(data, columns = ['SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'gender', 
                                           'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService',
                                           'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
                                           'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
                                           'PaymentMethod', 'tenure'])
    df_2 = pd.concat([df_1, new_df], ignore_index = True) 
    # Group the tenure in bins of 12 months
    labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
    
    df_2['tenure_group'] = pd.cut(df_2.tenure.astype(int), range(1, 80, 12), right=False, labels=labels)
    #drop column customerID and tenure
    df_2.drop(columns= ['tenure'], axis=1, inplace=True) 
    df_2.SeniorCitizen = pd.to_numeric(df_2.SeniorCitizen, errors='coerce')
    df_2.MonthlyCharges = pd.to_numeric(df_2.MonthlyCharges, errors='coerce')
    df_2.TotalCharges = pd.to_numeric(df_2.TotalCharges, errors='coerce')
    
    new_df__dummies = pd.get_dummies(df_2[['gender', 'SeniorCitizen','MonthlyCharges', 'TotalCharges', 'Partner', 'Dependents', 'PhoneService',
           'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
           'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
           'Contract', 'PaperlessBilling', 'PaymentMethod','tenure_group']])
    
    single = model.predict(new_df__dummies.tail(1))
    # probablity = model.predict_proba(new_df__dummies.tail(1))[:,1]
    
    if single==1:
        o1 = "This customer is churned!!"
        # o2 = "Confidence: {}".format(probablity*100)
    else:
        o1 = "This customer is not churn!!"
        # o2 = "Confidence: {}".format(probablity*100)
    return render_template('index.html', output1=o1,  
                           SeniorCitizen = request.form['SeniorCitizen'], 
                           MonthlyCharges = request.form['MonthlyCharges'],
                           TotalCharges = request.form['TotalCharges'],
                           Gender = request.form['Gender'],
                           Partner = request.form['Partner'], 
                           Dependents = request.form['Dependents'], 
                           PhoneService = request.form['PhoneService'], 
                           MultipleLines = request.form['MultipleLines'], 
                           InternetService = request.form['InternetService'], 
                           OnlineSecurity = request.form['OnlineSecurity'], 
                           OnlineBackup = request.form['OnlineBackup'], 
                           DeviceProtection = request.form['DeviceProtection'], 
                           TechSupport = request.form['TechSupport'], 
                           StreamingTV = request.form['StreamingTV'], 
                           StreamingMovies = request.form['StreamingMovies'], 
                           Contract = request.form['Contract'], 
                           PaperlessBilling = request.form['PaperlessBilling'],
                           PaymentMethod = request.form['PaymentMethod'], 
                           tenure = request.form['tenure'])

if __name__ == '__main__':
        app.run(debug=True)