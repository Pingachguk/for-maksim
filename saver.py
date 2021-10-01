import pandas as pd

def save(data: pd.DataFrame):
    data.to_excel("data.xlsx", engine='xlsxwriter', index=False)