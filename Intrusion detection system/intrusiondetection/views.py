from django.shortcuts import render

import os

from intrusiondetection.forms import UserForm, LoginForm
from intrusiondetection.models import UserModel

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

from keras.models import load_model
import tensorflow as tf


import numpy as np



def registration(request):

    status = False

    if request.method == "POST":
        # Get the posted form
        registrationForm = UserForm(request.POST)

        if registrationForm.is_valid():

            regModel = UserModel()

            passowrd=registrationForm.cleaned_data["password"]
            cpassword=registrationForm.cleaned_data["conformpassword"]

            if passowrd==cpassword:
                print("in insertion")
                regModel.username = registrationForm.cleaned_data["username"]
                regModel.password = registrationForm.cleaned_data["password"]
                regModel.email = registrationForm.cleaned_data["email"]
                regModel.mobile = registrationForm.cleaned_data["mobile"]
                regModel.name = registrationForm.cleaned_data["name"]

                user = UserModel.objects.filter(username=regModel.username).first()

                if user is not None:
                    print("Exist")
                    return render(request, 'registration.html', {"message": "User All Ready Exist"})
                else:
                    regModel.save()
                    print("Done")
                    return render(request, 'login.html', locals())
            else:
                print("password is not matching")
                return render(request, 'registration.html', {"message": "Password and Conform Password is Not Matching"})
        else:
            return render(request, 'registration.html', {"message": "Invalid Form"})
    else:
        return render(request, 'registration.html', {"message": "Invalid Request"})

def login(request):

    if request.method == "GET":
        # Get the posted form
        loginForm = LoginForm(request.GET)

        if loginForm.is_valid():

            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]

            client = UserModel.objects.filter(username=uname, password=upass).first()

            if client is not None:
                return render(request, 'predict.html')
            else:
                return render(request, 'login.html', {"message": "Invalid Credentials"})
        else:
            return render(request, 'login.html', {"message": "Invalid Form"})

    return render(request, 'login.html', {"message": "Invalid Request"})

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'index.html', {})
#====================================================================================

def predict(request):

    graph = tf.Graph()

    with graph.as_default():

        with tf.compat.v1.Session(graph=graph) as sess:

            int_features = []

            int_features.append(float(request.GET["protocol_type"]))
            int_features.append(float(request.GET["flag"]))
            int_features.append(float(request.GET["src_bytes"]))
            int_features.append(float(request.GET["dst_bytes"]))
            int_features.append(float(request.GET["count"]))
            int_features.append(float(request.GET["same_srv_rate"]))
            int_features.append(float(request.GET["diff_srv_rate"]))
            int_features.append(float(request.GET["dst_host_same_srv_rate"]))
            int_features.append(float(request.GET["dst_host_same_src_port_rate"]))
            int_features.append(float(request.GET["last_flag"]))

            sample_input_record = np.array(int_features)
            print(sample_input_record)
            loaded_dl_model = load_model(PROJECT_PATH + "/model/dl_model.h5")
            predicted_output = loaded_dl_model.predict_classes(sample_input_record.reshape(1, -1))
            print("Predicted Output:", predicted_output)
            predict=predicted_output[0]

            if predict == 0:
                output = 'Normal'
            elif predict == 1:
                output = 'DOS'
            elif predict == 2:
                output = 'PROBE'
            elif predict == 3:
                output = 'R2L'
            else:
                output = 'U2R'

            return render(request, 'predict.html', {"message":output})