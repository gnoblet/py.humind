def value_to_sl(
        df, 
        var, 
        undefined = None, 
        sl_vars = None, 
        sl_value = None, 
        suffix = ""):
    """
    Updates a Pandas DataFrame by replacing missing values in specified columns with a given value.

    Parameters:
    ----------
    df (pandas.DataFrame): The input DataFrame to be updated.
    var (str): The name of the column to check for "undefined" values.
    undefined (list, optional): A list of values to consider as "undefined" in the `var` column. Defaults to None.
    sl_vars (list, optional): A list of column names to update with the `sl_value`. Defaults to None.
    sl_value (any, optional): The value to replace missing values in `sl_vars` columns. Defaults to None.
    suffix (str, optional): An optional suffix to append to the updated column names. Defaults to "".

    Returns:
    pandas.DataFrame: Updated df with missing values replaced in columns sl_vars. If var values are not in undefined, then sl_vars values are replaced with sl_value.
    - If sl_vars is None, returns df unchanged.
    - If sl_value is None, returns df unchanged.
    """

    #------ Checks

    # Check types of parameters

    # df is a dataframe
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    # var is a string
    if not isinstance(var, str):
        raise TypeError("var must be a string")
    
    # sl_vars is a list of character strings
    if not (sl_vars is None or isinstance(sl_vars, list) and all(isinstance(v, str) for v in sl_vars)):
        raise TypeError("sl_vars must be a list of strings")
    
    # sl_value is a number
    if not (sl_value is None or isinstance(sl_value, (int, float))):
        raise TypeError("sl_value must be a number")
    
    # suffix is a string
    if not (suffix is None or isinstance(suffix, str)):
        raise TypeError("suffix must be a string")
    
    # Check that variables exist and are of the right type

    # var exist in df and is a character variable
    if var not in df.columns or not isinstance(df[var].iloc[0], str):
        raise ValueError("var " + str(var) + " not found in DataFrame or not a string")
    
    # sl_vars exist in df and are numeric variables
    if not (sl_vars is None or isinstance(sl_vars, list) and all(v in df.columns and isinstance(df[v].iloc[0], (int, float)) for v in sl_vars)):
        raise ValueError("sl_vars " + str(sl_vars) + " not found in DataFrame or not numeric")
    
    #------ Add value

    # Add sl_value across sl_vars if sl_vars is NA and var is not "undefined"
    for sl_var in sl_vars:
        df[f"{sl_var}{suffix}"] = np.where(
            df[sl_var].isna() & ~df[var].isin(undefined if undefined is not None else []),
            sl_value,
            df[sl_var]
        )

    return df