
from django.contrib.staticfiles.storage import staticfiles_storage

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import pandas as pd
import numpy as np
import os.path
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
# Create your views here.
from django.contrib.staticfiles import finders
@method_decorator(csrf_exempt, name='dispatch')
class Predict(View):
    def get(self, reqeust, model_number):

        ctx = {
            'model' : model_number,
            'state' : 'get',
            'view' : self.__class__.__name__,
        }

        if model_number == '1':
            return JsonResponse(ctx, status=200)
        elif model_number == '2':
            return JsonResponse(ctx, status=200)

        elif model_number == '3':
            return JsonResponse(ctx, status=200)

        elif model_number == '4':
            return JsonResponse(ctx, status=200)
        else:
            return JsonResponse({'MESSAGE': 'Model doesn\'t exist!'}, status=400)


    def post(self, request, model_number):
        try:

            # age = data['age']
            # sex =

            # {'AGE': [30], 'SEX': [1], 'BMI': [3], 'SBP': [3], 'DBP': [3], 'HRI': [100], 'TEMPI': [39],
            #  'ACC': [1], 'SOB': [1], 'DEMEN': [1],
            #  'DM': [1], 'HTN': [1],
            #  'HCT': [20], 'LYMPHO': [20], 'HGB': [20], 'PLT': [20000], 'WBC': [6000]}
            ctx = {
                'model': model_number,
                'state': 'post',
                'view' : self.__class__.__name__,

            }
            # return JsonResponse(ctx, status=200)

            if model_number == '1':
                return model1(request)
            elif model_number == '2':
                return model2(request)
            elif model_number == '3':
                # data = {key: request.POST.get(key) for key in ('AGE', 'SEX', 'BMI', 'SBP', 'DBP', 'HRI', 'TEMPI', 'ACC',
                #                                                'SOB', 'DEMEN', 'DM', 'HTN', 'HCT', 'LYMPHO', 'HGB',
                #                                                'PLT', 'WBC')}
                #
                # for k, v in data.items():
                #     data[k] = float(v)
                #
                # return JsonResponse(data, status=200)
                # data = {"lat": 20.586, "lon": -89.530}
                # data = json.loads(request.body)
                # post_data = {key: request.POST.get(key) for key in ('AGE', 'SEX', 'BMI')}
                # return JsonResponse(post_data, status=200)
                # return JsonResponse(json.loads(request.body))
                return model3(request)
            elif model_number == '4':
                return model4(request)
            else:
                return JsonResponse({'MESSAGE': 'Model doesn\'t exist!'}, status=400)


        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'}, status=400)



class TestView(View):
    def get(self, request):

        return test_print(request)




class TestView(View):
    def get(self, request):

        return test_print(request)

# class UserView(APIView):
#     """
#     POST /user
#     """
#
#     def post(self, request):
#         return Response("test ok", status=200)
#
#     """
#     GET /user
#     GET /user/{user_id}
#     """
#
#     def get(self, request):
#         return Response("test ok", status=200)
#
#     """
#     PUT /user/{user_id}
#     """
#
#     def put(self, request):
#         return Response("test ok", status=200)
#
#     """
#     DELETE /user/{user_id}
#     """
#
#     def delete(self, request):
#         return Response("test ok", status=200)


class AboutView(TemplateView):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        ctx = {
            'view' : self.__class__.__name__
        }
        return self.render_to_response(ctx)

def test_print(request):
    return HttpResponse('test print')

def index(request):
    url = static('csv/ModelRules_3.csv')
    isfile = os.path.isfile(url)
    return HttpResponse(isfile)

@csrf_exempt
def post_test(request):

    if request.method == 'POST':
        age = request.POST.get('age')
        sex = request.POST.get('sex')

    data = {}
    data['age'] = age
    data['sex'] = sex

    json_data = json.dumps(data)
    return HttpResponse(json_data)

def test(request):

    if request.method == 'GET':
        age = request.GET.get('age')
        sex = request.GET.get('sex')

    data = {}
    data['age'] = age
    data['sex'] = sex

    json_data = json.dumps(data)
    return HttpResponse(json_data)


def model4(request):
    # result = finders.find('csv/ModelRules_3.csv')
    # data = json.loads(request.body)
    # data = request.POST.get


    data = {key: request.POST.get(key) for key in ('AGE', 'SEX', 'BMI', 'SBP', 'DBP', 'HRI', 'TEMPI',
                                                   'SOB', 'DEMEN', 'DM', 'HTN')}
    for k, v in data.items():
        data[k] = to_number(v)

    # Age                   AGE /
    # Shortnessofbreath     SOB /
    # Bodymassindex         BMI /
    # Sex                   SEX /
    # Bodytemperature       TEMPI /
    # Heartrate             HRI /
    # Hypertension          HTN
    # Systolicbloodpressure SBP /
    # Diabetesmellitus      DM
    # Dementia              DEMEN
    # Diastolicbloodpressure    DBP /

    AllRules = pd.read_csv(staticfiles_storage.path('csv/ModelRules_4.csv'))  # Rule(Query) 와 각 rule에 해당하는 점수(Quality)

    patient = pd.DataFrame({'AGE': [data['AGE']], 'SEX': [data['SEX']], 'BMI': [data['BMI']],
                            'SBP': [data['SBP']], 'DBP': [data['DBP']], 'HRI': [data['HRI']],
                            'TEMPI': [data['TEMPI']],  'SOB': [data['SOB']],
                            'DEMEN': [data['DEMEN']], 'DM': [data['DM']], 'HTN': [data['HTN']],
                           })

    def xgb_predict(AllRules, patientInfo):
        tree_lst = []

        for i in range(len(AllRules)):
            Tree = len(patientInfo.query(AllRules.RuleText[i]))
            tree_lst.append(Tree)

        AllRules['idx'] = tree_lst

        Q = AllRules.loc[AllRules['idx'] == 1].Quality.sum()
        pred_prob = np.exp(Q) / (1 + np.exp(Q))

        return pred_prob


    xgb_predict(AllRules, patient)

    result = 'Predicted Probaility:: ' + str(round(xgb_predict(AllRules, patient) * 100, 3)) + '%'
    return JsonResponse({'result': str(round(xgb_predict(AllRules, patient) * 100, 3)) + '%'}, status=200)

def model3(request):
    # result = finders.find('csv/ModelRules_3.csv')
    # data = json.loads(request.body)
    # data = request.POST.get


    data = {key: request.POST.get(key) for key in ('AGE', 'SEX', 'BMI', 'SBP', 'DBP', 'HRI', 'TEMPI', 'ACC', 'SOB', 'DEMEN', 'DM', 'HTN', 'HCT', 'LYMPHO', 'HGB', 'PLT', 'WBC')}
    for k, v in data.items():
        data[k] = to_number(v)






    AllRules = pd.read_csv(staticfiles_storage.path('csv/ModelRules_3.csv'))  # Rule(Query) 와 각 rule에 해당하는 점수(Quality)

    patient = pd.DataFrame({'AGE': [data['AGE']], 'SEX': [data['SEX']], 'BMI': [data['BMI']], 'SBP': [data['SBP']], 'DBP': [data['DBP']], 'HRI': [data['HRI']], 'TEMPI': [data['TEMPI']], 'ACC': [data['ACC']], 'SOB': [data['SOB']], 'DEMEN': [data['DEMEN']], 'DM': [data['DM']], 'HTN': [data['HTN']], 'HCT': [data['HCT']], 'LYMPHO': [data['LYMPHO']], 'HGB': [data['HGB']], 'PLT': [data['PLT']], 'WBC': [data['WBC']]})




    xgb_predict(AllRules, patient)

    result = 'Predicted Probaility:: ' + str(round(xgb_predict(AllRules, patient) * 100, 3)) + '%'
    return JsonResponse({'result': str(round(xgb_predict(AllRules, patient) * 100, 3)) + '%'}, status=200)
    # return HttpResponse('Predicted Probaility:: ' + str(round(xgb_predict(AllRules, patient) * 100, 3)) + '%')


def model2(request):
    # Age                       AGE /
    # Shortness of breath       SOB /
    # Body mass index           BMI /
    # Sex                       SEX /
    # Body temperature          TEMPI   /
    # Heart rate                HRI /
    # Hypertension              HTN /
    # Systolic blood pressure   SBP /
    # Diabetes mellitus         DM  /
    # Dementia                  DEMEN   /
    # Diastolic blood pressure  DBP /
    # Rhinorrhea                RNR /
    # Fever                     FEVER   - 1/0 /
    # Cough                     COUGH   - 1/0 /
    # Headache                  HEADA   - 1/0 /
    # Sore throat               ST      - 1/0 /
    # Altered consciousness     ACC     /
    # Malignancy                MALIG    - 1/0 /
    # Sputum                    SPUTUM  - 1/0   /
    # Myalgia                   MAM         - 1/0   /
    # Cardiovascular disease    CCD     - 1/0   /
    # Chronic kidney disease    CKD      - 1/0 /
    # Diarrhea                  DIARR   - 1/0 /
    # Vomiting                  VN      - 1/0 /
    # Chronic liver disease     CLD     - 1/0 /
    # Fatigue                   FM      - 1/0
    # Asthma                    ASTHMA  - 1/0
    # Heart failure             HF      - 1/0
    # Chronic obstructive pulmonary disease     COPD    - 1/0
    # Autoimmune disease        RDAD  - 1/0 (2 > 있음 확인필요)
    # Pregnancy                 PREG
    # Pregnancy Weeks           PREGGW

    # result = finders.find('csv/ModelRules_3.csv')
    # data = json.loads(request.body)
    # data = request.POST.get


    data = {key: request.POST.get(key) for key in ('AGE', 'SEX', 'BMI', 'SBP', 'DBP', 'HRI', 'TEMPI', 'ACC',
                                                   'SOB', 'DEMEN', 'DM', 'HTN', 'RNR',
                                                   'FEVER', 'COUGH', 'HEADA', 'ST', 'MALIG', 'SPUTUM', 'MAM',
                                                   'CCD', 'CKD', 'DIARR', 'VN', 'CLD', 'FM', 'ASTHMA', 'HF',
                                                   'COPD', 'RDAD', 'PREGGW')}
    for k, v in data.items():
        data[k] = to_number(v)






    AllRules = pd.read_csv(staticfiles_storage.path('csv/ModelRules_2.csv'))  # Rule(Query) 와 각 rule에 해당하는 점수(Quality)

    patient = pd.DataFrame({'AGE': [data['AGE']], 'SEX': [data['SEX']], 'BMI': [data['BMI']],
                            'SBP': [data['SBP']], 'DBP': [data['DBP']], 'HRI': [data['HRI']],
                            'TEMPI': [data['TEMPI']], 'ACC': [data['ACC']], 'SOB': [data['SOB']],
                            'DEMEN': [data['DEMEN']], 'DM': [data['DM']], 'HTN': [data['HTN']],
                            'RNR': [data['RNR']], 'FEVER': [data['FEVER']], 'COUGH': [data['COUGH']],
                            'HEADA': [data['HEADA']], 'ST': [data['ST']],  'MALIG': [data['MALIG']],
                            'SPUTUM': [data['SPUTUM']], 'MAM': [data['MAM']], 'CCD': [data['CCD']],
                            'CKD': [data['CKD']], 'DIARR': [data['DIARR']],  'VN': [data['VN']],
                            'CLD': [data['CLD']], 'FM': [data['FM']], 'ASTHMA': [data['ASTHMA']],
                            'HF': [data['HF']], 'COPD': [data['COPD']], 'RDAD': [data['RDAD']],
                            'PREGGW': [data['PREGGW']],
                            })




    xgb_predict(AllRules, patient)

    result = 'Predicted Probaility:: ' + str(round(xgb_predict(AllRules, patient) * 100, 3)) + '%'
    return JsonResponse({'result': str(round(xgb_predict(AllRules, patient) * 100, 3)) + '%'}, status=200)



def model1(request):
    # Age                       AGE /
    # Shortness of breath       SOB /
    # Body mass index           BMI /
    # Sex                       SEX /
    # Body temperature          TEMPI   /
    # Heart rate                HRI /
    # Hypertension              HTN /
    # Systolic blood pressure   SBP /
    # Diabetes mellitus         DM  /
    # Dementia                  DEMEN   /
    # Diastolic blood pressure  DBP /
    # Rhinorrhea                RNR /
    # Fever                     FEVER   - 1/0 /
    # Cough                     COUGH   - 1/0 /
    # Headache                  HEADA   - 1/0 /
    # Sore throat               ST      - 1/0 /
    # Altered consciousness     ACC     /
    # Malignancy                MALIG    - 1/0 /
    # Sputum                    SPUTUM  - 1/0   /
    # Myalgia                   MAM         - 1/0   /
    # Cardiovascular disease    CCD     - 1/0   /
    # Chronic kidney disease    CKD      - 1/0 /
    # Diarrhea                  DIARR   - 1/0 /
    # Vomiting                  VN      - 1/0 /
    # Chronic liver disease     CLD     - 1/0 /
    # Fatigue                   FM      - 1/0
    # Asthma                    ASTHMA  - 1/0
    # Heart failure             HF      - 1/0
    # Chronic obstructive pulmonary disease     COPD    - 1/0
    # Autoimmune disease        RDAD  - 1/0 (2 > 있음 확인필요)
    # Pregnancy                 PREG
    # Pregnancy Weeks           PREGGW

    # 'HCT': [20], 'LYMPHO': [20], 'HGB': [20], 'PLT': [20000], 'WBC': [6000]


    # result = finders.find('csv/ModelRules_3.csv')
    # data = json.loads(request.body)
    # data = request.POST.get


    data = {key: request.POST.get(key) for key in ('AGE', 'SEX', 'BMI', 'SBP', 'DBP', 'HRI', 'TEMPI', 'ACC',
                                                   'SOB', 'DEMEN', 'DM', 'HTN', 'RNR',
                                                   'FEVER', 'COUGH', 'HEADA', 'ST', 'MALIG', 'SPUTUM', 'MAM',
                                                   'CCD', 'CKD', 'DIARR', 'VN', 'CLD', 'FM', 'ASTHMA', 'HF',
                                                   'COPD', 'RDAD', 'PREGGW',  'HCT', 'LYMPHO', 'HGB', 'PLT', 'WBC')}
    for k, v in data.items():
        data[k] = to_number(v)






    AllRules = pd.read_csv(staticfiles_storage.path('csv/ModelRules_1.csv'))  # Rule(Query) 와 각 rule에 해당하는 점수(Quality)

    patient = pd.DataFrame({'AGE': [data['AGE']], 'SEX': [data['SEX']], 'BMI': [data['BMI']],
                            'SBP': [data['SBP']], 'DBP': [data['DBP']], 'HRI': [data['HRI']],
                            'TEMPI': [data['TEMPI']], 'ACC': [data['ACC']], 'SOB': [data['SOB']],
                            'DEMEN': [data['DEMEN']], 'DM': [data['DM']], 'HTN': [data['HTN']],
                            'RNR': [data['RNR']], 'FEVER': [data['FEVER']], 'COUGH': [data['COUGH']],
                            'HEADA': [data['HEADA']], 'ST': [data['ST']],  'MALIG': [data['MALIG']],
                            'SPUTUM': [data['SPUTUM']], 'MAM': [data['MAM']], 'CCD': [data['CCD']],
                            'CKD': [data['CKD']], 'DIARR': [data['DIARR']],  'VN': [data['VN']],
                            'CLD': [data['CLD']], 'FM': [data['FM']], 'ASTHMA': [data['ASTHMA']],
                            'HF': [data['HF']], 'COPD': [data['COPD']], 'RDAD': [data['RDAD']],
                            'PREGGW': [data['PREGGW']],
                            'HCT': [data['HCT']], 'LYMPHO': [data['LYMPHO']], 'HGB': [data['HGB']], 'PLT': [data['PLT']], 'WBC': [data['WBC']]
                            })




    xgb_predict(AllRules, patient)

    result = 'Predicted Probaility:: ' + str(round(xgb_predict(AllRules, patient) * 100, 3)) + '%'
    return JsonResponse({'result': str(round(xgb_predict(AllRules, patient) * 100, 3)) + '%'}, status=200)

def xgb_predict(AllRules, patientInfo):
        tree_lst = []

        for i in range(len(AllRules)):
            Tree = len(patientInfo.query(AllRules.RuleText[i]))
            tree_lst.append(Tree)

        AllRules['idx'] = tree_lst

        Q = AllRules.loc[AllRules['idx'] == 1].Quality.sum()
        pred_prob = np.exp(Q) / (1 + np.exp(Q))

        return pred_prob

def model3_test(request):
    # result = finders.find('csv/ModelRules_3.csv')

    if request.method == 'POST':
        title = request.POST.get('AGE')
        content = request.POST.get('SEX')




    AllRules = pd.read_csv(staticfiles_storage.path('csv/ModelRules_3.csv'))  # Rule(Query) 와 각 rule에 해당하는 점수(Quality)



    patient = pd.DataFrame({'AGE': [30], 'SEX': [1], 'BMI': [3], 'SBP': [3], 'DBP': [3], 'HRI': [100], 'TEMPI': [39],
                            'ACC': [1], 'SOB': [1], 'DEMEN': [1],
                            'DM': [1], 'HTN': [1],
                            'HCT': [20], 'LYMPHO': [20], 'HGB': [20], 'PLT': [20000], 'WBC': [6000]})

    def xgb_predict(AllRules, patientInfo):
        tree_lst = []

        for i in range(len(AllRules)):
            Tree = len(patientInfo.query(AllRules.RuleText[i]))
            tree_lst.append(Tree)

        AllRules['idx'] = tree_lst

        Q = AllRules.loc[AllRules['idx'] == 1].Quality.sum()
        pred_prob = np.exp(Q) / (1 + np.exp(Q))

        return pred_prob


    xgb_predict(AllRules, patient)

    return HttpResponse('Predicted Probaility:: ' + str(round(xgb_predict(AllRules, patient) * 100, 3)) + '%')



def model3_test(request):
    # result = finders.find('csv/ModelRules_3.csv')
    AllRules = pd.read_csv(staticfiles_storage.path('csv/ModelRules_3.csv'))  # Rule(Query) 와 각 rule에 해당하는 점수(Quality)



    patient = pd.DataFrame({'AGE': [30], 'SEX': [1], 'BMI': [3], 'SBP': [3], 'DBP': [3], 'HRI': [100], 'TEMPI': [39],
                            'ACC': [1], 'SOB': [1], 'DEMEN': [1],
                            'DM': [1], 'HTN': [1],
                            'HCT': [20], 'LYMPHO': [20], 'HGB': [20], 'PLT': [20000], 'WBC': [6000]})

    def xgb_predict(AllRules, patientInfo):
        tree_lst = []

        for i in range(len(AllRules)):
            Tree = len(patientInfo.query(AllRules.RuleText[i]))
            tree_lst.append(Tree)

        AllRules['idx'] = tree_lst

        Q = AllRules.loc[AllRules['idx'] == 1].Quality.sum()
        pred_prob = np.exp(Q) / (1 + np.exp(Q))

        return pred_prob


    xgb_predict(AllRules, patient)

    return HttpResponse('Predicted Probaility:: ' + str(round(xgb_predict(AllRules, patient) * 100, 3)) + '%')


def to_number(n):
    ''' Convert any number representation to a number
    This covers: float, decimal, hex, and octal numbers.
    '''

    try:
        return int(str(n), 0)
    except:
        try:
            # python 3 doesn't accept "010" as a valid octal.  You must use the
            # '0o' prefix
            return int('0o' + n, 0)
        except:
            return float(n)

# Manuscript.docx
# Table 1. Demographics and clinical characteristics by cohort. 참고

# sex
# male : 0
# female : 1

# age
# 1 : 0 - 9
# 2 : 10 - 19
# 3 : 20 - 29
# 4 : 30 - 39
# 5 : 40 - 49
# 6 : 50 - 59
# 7 : 60 - 69
# 8 : 70 - 79
# 9 : ≥ 80


# BMI
# 1: < 18.5
# 2: 18.5 - 22.9
# 3: 23.0 - 24.9
# 4: 25.0 - 29.9
# 5: ≥ 30


# SBP
# 1: < 120
# 2: 120 - 129
# 3: 130 - 139
# 4: 140 - 159
# 5: ≥ 160


# DBP
# 1: < 80
# 2: 80 - 89
# 3: 90 - 99
# 4: ≥ 100