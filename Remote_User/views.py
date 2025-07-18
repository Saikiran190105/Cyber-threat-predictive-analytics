from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import openpyxl

import nltk
import re
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
# Create your views here.
from Remote_User.models import ClientRegister_Model,Cyber_model,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Add_DataSet_Details(request):

    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})


def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city)

        return render(request, 'RUser/Register1.html')
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Predict_CyberThreat_Type(request):
    if request.method == "POST":
        review = request.POST.get('keyword')
        if request.method == "POST":

            Name_of_Covered_Entity= request.POST.get('Name_of_Covered_Entity')
            State= request.POST.get('State')
            Individuals_Affected= request.POST.get('Individuals_Affected')
            Date_of_Breach= request.POST.get('Date_of_Breach')
            Location_of_Breached_Information= request.POST.get('Location_of_Breached_Information')
            Date_Posted_or_Updated= request.POST.get('Date_Posted_or_Updated')
            breach_start= request.POST.get('breach_start')
            year= request.POST.get('year')
            Source_Ip= request.POST.get('Source_Ip')
            Destination_Ip= request.POST.get('Destination_Ip')

        data = pd.read_csv("Cyber_Threat.csv")
        # data.replace([np.inf, -np.inf], np.nan, inplace=True)

        mapping = {'Theft': 0,
                   'Loss': 1,
                   'Disclosure': 2,
                   'Hacking': 3,
                   'Improper Disposal': 4

                   }
        data['Label'] = data['Type_of_Breach'].map(mapping)

        x = data['Name_of_Covered_Entity']
        y = data['Label']

        # data.drop(['Type_of_Breach'],axis = 1, inplace = True)
        cv = CountVectorizer()

        print(x)
        print(y)

        labeled = 'labeled_data.csv'
        data.to_csv(labeled, index=False)
        data.to_markdown

        x = cv.fit_transform(x)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Naive Bayes")

        from sklearn.naive_bayes import MultinomialNB

        NB = MultinomialNB()
        NB.fit(X_train, y_train)
        predict_nb = NB.predict(X_test)
        naivebayes = accuracy_score(y_test, predict_nb) * 100
        print(naivebayes)
        print(confusion_matrix(y_test, predict_nb))
        print(classification_report(y_test, predict_nb))
        models.append(('naive_bayes', NB))


        # SVM Model
        print("SVM")
        from sklearn import svm

        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))


        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression

        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))

        print("Decision Tree Classifier")
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        dtcpredict = dtc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, dtcpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, dtcpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, dtcpredict))
        models.append(('DecisionTreeClassifier', dtc))


        print("SGD Classifier")
        from sklearn.linear_model import SGDClassifier
        sgd_clf = SGDClassifier(loss='hinge', penalty='l2', random_state=0)
        sgd_clf.fit(X_train, y_train)
        sgdpredict = sgd_clf.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, sgdpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, sgdpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, sgdpredict))
        models.append(('SGDClassifier', sgd_clf))


        print("KNeighborsClassifier")
        from sklearn.neighbors import KNeighborsClassifier
        kn = KNeighborsClassifier()
        kn.fit(X_train, y_train)
        knpredict = kn.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, knpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, knpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, knpredict))
        models.append(('KNeighborsClassifier', kn))


        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)


        data = [Name_of_Covered_Entity]
        vector1 = cv.transform(data).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if prediction == 0:
            val = 'Theft'
        elif prediction == 1:
            val = 'Loss'
        elif prediction == 2:
            val = 'Disclosure'
        elif prediction == 3:
            val = 'Hacking'
        elif prediction == 4:
            val = 'Improper Disposal'
        print(prediction)
        print(val)

        Cyber_model.objects.create(Name_of_Covered_Entity=Name_of_Covered_Entity,
State=State,
Individuals_Affected=Individuals_Affected,
Date_of_Breach=Date_of_Breach,
Location_of_Breached_Information=Location_of_Breached_Information,
Date_Posted_or_Updated=Date_Posted_or_Updated,
breach_start=breach_start,
year=year,
Source_Ip=Source_Ip,
Destination_Ip=Destination_Ip,
Prediction=val)

        return render(request, 'RUser/Predict_CyberThreat_Type.html',{'objs': val})
    return render(request, 'RUser/Predict_CyberThreat_Type.html')



