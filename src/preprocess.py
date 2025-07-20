import pandas as pd

def preprocess_ev_data(csv_path):
    df = pd.read_csv(csv_path)

    df['Year'] = df['Year'].astype(int)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    categorical_columns = ['Month_Name', 'State', 'Vehicle_Class',
                           'Vehicle_Category', 'Vehicle_Type']
    df[categorical_columns] = df[categorical_columns].astype('category')

    return df
