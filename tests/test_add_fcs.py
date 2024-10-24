# tests/test_add_fcs.py

import pandas as pd
import numpy as np
from py.humind import add_fcs

def test_add_fcs():
    
    # Create a sample DataFrame
    data = {
        'fsl_fcs_cereal': [1, 2, np.nan, 4],
        'fsl_fcs_legumes': [5, np.nan, 7, 8],
        'fsl_fcs_dairy': [2, 10, 11, np.nan],
        'fsl_fcs_meat': [2, 3, np.nan, 5],
        'fsl_fcs_veg': [6, 7, 1, np.nan],
        'fsl_fcs_fruit': [7, np.nan, 2, 2],
        'fsl_fcs_oil': [5, 4, np.nan, 6],
        'fsl_fcs_sugar': [5, 5, 7, np.nan]
    }
    df = pd.DataFrame(data)

    # Call the add_fcs function
    result = add_fcs(df, 'fsl_fcs_cereal', 'fsl_fcs_legumes', 'fsl_fcs_dairy', 'fsl_fcs_meat', 'fsl_fcs_veg', 'fsl_fcs_fruit', 'fsl_fcs_oil', 'fsl_fcs_sugar')

    # Check if the result is a DataFrame
    assert isinstance(result, pd.DataFrame)

    # Check if the result has the expected columns
    expected_columns = [
        'fsl_fcs_weight_cereal',
        'fsl_fcs_weight_legume',
        'fsl_fcs_weight_dairy',
        'fsl_fcs_weight_meat', 
        'fsl_fcs_weight_veg',
        'fsl_fcs_weight_fruit', 
        'fsl_fcs_weight_oil',
        'fsl_fcs_weight_sugar', 
        'fsl_fcs_score',
        'fsl_fcs_cat']
    assert all(col in result.columns for col in expected_columns)

    # Check if the result has the expected number of rows
    assert len(result) == len(df)

# Run the test
test_add_fcs()