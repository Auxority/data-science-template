import pandas as pd
from DataVisualizer import DataVisualizer
from IPython.display import display

class DataExplorer:
    def __init__(self, dv: DataVisualizer):
        self.dv = dv

    def explore(self, df: pd.DataFrame) -> None:
        self.show_shape(df)
        self.show_missing(df)
        self.show_duplicate(df)

        print('Variable types and summary statistics:')
        for dtype in df.dtypes.unique():
            subset = df.select_dtypes(include=[dtype])
            if subset.shape[1] > 0:
                print(f'\n{dtype} variables:')
                display(subset.describe(datetime_is_numeric=True).transpose())

        self.dv.visualize(df)

    def show_missing(self, df: pd.DataFrame) -> None:
        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            message = 'There are {} missing values in the dataset.\n' if missing_values.sum() > 1 else 'There is {} missing value in the dataset.\n'
            print(message.format(missing_values.sum()))
            display(missing_values.to_frame().rename(columns={0: 'count'}))
        else:
            print('There are no missing values in the dataset.\n')
    
    def show_duplicate(self, df: pd.DataFrame) -> None:
        duplicated = df.duplicated()
        if duplicated.sum() > 0:
            message = 'There are {} duplicate rows in the dataset.\n' if duplicated.sum() > 1 else 'There is {} duplicate row in the dataset.\n'
            print(message.format(duplicated.sum()))
            display(df[duplicated])
        else:
            print('There are no duplicate rows in the dataset.\n')
    
    def show_shape(self, df: pd.DataFrame) -> None:
        n_rows, n_cols = df.shape
        print(f'The dataset has {n_rows} rows and {n_cols} columns.\n')
