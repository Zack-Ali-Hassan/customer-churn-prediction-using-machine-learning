from flask import Flask,render_template,request, url_for,redirect,session
import mysql.connector
import re
import pandas as pd
import pickle

app =Flask(__name__)
app.secret_key = "zxsdasdasdasdsd"

# load your data
df_1=pd.read_csv("../Project/Telco-Customer-Churn-Prediction/first_telc.csv")

# MySQL configurations
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'customer_churn'
}


@app.route("/")
def loadPage():
      if 'username' in session:
        return render_template('index.html', query="")
      return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
          email = request.form['email']
          password = request.form['password']
          conn = mysql.connector.connect(**mysql_config)
          cursor = conn.cursor(dictionary=True)
          cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
          user = cursor.fetchone()
          cursor.close()
          conn.close()

          if user:
            session['username'] = user['name']
            session['email'] = user['email']
            return redirect(url_for('index'))
          else:
            return render_template('login.html', error='Sorry Invalid email or password')
     return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

         # Check if the name is valid
        if not is_valid_name(name):
            return render_template('signup.html', error='Invalid name. Please enter a valid name.')
        # Check if email already exists
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            cursor.close()
            conn.close()
            return render_template('signup.html', error='Sorry!. his email already exists')

        # Insert user into database
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s, %s)", (name,email, password))
        conn.commit()
        cursor.close()
        conn.close()

        # session['username'] = name
        return redirect(url_for('login'))
    return render_template('signup.html')

def is_valid_name(name):
    # Add your validation logic here, for example:
    # Name should contain only alphabets and spaces
    return bool(re.match("^[a-zA-Z ]+$", name))

@app.route("/predict", methods=['POST'])
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

    #drop column tenure
    df_2.drop(columns= ['tenure'], axis=1, inplace=True) 
    df_2.SeniorCitizen = pd.to_numeric(df_2.SeniorCitizen, errors='coerce')
    df_2.MonthlyCharges = pd.to_numeric(df_2.MonthlyCharges, errors='coerce')
    df_2.TotalCharges = pd.to_numeric(df_2.TotalCharges, errors='coerce')
    
    new_df__dummies = pd.get_dummies(df_2[['gender', 'SeniorCitizen','MonthlyCharges', 'TotalCharges', 'Partner', 'Dependents', 'PhoneService',
           'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
           'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
           'Contract', 'PaperlessBilling', 'PaymentMethod','tenure_group']])
    
    # Load model
    # model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modeldt.sav", "rb"))
    model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modellog.sav", "rb"))
    # model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modelrf.sav", "rb"))
    # model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modelsvm.sav", "rb"))

    single = model.predict(new_df__dummies.tail(1))
    
    if single==1:
        o1 = "This customer is churned!!."
    else:
        o1 = "This customer is not churn."
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