import pandas as pd
import numpy as np

def add_fcs(
    df, 
    cutoffs = ["normal", "alternative"], 
    fsl_fcs_cereal = "fsl_fcs_cereal", 
    fsl_fcs_legumes = "fsl_fcs_legumes", 
    fsl_fcs_veg = "fsl_fcs_veg", 
    fsl_fcs_fruit = "fsl_fcs_fruit", 
    fsl_fcs_meat = "fsl_fcs_meat", 
    fsl_fcs_dairy = "fsl_fcs_dairy", 
    fsl_fcs_sugar = "fsl_fcs_sugar", 
    fsl_fcs_oil = "fsl_fcs_oil"):
    
    """
    Adds a set of columns to a Pandas DataFrame representing the Food Composition Survey (FCS) nutrient intake.

    Parameters:
    df (pandas.DataFrame): The input DataFrame to be updated.
    fsl_fcs_cereal (str): The name of the column that indicates the number of days cereals were consumed.
    fsl_fcs_legumes (str): The name of the column that indicates the number of days legumes were consumed.
    fsl_fcs_dairy (str): The name of the column that indicates the number of days dairy products were consumed.
    fsl_fcs_meat (str): The name of the column that indicates the number of days meat products were consumed.
    fsl_fcs_veg (str): The name of the column that indicates the number of days vegetables were consumed.
    fsl_fcs_fruit (str): The name of the column that indicates the number of days fruits were consumed.
    fsl_fcs_oil (str): The name of the column that indicates the number of days oil products were consumed.
    fsl_fcs_sugar (str): The name of the column that indicates the number of days sugar products were consumed.
    cutoffs (str): The cutoffs to use for categorizing the FCS score. Defaults to "normal", either "normal" or "alternative".

    Returns:
    pandas.DataFrame: The updated DataFrame with the added 'fsl_fcs_score' and 'fsl_fcs_cat' columns, as well as the 8 weighted food groups.
    """
    
    #------ Checks
    
    # Check types of parameters
    
    # df is a dataframe
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    
    # cutoffs is either "normal" or "alternative"
    if cutoffs not in ["normal", "alternative"]:
        raise ValueError("cutoffs must be either 'normal' or 'alternative'")
    
    # fcs_vars is a list of strings NOT NULL
    fcs_vars = [fsl_fcs_cereal, fsl_fcs_legumes, fsl_fcs_veg, fsl_fcs_fruit, fsl_fcs_meat, fsl_fcs_dairy, fsl_fcs_sugar, fsl_fcs_oil]
    for var in fcs_vars:
        if not isinstance(var, str):
            raise TypeError("Parameter" + str(var) + " must be a string")            
        if var is None:
            raise ValueError("Parameter" + str(var) + " cannot be None")
            
    # Check if variables are in df and of the right type
    
    # df is not an empty dataframe (0 row)
    if df.shape[0] == 0:
        raise ValueError("df is empty")
    
    # fcs_vars are in df (error should print the missing columns)
    for var in fcs_vars:
        if var not in df.columns:
            raise ValueError(var + " not in df")
    
    # fcs_vars are integers
    for var in fcs_vars:
        if not isinstance(df[var], (int, np.integer)):
            raise TypeError(var + " must be integer")
        
    # fcs_vars: all values must be between 0 and 7 or missing/NA
    fcs_values = [0, 1, 2, 3, 4, 5, 6, 7]
    if not all(x in fcs_values for x in df[fcs_vars].values.flatten()):
        raise ValueError("All values in fcs_vars must be integers between 0 and 7 or missing")
        
    # Further checks
        
    # fsl_fcs_score is in df and raise warning that it will be overwritten
    if fsl_fcs_score in df.columns:
        print("Warning: fsl_fcs_score will be overwritten")
        
    # fsl_fcs_cat is in df and raise warning that it will be overwritten
    if fsl_fcs_cat in df.columns:
        print("Warning: fsl_fcs_cat will be overwritten")
        
    # weight columns are in df and raise warning that they will be overwritten
    if "fsl_fcs_weight_cereal" in df.columns:
        print("Warning: fsl_fcs_weight_cereal will be overwritten")
    if "fsl_fcs_weight_legume" in df.columns:
        print("Warning: fsl_fcs_weight_legume will be overwritten")
    if "fsl_fcs_weight_dairy" in df.columns:
        print("Warning: fsl_fcs_weight_dairy will be overwritten")
    if "fsl_fcs_weight_meat" in df.columns:
        print("Warning: fsl_fcs_weight_meat will be overwritten")
    if "fsl_fcs_weight_veg" in df.columns:
        print("Warning: fsl_fcs_weight_veg will be overwritten")
    if "fsl_fcs_weight_fruit" in df.columns:
        print("Warning: fsl_fcs_weight_fruit will be overwritten")
    if "fsl_fcs_weight_oil" in df.columns:
        print("Warning: fsl_fcs_weight_oil will be overwritten")
    if "fsl_fcs_weight_sugar" in df.columns:
        print("Warning: fsl_fcs_weight_sugar will be overwritten")
    
    
    # ------ Compose
    
    # Add weights columns for each food group
    df['fsl_fcs_weight_cereal'] = np.where(df[fsl_fcs_cereal].isna(), np.nan, df[fsl_fcs_cereal] * 2)
    df['fsl_fcs_weight_legume'] = np.where(df[fsl_fcs_legumes].isna(), np.nan, df[fsl_fcs_legumes] * 3)
    df['fsl_fcs_weight_dairy'] = np.where(df[fsl_fcs_dairy].isna(), np.nan, df[fsl_fcs_dairy] * 4)
    df['fsl_fcs_weight_meat'] = np.where(df[fsl_fcs_meat].isna(), np.nan, df[fsl_fcs_meat] * 4)
    df['fsl_fcs_weight_veg'] = np.where(df[fsl_fcs_veg].isna(), np.nan, df[fsl_fcs_veg] * 1)
    df['fsl_fcs_weight_fruit'] = np.where(df[fsl_fcs_fruit].isna(), np.nan, df[fsl_fcs_fruit] * 1)
    df['fsl_fcs_weight_oil'] = np.where(df[fsl_fcs_oil].isna(), np.nan, df[fsl_fcs_oil] * 0.5)
    df['fsl_fcs_weight_sugar'] = np.where(df[fsl_fcs_sugar].isna(), np.nan, df[fsl_fcs_sugar] * 0.5)
    
    # Add score (sum by row across weigth columns)    
    df['fsl_fcs_score'] = df[['fsl_fcs_weight_cereal', 'fsl_fcs_weight_legume', 'fsl_fcs_weight_dairy', 
                                         'fsl_fcs_weight_meat', 'fsl_fcs_weight_veg', 'fsl_fcs_weight_fruit', 
                                         'fsl_fcs_weight_oil', 'fsl_fcs_weight_sugar']].sum(axis = 1)
    
    # Add category based on cutoffs and score
    if cutoffs == "normal":
        df['fsl_fcs_cat'] = np.select(
            [df['fsl_fcs_score'] < 21.5, 
             (df['fsl_fcs_score'] >= 21.5) & (df['fsl_fcs_score'] <= 35), 
             df['fsl_fcs_score'] > 35],
            ["Poor", "Borderline", "Acceptable"],
            default=np.nan
        )
    elif cutoffs == "alternative":
        df['fsl_fcs_cat'] = np.select(
            [df['fsl_fcs_score'] <= 28, 
             (df['fsl_fcs_score'] > 28) & (df['fsl_fcs_score'] <= 42), 
             df['fsl_fcs_score'] > 42],
            ["Poor", "Borderline", "Acceptable"],
            default=np.nan
        )
    
    return df

