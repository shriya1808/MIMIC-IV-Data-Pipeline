import pandas as pd
import os
import sys

def generate_patient_features_csv(cohort_output_name):
    """
    Generates a CSV file with patient features (demographics + aggregated clinical codes)
    
    Args:
        cohort_output_name (str): The name of your cohort file inside ./data/cohort/ 
                                  (without .csv.gz extension). 
                                  Example: "cohort_non-icu_readmission_30_no_disease_filter"
    """
    
    # Define Paths
    cohort_path = f"./dataCKD/cohort/{cohort_output_name}.csv.gz"
    # cohort_path = f"./data/cohort/{cohort_output_name}.csv"
    diag_path = "./dataCKD/features/preproc_diag.csv.gz"
    proc_path = "./dataCKD/features/preproc_proc.csv.gz"
    med_path = "./dataCKD/features/preproc_med.csv.gz"
    lab_path = "./dataCKD/features/preproc_labs.csv.gz"
    
    output_filename = "patient_features_CKD.csv"

    # 1. Read Cohort Data (Base)
    print(f"[ READING COHORT ] {cohort_path}")
    if not os.path.exists(cohort_path):
        print(f"Error: Cohort file not found at {cohort_path}")
        return

    cohort = pd.read_csv(cohort_path, compression='gzip')
    # cohort = pd.read_csv(cohort_path)
    
    # Select and Rename Columns to match your requested format
    # Expecting columns: hadm_id, label, Age, gender, ethnicity
    required_cols = ['hadm_id', 'label', 'Age', 'gender', 'ethnicity']
    
    # Check if 'hadm_id' exists (Non-ICU), otherwise check for 'stay_id' (ICU) and rename
    if 'hadm_id' not in cohort.columns and 'stay_id' in cohort.columns:
        cohort = cohort.rename(columns={'stay_id': 'hadm_id'})
        
    cohort = cohort[required_cols].copy()
    cohort = cohort.rename(columns={'Age': 'age'}) # Rename Age -> age
    
    # 2. Process Diagnoses (Cond)
    print("[ PROCESSING DIAGNOSES ]")
    if os.path.exists(diag_path):
        diag = pd.read_csv(diag_path, compression='gzip')
        # Filter for patients in cohort
        diag = diag[diag['hadm_id'].isin(cohort['hadm_id'])]
        
        # Determine correct column name (based on feature_selection_hosp.py)
        icd_col = 'new_icd_code' if 'new_icd_code' in diag.columns else 'icd_code'
        
        # Aggregate into lists
        cond_grp = diag.groupby('hadm_id')[icd_col].apply(list).reset_index()
        cond_grp = cond_grp.rename(columns={icd_col: 'Cond'})
        
        # Merge
        cohort = cohort.merge(cond_grp, on='hadm_id', how='left')
    else:
        print("Warning: Diagnosis file not found.")
        cohort['Cond'] = None

    # 3. Process Procedures (Proc)
    print("[ PROCESSING PROCEDURES ]")
    if os.path.exists(proc_path):
        proc = pd.read_csv(proc_path, compression='gzip')
        proc = proc[proc['hadm_id'].isin(cohort['hadm_id'])]
        
        # Aggregate into lists
        proc_grp = proc.groupby('hadm_id')['icd_code'].apply(list).reset_index()
        proc_grp = proc_grp.rename(columns={'icd_code': 'Proc'})
        
        cohort = cohort.merge(proc_grp, on='hadm_id', how='left')
    else:
        print("Warning: Procedure file not found.")
        cohort['Proc'] = None

    # 4. Process Medications (Med)
    print("[ PROCESSING MEDICATIONS ]")
    if os.path.exists(med_path):
        med = pd.read_csv(med_path, compression='gzip')
        med = med[med['hadm_id'].isin(cohort['hadm_id'])]
        
        # Aggregate into lists (using 'drug_name')
        med_grp = med.groupby('hadm_id')['drug_name'].apply(list).reset_index()
        med_grp = med_grp.rename(columns={'drug_name': 'Med'})
        
        cohort = cohort.merge(med_grp, on='hadm_id', how='left')
    else:
        print("Warning: Medication file not found.")
        cohort['Med'] = None

    # 5. Process Labs (Lab)
    print("[ PROCESSING LABS ]")
    if os.path.exists(lab_path):
        # Labs file can be large, reading entire file
        lab = pd.read_csv(lab_path, compression='gzip')
        lab = lab[lab['hadm_id'].isin(cohort['hadm_id'])]
        
        # Aggregate into lists (using 'itemid')
        # Note: itemid is usually int, converting to string for consistency with example if needed, 
        # but list of ints is also valid. Leaving as is.
        lab_grp = lab.groupby('hadm_id')['itemid'].apply(list).reset_index()
        lab_grp = lab_grp.rename(columns={'itemid': 'Lab'})
        
        cohort = cohort.merge(lab_grp, on='hadm_id', how='left')
    else:
        print("Warning: Lab file not found.")
        cohort['Lab'] = None

    # 6. Cleanup and Save
    print("[ FINALIZING ]")
    
    # Fill NaN values with empty lists [] for patients who have no records in a specific modality
    for col in ['Cond', 'Proc', 'Med', 'Lab']:
        # Ensure the column exists (in case a file was missing)
        if col not in cohort.columns:
            cohort[col] = None
        
        # Replace NaN/None with []
        cohort[col] = cohort[col].apply(lambda x: x if isinstance(x, list) else [])

    # Save to CSV
    cohort.to_csv(output_filename, index=False)
    print(f"SUCCESS: Generated {output_filename} with {len(cohort)} rows.")

# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    # REPLACE THIS with the actual name of your cohort file found in ./data/cohort/
    # Do not include the .csv.gz extension.
    # Example: "cohort_non-icu_readmission_30_no_disease_filter"
    pwd = os.getcwd()
    print(f"Current working directory: {pwd}")
    my_cohort_name = "cohort_non-icu_readmission_30_"          
    generate_patient_features_csv(my_cohort_name)