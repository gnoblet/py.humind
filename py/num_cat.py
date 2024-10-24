import pandas as pd
import numpy as np

def num_cat(
        df,
        num_col, 
        breaks, 
        labels = None, 
        int_undefined = [-999, 999],
        char_undefined = "Unknown", 
        new_colname = None, 
        plus_last = False, 
        above_last = False):
    
    """
    Categorizes a numeric column in a Pandas DataFrame into discrete categories.

    Parameters:
    df (pandas.DataFrame): The input DataFrame to be updated.
    num_col (str): The name of the column containing the numeric values to be categorized.
    breaks (list): A list of break points to define the categories.
    labels (list, optional): A list of labels for the categories. Defaults to None.
    int_undefined (list): A list of integer values to consider as "undefined" in the `num_col` column. Defaults to [-999, 999].
    char_undefined (str): A string value to consider as "undefined" in the `num_col` column. Defaults to "Unknown".
    new_colname (str, optional): The name of the new category column. Defaults to None adds a "_cat" suffix to num_col.
    plus_last (bool): Whether to include a "+" sign in the label for the last category. Defaults to False.
    above_last (bool): Whether to include values above the last break point in the last category. Defaults to False.

    Returns:
    pandas.DataFrame: The updated DataFrame with the new category column.
    """
    
    #------ Checks

    # Check for types

    # df is a dataframe
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a dataframe")

    # num_col is a string
    if not isinstance(num_col, str):
        raise TypeError("num_col must be a string")
    
    # breaks is a list with numeric values only
    if not (isinstance(breaks, list) and all(isinstance(v, (int, float)) for v in breaks)):
        raise TypeError("breaks must be a list of numeric values")
    
    # labels is a list of strings
    if labels is not None and not isinstance(labels, list):
        raise TypeError("labels must be a list of strings")
    
    # int_undefined is a list of integers
    if not all(isinstance(i, int) for i in int_undefined):
        raise TypeError("int_undefined must be a list of integers")
    
    # char_undefined is a string
    if not isinstance(char_undefined, str):
        raise TypeError("char_undefined must be a string")
    
    # new_colname is a string
    if new_colname is not None and not isinstance(new_colname, str):
        raise TypeError("new_colname must be a string")
    
    # plus_last is a boolean and not none
    if not (isinstance(plus_last, bool) and not pd.isna(plus_last)):
        raise TypeError("plus_last must be a boolean and not NA")
    
    # above_last is a boolean and not None
    if not (isinstance(above_last, bool) and not pd.isna(above_last)):
        raise TypeError("above_last must be a boolean and not NA")

    # Checks for the existence and types of columns 

    # num_col is in df
    if num_col not in df.columns:
        raise ValueError(f"{num_col} is not in the dataframe")

    # num_col is numeric
    if not pd.api.types.is_numeric_dtype(df[num_col]):
        raise ValueError(f"{num_col} must be numeric")
    
    # Further checks

    # char_undefined is of length 1
    if len(char_undefined) != 1:
        raise ValueError("char_undefined must be of length 1")

    # breaks have at least two values
    if len(breaks) < 2:
        raise ValueError("breaks must have at least two values")

    # labels qre of length of breaks if above_last is TRUE
    if labels is not None and len(labels) != len(breaks) and above_last:
        print("labels must be of length of breaks. Reverting to labels = None")
        labels = None

    # if labels is of length of breaks - 1 if above_last is FALSE
    if labels is not None and len(labels) != len(breaks) - 1 and not above_last:
        print("labels must be of length of breaks - 1. Reverting to labels = None")
        labels = None

    # If new_colname is not provided, create one
    if new_colname is None:
        new_colname = f"{num_col}_cat"

    #----- Create labels if NULL

    vals = df[num_col][~df[num_col].isin(int_undefined)]
    max_val = vals.max()

    # Total number of breaks
    if above_last:
        breaks = breaks + [np.inf]

    # If labels are not provided, generate them
    if labels is None:
    labels = []
    for i in range(len(breaks) - 1):
        if i < len(breaks) - 2:
            label = f"{breaks[i]}-{breaks[i + 1] - 1}"
        elif plus_last:
            label = f"{breaks[i]}+"
        else:
            label = f"{breaks[i]}-{max_val}"
        labels.append(label)

    #----- Add cat variable to df
    df[new_colname] = np.select(
        [
            df[num_col].isin(int_undefined),
            df[num_col] < min(breaks)
        ],
        [
            char_undefined,
            np.nan
        ],
        default = pd.cut(df[num_col], bins=breaks, labels=labels, include_lowest = True, right = False)
    )

    return df