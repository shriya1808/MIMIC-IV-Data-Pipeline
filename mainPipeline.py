
#import ipywidgets as widgets
from pathlib import Path
import os
import numpy as np
import argparse
#import nltk

import sys

module_path = 'preprocessing/day_intervals_preproc'
if module_path not in sys.path:
    sys.path.append(module_path)
module_path = 'utils'
if module_path not in sys.path:
    sys.path.append(module_path)

module_path = 'preprocessing'
if module_path not in sys.path:
    sys.path.append(module_path)

module_path = 'preprocessing/hosp_module_preproc'
if module_path not in sys.path:
    sys.path.append(module_path)

module_path = 'model'
if module_path not in sys.path:
    sys.path.append(module_path)
#print(sys.path)

parser = argparse.ArgumentParser(description="MIMIC-IV Data Pipeline")
parser.add_argument(
    "--workdir",
    type=str,
    required=True,
    help="Working directory for the pipeline"
)
args = parser.parse_args()

root_dir = os.path.dirname(args.workdir)
print(os.getcwd())

import day_intervals_cohort
from day_intervals_cohort import *

import day_intervals_cohort_v2
from day_intervals_cohort_v2 import *

import day_intervals_cohort_v3
from day_intervals_cohort_v3 import *

import notes_preproc
from notes_preproc import *

import data_generation_icu

import data_generation
import evaluation

import feature_selection_hosp
from feature_selection_hosp import *

# import train
# from train import *

# import ml_models
# from ml_models import *

# import dl_train
# from dl_train import *

import tokenization
from tokenization import *

# import behrt_train
# from behrt_train import *

import feature_selection_icu
from feature_selection_icu import *
import fairness
import callibrate_output

importlib.reload(day_intervals_cohort)
import day_intervals_cohort
from day_intervals_cohort import *

importlib.reload(day_intervals_cohort_v2)
import day_intervals_cohort_v2
from day_intervals_cohort_v2 import *

importlib.reload(day_intervals_cohort_v3)
import day_intervals_cohort_v3
from day_intervals_cohort_v3 import *

importlib.reload(data_generation_icu)
import data_generation_icu

importlib.reload(data_generation)
import data_generation

importlib.reload(feature_selection_hosp)
import feature_selection_hosp
from feature_selection_hosp import *

importlib.reload(feature_selection_icu)
import feature_selection_icu
from feature_selection_icu import *

importlib.reload(tokenization)
import tokenization
from tokenization import *

# importlib.reload(ml_models)
# import ml_models
# from ml_models import *

# importlib.reload(dl_train)
# import dl_train
# from dl_train import *

# importlib.reload(behrt_train)
# import behrt_train
# from behrt_train import *

importlib.reload(fairness)
import fairness

importlib.reload(callibrate_output)
import callibrate_output

importlib.reload(evaluation)
import evaluation

print("Finished importing.")







############## Data Extraction################
print("Please select the approriate version of MIMIC-IV for which you have downloaded data ?")
# version = widgets.RadioButtons(options=['Version 1','Version 2', 'Version 3', 'Notes'],value='Version 3')
version = 'Version 3'
print(version)


print("Please select what prediction task you want to perform ?")
# radio_input4 = widgets.RadioButtons(options=['Mortality','Length of Stay','Readmission','Phenotype'],value='Readmission')
radio_input4 = 'Readmission'
print(radio_input4)




if version == 'Notes':
    print ('What file ?')
    # notes_sec = widgets.RadioButtons(options=['Discharge', 'Radiology'], value='Discharge')
    notes_sec = 'Discharge'
    print(notes_sec)
    print('What NLP would you like with Notes ?')
    # notes_pred = widgets.RadioButtons(options=['Section Splitting', 'Negation Detection'], value='Section Splitting')
    notes_pred = 'Section Splitting'
    print(notes_pred)
    
if radio_input4 =='Length of Stay':
    # radio_input2 = widgets.RadioButtons(options=['Length of Stay ge 3','Length of Stay ge 7','Custom'],value='Length of Stay ge 3')
    radio_input2 = 'Length of Stay ge 3'
    print(radio_input2)

elif radio_input4 =='Readmission':
    # radio_input2 = widgets.RadioButtons(options=['30 Day Readmission','60 Day Readmission','90 Day Readmission','120 Day Readmission','Custom'],value='30 Day Readmission')
    radio_input2 = '30 Day Readmission'
    print(radio_input2)

elif radio_input4.value=='Phenotype':
    # radio_input2 = widgets.RadioButtons(options=['Heart Failure in 30 days','CAD in 30 days','CKD in 30 days','COPD in 30 days'],value='Heart Failure in 30 days')
    radio_input2 = 'Heart Failure in 30 days'
    print(radio_input2)
elif radio_input4.value=='Mortality':
    # radio_input2 = widgets.RadioButtons(options=['Mortality'],value='Mortality')
    radio_input2 = 'Mortality'
    #print(radio_input2)

print("Extract Data")
print("Please select below if you want to work with ICU or Non-ICU data ?")
# radio_input1 = widgets.RadioButtons(options=['ICU', 'Non-ICU'],value='Non-ICU')
radio_input1 = 'Non-ICU'
print(radio_input1)

print("Please select if you want to perform choosen prediction task for a specific disease.")
# radio_input3 = widgets.RadioButtons(options=['No Disease Filter','Heart Failure','CKD','CAD','COPD'],value='No Disease Filter')
radio_input3 = 'No Disease Filter'
print(radio_input3)







disease_label=""
time=0
label=radio_input4

if label=='Readmission':
    time=int(radio_input2.split()[0])

elif label=='Length of Stay':
    time=int(radio_input2.split()[4])

if label=='Phenotype':    
    if radio_input2=='Heart Failure in 30 days':
        label='Readmission'
        time=30
        disease_label='I50'
    elif radio_input2=='CAD in 30 days':
        label='Readmission'
        time=30
        disease_label='I25'
    elif radio_input2=='CKD in 30 days':
        label='Readmission'
        time=30
        disease_label='N18'
    elif radio_input2=='COPD in 30 days':
        label='Readmission'
        time=30
        disease_label='J44'
    
data_icu=radio_input1=="ICU"
data_mort=label=="Mortality"
data_admn=label=='Readmission'
data_los=label=='Length of Stay'
        

if (radio_input3=="Heart Failure"):
    icd_code='I50'
elif (radio_input3=="CKD"):
    icd_code='N18'
elif (radio_input3=="COPD"):
    icd_code='J44'
elif (radio_input3=="CAD"):
    icd_code='I25'
else:
    icd_code='No Disease Filter'

if version=='Version 1':
    version_path="mimiciv/1.0"
    cohort_output = day_intervals_cohort.extract_data(radio_input1,label,time,icd_code, root_dir,disease_label)
elif version=='Version 2':
    version_path="mimiciv/2.0"
    cohort_output = day_intervals_cohort_v2.extract_data(radio_input1,label,time,icd_code, root_dir,disease_label)
elif version=='Version 3':
    version_path="mimicv/3.1"
    # cohort_output = "cohort_non-icu_readmission_30_"
    cohort_output = day_intervals_cohort_v3.extract_data(radio_input1,label,time,icd_code, root_dir,disease_label)
elif version=='Notes':
    version_path='mimiciv/notes'
    nlp_output = notes_preproc.extract_data(notes_sec, notes_pred)














################# Feature Selection ################
print("Feature Selection")
if data_icu:
    print("Which Features you want to include for cohort?")
    # check_input1 = widgets.Checkbox(description='Diagnosis', value=True)
    check_input1 = True
    print(check_input1)
    # check_input2 = widgets.Checkbox(description='Output Events', value=True)
    check_input2 = True
    print(check_input2)
    # check_input3 = widgets.Checkbox(description='Chart Events(Labs and Vitals)', value=True)
    check_input3 = True
    print(check_input3)
    check_input4 = True
    # check_input4 = widgets.Checkbox(description='Procedures', value=True)
    print(check_input4)
    # check_input5 = widgets.Checkbox(description='Medications', value=True)
    check_input5 = True
    print(check_input5)

elif version == "Notes":
    print("Which Features you want to include for cohort ?")
    check_input1 = True
    check_input2 = True
    check_input3 = True
    check_input4 = True
    check_input5 = True
    # check_input1 = widgets.CheckBox(description='Diagnosis', value=True)
    print(check_input1)
    # check_input2 = widgets.Checkbox(description='Medical History', value=True)
    print(check_input2)
    # check_input3 = widgets.Checkbox(description='Family Medical History', value=True)
    print(check_input3)
    # check_input4 = widgets.Checkbox(description='History of Drug Use', value=True)
    print(check_input4)
    # check_input5 = widgets.Checkbox(description='History of Mental Illness', value=True)
    print(check_input5)
    
else:
    print("Which Features you want to include for cohort?")
    check_input1 = True
    check_input2 = False
    check_input3 = True
    check_input4 = True
    # check_input1 = widgets.Checkbox(description='Diagnosis', value=True)
    print(check_input1)
    # check_input2 = widgets.Checkbox(description='Labs', value=False)
    print(check_input2)
    # check_input3 = widgets.Checkbox(description='Procedures', value=True)
    print(check_input3)
    # check_input4 = widgets.Checkbox(description='Medications', value=True)
    print(check_input4)
print("**Please run below cell to extract selected features**")





if data_icu:
    diag_flag=check_input1
    out_flag=check_input2
    chart_flag=check_input3
    proc_flag=check_input4
    med_flag=check_input5
    feature_icu(cohort_output, version_path,diag_flag,out_flag,chart_flag,proc_flag,med_flag)
elif version.value == "Notes":
    diag_flag = check_input1
    med_hist = check_input2
    f_med_hist = check_input3
    hist_drug = check_input4
    hist_mi = check_input5
    feature_notes(diag_flag, med_hist, f_med_hist, hist_drug, hist_mi)
    
else:
    diag_flag=check_input1
    lab_flag=check_input2
    proc_flag=check_input3
    med_flag=check_input4
    feature_nonicu(cohort_output, version_path,diag_flag,lab_flag,proc_flag,med_flag)
















########## Clinical Grouping ###################
if data_icu:
    if diag_flag:
        print("Do you want to group ICD 10 DIAG codes ?")
        # radio_input4 = widgets.RadioButtons(options=['Keep both ICD-9 and ICD-10 codes','Convert ICD-9 to ICD-10 codes','Convert ICD-9 to ICD-10 and group ICD-10 codes'],value='Convert ICD-9 to ICD-10 and group ICD-10 codes',layout={'width': '100%'})
        radio_input4 = 'Convert ICD-9 to ICD-10 and group ICD-10 codes'
        print(radio_input4)   
    
else:
    if diag_flag:
        print("Do you want to group ICD 10 DIAG codes ?")
        # radio_input4 = widgets.RadioButtons(options=['Keep both ICD-9 and ICD-10 codes','Convert ICD-9 to ICD-10 codes','Convert ICD-9 to ICD-10 and group ICD-10 codes'],value='Convert ICD-9 to ICD-10 and group ICD-10 codes',layout={'width': '100%'})
        radio_input4 = 'Convert ICD-9 to ICD-10 and group ICD-10 codes'
        print(radio_input4)     
    if med_flag:
        print("Do you want to group Medication codes to use Non propietary names?")
        # radio_input5 = widgets.RadioButtons(options=['Yes','No'],value='Yes',layout={'width': '100%'})
        radio_input5 = 'Yes'
        print(radio_input5)
    if proc_flag:
        print("Which ICD codes for Procedures you want to keep in data?")
        # radio_input6 = widgets.RadioButtons(options=['ICD-9 and ICD-10','ICD-10'],value='ICD-10',layout={'width': '100%'})
        radio_input6 = 'ICD-10'
        print(radio_input6)
print("**Please run below cell to perform feature preprocessing**")




group_diag=False
group_med=False
group_proc=False
if data_icu:
    if diag_flag:
        group_diag=radio_input4
    preprocess_features_icu(cohort_output, diag_flag, group_diag,False,False,False,0,0)
else:
    if diag_flag:
        group_diag=radio_input4
    if med_flag:
        group_med=radio_input5
    if proc_flag:
        group_proc=radio_input6
    preprocess_features_hosp(cohort_output, diag_flag,proc_flag,med_flag,False,group_diag,group_med,group_proc,False,False,0,0)











################ Summary Of Features ##############
if data_icu:
    generate_summary_icu(diag_flag,proc_flag,med_flag,out_flag,chart_flag)
else:
    generate_summary_hosp(diag_flag,proc_flag,med_flag,lab_flag)










#############Feature Selection #################
if data_icu:
    if diag_flag:
        print("Do you want to do Feature Selection for Diagnosis \n (If yes, please edit list of codes in ./data/summary/diag_features.csv)")
        # radio_input4 = widgets.RadioButtons(options=['Yes','No'],value='No')
        radio_input4 = 'No'
        print(radio_input4)       
    if med_flag:
        print("Do you want to do Feature Selection for Medication \n (If yes, please edit list of codes in ./data/summary/med_features.csv)")
        # radio_input5 = widgets.RadioButtons(options=['Yes','No'],value='No')
        radio_input5 = 'No'
        print(radio_input5)   
    if proc_flag:
        print("Do you want to do Feature Selection for Procedures \n (If yes, please edit list of codes in ./data/summary/proc_features.csv)")
        # radio_input6 = widgets.RadioButtons(options=['Yes','No'],value='No')
        radio_input6 = 'No'
        print(radio_input6)   
    if out_flag:
        print("Do you want to do Feature Selection for Output event \n (If yes, please edit list of codes in ./data/summary/out_features.csv)")
        # radio_input7 = widgets.RadioButtons(options=['Yes','No'],value='No')
        radio_input7 = 'No'
        print(radio_input7)  
    if chart_flag:
        print("Do you want to do Feature Selection for Chart events \n (If yes, please edit list of codes in ./data/summary/chart_features.csv)")
        # radio_input8 = widgets.RadioButtons(options=['Yes','No'],value='No')
        radio_input8 = 'No'
        print(radio_input8)  
else:
    if diag_flag:
        print("Do you want to do Feature Selection for Diagnosis \n (If yes, please edit list of codes in ./data/summary/diag_features.csv)")
        # radio_input4 = widgets.RadioButtons(options=['Yes','No'],value='No')
        radio_input4
        print(radio_input4)         
    if med_flag:
        print("Do you want to do Feature Selection for Medication \n (If yes, please edit list of codes in ./data/summary/med_features.csv)")
        # radio_input5 = widgets.RadioButtons(options=['Yes','No'],value='No')
        radio_input5 = 'No'
        print(radio_input5)   
    if proc_flag:
        print("Do you want to do Feature Selection for Procedures \n (If yes, please edit list of codes in ./data/summary/proc_features.csv)")
        # radio_input6 = widgets.RadioButtons(options=['Yes','No'],value='No')
        radio_input6 = 'No'
        print(radio_input6)   
    if lab_flag:
        print("Do you want to do Feature Selection for Labs \n (If yes, please edit list of codes in ./data/summary/lab_features.csv)")
        # radio_input7 = widgets.RadioButtons(options=['Yes','No'],value='No')
        radio_input7 = 'No'
        print(radio_input7)   
print("**Please run below cell to perform feature selection**")





select_diag=False
select_med=False
select_proc=False
select_lab=False
select_out=False
select_chart=False

if data_icu:
    if diag_flag:
        select_diag=radio_input4 == 'Yes'
    if med_flag:
        select_med=radio_input5 == 'Yes'
    if proc_flag:
        select_proc=radio_input6 == 'Yes'
    if out_flag:
        select_out=radio_input7 == 'Yes'
    if chart_flag:
        select_chart=radio_input8 == 'Yes'
    features_selection_icu(cohort_output, diag_flag,proc_flag,med_flag,out_flag, chart_flag,select_diag,select_med,select_proc,select_out,select_chart)
else:
    if diag_flag:
        select_diag=radio_input4 == 'Yes'
    if med_flag:
        select_med=radio_input5 == 'Yes'
    if proc_flag:
        select_proc=radio_input6 == 'Yes'
    if lab_flag:
        select_lab=radio_input7 == 'Yes'
    features_selection_hosp(cohort_output, diag_flag,proc_flag,med_flag,lab_flag,select_diag,select_med,select_proc,select_lab)










###########Cleaning of Features ############
if data_icu:
    if chart_flag:
        print("Outlier removal in values of chart events ?")
        # layout = widgets.Layout(width='100%', height='40px') #set width and height

        # radio_input5 = widgets.RadioButtons(options=['No outlier detection','Impute Outlier (default:98)','Remove outliers (default:98)'],value='Remove outliers (default:98)',layout=layout)
        radio_input5 = 'Remove outliers (default:98)'
        print(radio_input5)
        left_outlier=0
        outlier=98
    
else:      
    if lab_flag:
        print("Outlier removal in values of lab events ?")
        # layout = widgets.Layout(width='100%', height='40px') #set width and height

        # radio_input7 = widgets.RadioButtons(options=['No outlier detection','Impute Outlier (default:98)','Remove outliers (default:98)'],value='Remove outliers (default:98)',layout=layout)
        radio_input7 = 'Remove outliers (default:98)'
        print(radio_input7)
        left_outlier=0
        outlier=98
print("**Please run below cell to perform feature preprocessing**")



thresh=0
if data_icu:
    if chart_flag:
        clean_chart=radio_input5!='No outlier detection'
        impute_outlier_chart=radio_input5=='Impute Outlier (default:98)'
        thresh=outlier
        left_thresh=left_outlier
        preprocess_features_icu(cohort_output, False, False,chart_flag,clean_chart,impute_outlier_chart,thresh,left_thresh)
else:
    if lab_flag:
        clean_lab=radio_input7!='No outlier detection'
        impute_outlier=radio_input7=='Impute Outlier (default:98)'
        thresh=outlier
        left_thresh=left_outlier
        preprocess_features_hosp(cohort_output, False,False,False,lab_flag,False,False,False,clean_lab,impute_outlier,thresh,left_thresh)











###############Time-Series Generation ##############
print("=======Time-series Data Represenation=======")

print("Length of data to be included for time-series prediction ?")
if(data_mort):
    # radio_input8 = widgets.RadioButtons(options=['First 72 hours','First 48 hours','First 24 hours','Custom'],value='First 72 hours')
    radio_input8 = 'First 72 hours'
    print(radio_input8)
    text2=72
elif(data_admn):
    # radio_input8 = widgets.RadioButtons(options=['Last 72 hours','Last 48 hours','Last 24 hours','Custom'],value='Last 72 hours')
    radio_input8 = 'Last 72 hours'
    print(radio_input8)
    text2=72
elif(data_los):
    # radio_input8 = widgets.RadioButtons(options=['First 12 hours','First 24 hours','Custom'],value='First 24 hours')
    radio_input8 = 'First 24 hours'
    print(radio_input8)
    text2=72
    
    
print("What time bucket size you want to choose ?")
radio_input7 = '2 hour' # widgets.RadioButtons(options=['1 hour','2 hour','3 hour','4 hour','5 hour','Custom'],value='2 hour')
print(radio_input7)
text1=1
#print(text1)
print("Do you want to forward fill and mean or median impute lab/chart values to form continuous data signal?")
# radio_impute = widgets.RadioButtons(options=['No Imputation', 'forward fill and mean','forward fill and median'],value='forward fill and median')
radio_impute = 'forward fill and median'
print(radio_impute)   

# radio_input6 = widgets.RadioButtons(options=['0 hours','2 hours','4 hours','6 hours'],value='2 hours')
radio_input6 = '2 hours'
if(data_mort):
    print("If you have choosen mortality prediction task, then what prediction window length you want to keep?")
    # radio_input6 = widgets.RadioButtons(options=['2 hours','4 hours','6 hours','8 hours','Custom'],value='2 hours')
    radio_input6 = '2 hours'
    print(radio_input6)
    text3=2
print("**Please run below cell to perform time-series represenation and save in data dictionaries**")





if (radio_input6=='Custom'):
    predW=int(text3)
else:
    predW=int(radio_input6[0].strip())
if (radio_input7=='Custom'):
    bucket=int(text1)
else:
    bucket=int(radio_input7[0].strip())
if (radio_input8=='Custom'):
    include=int(text2)
else:
    include=int(radio_input8.split()[1])
if (radio_impute=='forward fill and mean'):
    impute='Mean'
elif (radio_impute=='forward fill and median'):
    impute='Median'
else:
    impute=False

if data_icu:
    gen=data_generation_icu.Generator(cohort_output,data_mort,data_admn,data_los,diag_flag,proc_flag,out_flag,chart_flag,med_flag,impute,include,bucket,predW)
    #gen=data_generation_icu.Generator(cohort_output,data_mort,diag_flag,False,False,chart_flag,False,impute,include,bucket,predW)
    #if chart_flag:
    #    gen=data_generation_icu.Generator(cohort_output,data_mort,False,False,False,chart_flag,False,impute,include,bucket,predW)
else:
    gen=data_generation.Generator(cohort_output,data_mort,data_admn,data_los,diag_flag,lab_flag,proc_flag,med_flag,impute,include,bucket,predW)


