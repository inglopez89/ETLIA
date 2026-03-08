import pandas as pd

class DataProcessingActions:
    """
    A class to perform various data processing actions such as merging dataframes.
    """
    def merge_data(df_1, df_2, **params):
        """
        Merges two dataframes based on specified columns and merge type.

        Parameters:
        df_1 (pd.DataFrame): First dataframe to merge.
        df_2 (pd.DataFrame): Second dataframe to merge.
        columns_1 (list): List of column names from the first dataframe to merge on.
        columns_2 (list): List of column names from the second dataframe to merge on.
        how (str): Type of merge to perform. Options are 'inner', 'outer', 'left', 'right'. Default is 'inner'.

        Returns:
        pd.DataFrame: Merged dataframe.
        """
        merged_df = pd.merge(
            df_1, df_2,
            left_on=params.get("columns_1"),
            right_on=params.get("columns_2"),
            how=params.get("how", "inner"),
        )
        return merged_df

    def filter_data(df, filter_conditions):
        """
        Filters a dataframe based on specified conditions.

        Parameters:
        df (pd.DataFrame): Dataframe to filter.
        filter_conditions (dict): Dictionary where keys are column names and values are the conditions to filter on.

        Returns:
        pd.DataFrame: Filtered dataframe.
        """
        for column, condition in filter_conditions.items():
            df = df[df[column] == condition]
        return df
AVAILABLE_ACTIONS = {
    'merge_data': DataProcessingActions.merge_data,
    'filter_data': DataProcessingActions.filter_data
}