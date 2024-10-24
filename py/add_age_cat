
def add_age_cat(
    df, 
    age_col, 
    breaks = [0, 18, 60, 120], 
    labels = None,
    int_undefined = [-999, 999],
    char_undefined = "undefined", 
    new_colname = None):
    """
    Adds an age category column to a Pandas DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame to be updated.
    age_col (str): The name of the column containing the age values.
    breaks (list, optional): A list of age break points. Defaults to [0, 18, 60, 120].
    labels (list, optional): A list of labels for the age categories. Defaults to None.
    int_undefined (list, optional): A list of integer values to consider as "undefined" in the `age_col` column. Defaults to [-999, 999].
    char_undefined (str, optional): A string value to consider as "undefined" in the `age_col` column. Defaults to "undefined".
    new_colname (str, optional): The name of the new age category column. Defaults to None.

    Returns:
    pandas.DataFrame: The updated DataFrame with the new age category column.

    Notes:
    This function assumes that the `num_cat` function is defined elsewhere.
    """

    # Use categorize_num function (assumed to be defined elsewhere)
    df  = num_cat(
        df = df,
        num_col = age_col,
        breaks = breaks,
        labels = labels,
        int_undefined = int_undefined,
        char_undefined = char_undefined,
        new_colname = new_colname,
        plus_last = True,
        above_last = True
    )
    return df


def add_age_18_cat(
        df, 
        age_col, 
        int_undefined = [-999, 999], 
        char_undefined = "undefined", 
        new_colname = None):
    """
    Adds two age category columns to a Pandas DataFrame, categorizing ages as below or above 18 and the associated binary column.

    Parameters:
    df (pandas.DataFrame): The input DataFrame to be updated.
    age_col (str): The name of the column containing the age values.
    int_undefined (list): A list of integer values to consider as "undefined" in the `age_col` column. Defaults to [-999, 999].
    char_undefined (str): A string value to consider as "undefined" in the `age_col` column. Defaults to "undefined".
    new_colname (str, optional): The name of the new age category column. Defaults to None adds a "_18_cat" suffix to age_col and a "_d" suffix to the new binary column.

    Returns:
    pandas.DataFrame: The updated DataFrame with the new age category column and a new binary column.
    """

    # If new_colname is not provided, create one
    if new_colname is None:
        new_colname = f"{age_col}_18_cat"

    # Paste "_d" for the new binary column
    new_colname_d = f"{new_colname}_d"

    df[new_colname] = np.select(
        [
            df[age_col].isin(int_undefined),
            df[age_col] < 18,
            df[age_col] >= 18
        ],
        [
            char_undefined,
            "below_18",
            "above_18"
        ],
        default = np.nan
    )

    df[new_colname_d] = np.select(
        [
            df[new_colname] == char_undefined,
            df[new_colname] == "above_18",
            df[new_colname] == "below_18"
        ],
        [
            np.nan,
            1,
            0
        ],
        default = np.nan
    )

    return df