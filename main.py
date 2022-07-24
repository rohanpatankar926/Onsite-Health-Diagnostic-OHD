
# importing the necessary tools
from flask import Flask, render_template, request,redirect, url_for, session
# to let flask interact easily while performing file and folder processes irrespective of operating system
import os
import sys
# load the model using joblib
import joblib
import numpy as np
# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
# root directory
webroot = 'src'
static_dir = os.path.join(webroot,'static')
template_dir = os.path.join(webroot,'templates')
# defining the flask app
app = Flask(__name__,static_folder=static_dir,template_folder=template_dir)
# route for home page
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

# route for disease section
@app.route('/disease',methods=['GET','POST'])
def disease():
    return render_template('disease.html')

# breast cancer section
@app.route('/breastcancer',methods=['GET','POST'])
def breastcancer():
    if request.method == "POST":
        try:
            Radius_Mean = float(request.form["radius_mean"])
            Area_Mean = float(request.form["area_mean"])
            Compactness_Mean = float(request.form["compactness_mean"])
            Concavity_Mean = float(request.form["concavity_mean"])
            Concave_Points_Mean = float(request.form["concave_points_mean"])
            Area_Worst = float(request.form["area_worst"])
            Compactness_Worst = float(request.form["compactness_worst"])
            Concavity_Worst = float(request.form["concavity_worst"])
            Area_Se = float(request.form["area_se"])
            Fractal_Dimension_Se = float(request.form["fractal_dimension_se"])
            Symmetry_Worst = float(request.form["symmetry_worst"])
            Fractal_Dimension_Worst = float(request.form["fractal_dimension_worst"])

            breast_file = "breast_model.sav"
            loaded_breast_model = joblib.load(breast_file)
            breast_pred = loaded_breast_model.predict([[Radius_Mean, Area_Mean, Compactness_Mean, Concavity_Mean,
            Concave_Points_Mean, Area_Worst, Compactness_Worst,Concavity_Worst, 
            Area_Se, Fractal_Dimension_Se, Symmetry_Worst, Fractal_Dimension_Worst]])
            breast_pred = round(100*breast_pred[0])
            if(breast_pred == 0):
                res = "Congratulations! you are safe from Breast Cancer"
            else:
                res = "Sorry :( you have encountered with Breast Cancer"
            return render_template('breastcancer.html',prediction=res)

        except Exception as e:
            print(e)
            error=("Please fill all the fields for prediction🤦🤦")
            error={"error":error}
            return render_template("404.html",error=error)
    else:
        return render_template('breastcancer.html')

# Diabetes section
@app.route('/diabetes',methods=['GET','POST'])
def diabetes():
    if request.method == "POST":
        try:
            Pregnancies = float(request.form["Pregnancies"])
            Glucose = float(request.form["Glucose"])
            Bloodpressure = float(request.form["Bloodpressure"])
            SkinThickness = float(request.form["SkinThickness"])
            Insulin = float(request.form["Insulin"])
            BMIn = float(request.form["BMI"])
            DiabetesPedigreeFunction = float(request.form["DiabetesPedigreeFunction"])
            Age = float(request.form["Age"])
            filename = "diabetes.sav"
            loaded_model = joblib.load(filename)
            dia_pred = loaded_model.predict([[Pregnancies,Glucose,Bloodpressure,SkinThickness,Insulin,BMIn,DiabetesPedigreeFunction,Age]])
            dia_pred = round(100*dia_pred[0])
            if(dia_pred == 0):
                res = "Congratulations! you are safe from Diabetes"
            else:
                res = "Sorry :( you have encountered with Diabetes"
            return render_template('diabetes.html',prediction=res)

        except Exception as e:
            print(e)
            error=("Please fill all the fields for diabetes prediction🤦🤦")
            error={"error":error}
            return render_template("404.html",error=error)
    else:
        return render_template('diabetes.html')

@app.route('/heart',methods=['GET','POST'])
def heart():
    if request.method == 'POST':
        try:
            Age = float(request.form["age"])
            sex = (request.form["sex"])
            if(sex == "male"):
                sex = 1
            else:
                sex = 0
            #chest pain
            chestpain = (request.form["chestpain"])
            if(chestpain == "ATA"):
                chestpain = 1
            elif (chestpain == "NAP"):
                chestpain = 2
            elif (chestpain == "ASY"):
                chestpain = 0
            else:
                chestpain = 3
            # resting bp
            restingbp = float(request.form["restingbp"])
            cholestrol = float(request.form["cholestrol"])
            fastingbs = float(request.form["fastingbs"])
            restingecg = (request.form["restingecg"])
            if(restingecg == "Normal"):
                restingecg = 1
            elif (restingecg == "ST"):
                restingecg = 2
            else:
                restingecg = 0

            maxhr = float(request.form["maxhr"])
            exercise = (request.form["exercise"])
            if(exercise == "N"):
                exercise = 0
            else:
                exercise = 1

            oldpeak = float(request.form["oldpeak"])
            stslope = (request.form["stslope"])
            if(stslope == "up"):
                stslope = 2
            elif(stslope == "flat"):
                stslope = 1
            else:
                stslope = 0
            file_heart = "heart_model.sav"
            loaded_model = joblib.load(file_heart)
            heart_pred = loaded_model.predict([[Age, sex, chestpain, restingbp, cholestrol, fastingbs, restingecg, maxhr,
            exercise, oldpeak, stslope]])

            heart_pred = round(100*heart_pred[0])
            if(heart_pred == 0):
                res = "Congratulations! you are safe from Heart Disease"
            else:
                res = "Sorry :( you have encountered with Heart Failure"
            return render_template('heart.html',predict = res)

        except Exception as e:
            print(e)
            error=("Please fill all the fields for heart disease prediction🤦🤦")
            error={"error":error}
            return render_template("404.html",error=error)
    else:
        return render_template('heart.html')

#pneumonia prediction section

# load pneumonia model path
PNEUMONIA_MODEL_PATH = 'pneumonia_model.h5'

#Load your trained model
model = load_model(PNEUMONIA_MODEL_PATH)
# pneumonia detection
def pneumonia_predict(img_path, model):
    img = image.load_img(img_path, target_size=(64, 64)) #target_size must agree with what the trained model expects!!
    # Preprocessing the image
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    preds = model.predict(img)
    return preds

@app.route('/pneumonia',methods=['GET','POST'])
def pneumonia():
    if request.method == 'POST':
        try:
            # Get the file from post request
            f = request.files['file']
            # Save the file to ./uploads
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(
                basepath, '', secure_filename(f.filename))
            f.save(file_path)
            # Make prediction
            preds = pneumonia_predict(file_path, model)
            os.remove(file_path)#removes file from the server after prediction has been returned
            if preds == 1:
                res = "Sorry :( you have got the chances of Pneumonia"
            else:
                res = "Congratulations! you are safe from Pneumonia"
            return render_template('pneumonia.html',prediction=res)
        except Exception as e:
            print(e)
            error=("Have you uploaded the image??🤔🤔")
            error={"error":error}
            return render_template("404.html",error=error)
    return render_template('pneumonia.html')

# thyroid static page
@app.route('/thyroid',methods=['GET','POST'])
def thyroid():
    return render_template('thyroid.html')
# Driver code
port = int(os.environ.get("PORT", 5000))

if __name__=="__main__":
    
    app.run(debug=True,port=port,host="0.0.0.0")
