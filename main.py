"""
Get BEA API Key for free at : https://apps.bea.gov/api/signup/
API User Guide : https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf
"""

import requests
import pandas as pd

def get_bea_api_key():
    # Replace 'YOUR_API_KEY' with your actual BEA API key
    return 'YOUR_API_KEY'

def fetch_bea_data(api_key, datasetname, table_name, frequency, year, line_description=None, show_all=False):
    url = 'https://apps.bea.gov/api/data/'
    params = {
        'UserID': api_key,
        'method': 'GetData',
        'datasetname': datasetname,
        'TableName': table_name,
        'Frequency': frequency,
        'Year': year,
        'ResultFormat': 'json'
    }

    response = requests.get(url, params=params)
    data = response.json()
    data = data['BEAAPI']['Results']['Data']
    df = pd.DataFrame(data)

    if line_description:
        df = df.loc[df['LineDescription'] == line_description]

    df['DataValue'] = df['DataValue'].str.replace(',', '').astype(float)

    if frequency == 'Q':
        df['TimePeriod'] = pd.PeriodIndex(df['TimePeriod'], freq='Q').to_timestamp()
    elif frequency == 'M':
        df['TimePeriod'] = df['TimePeriod'].apply(lambda x: pd.to_datetime(x[:4] + '-' + x[5:]))

    df = df.sort_values('TimePeriod')
    if show_all == True:
        return df
    else:
        return df[['TimePeriod', 'DataValue']]

def get_bea_table_names(api_key):  # Return BEA avaible table names, need to note using line_description to filter further
    url = 'https://apps.bea.gov/api/data/'
    params = {
        'UserID': api_key,
        'method': 'GetParameterValues',
        'datasetname': 'NIPA',
        'ParameterName': 'TableName',
        'ResultFormat': 'json'
    }

    response = requests.get(url, params=params)
    data = response.json()
    tables = data['BEAAPI']['Results']['ParamValue']
    return pd.DataFrame(tables)

def main():
    api_key = get_bea_api_key()
    
#     print("GDP Data") 
#     gdp_df = fetch_bea_data(api_key, 'NIPA', 'T10105', 'Q', 'ALL', line_description=None)
#     print(gdp_df)
    
    print("GDP Quarterly Percentage Change Data") # https://www.bea.gov/data/gdp/gross-domestic-product
    gdp_pct_change_df = fetch_bea_data(api_key, 'NIPA', 'T10101', 'Q', 'ALL', line_description='Gross domestic product', show_all=False)
#     print(gdp_pct_change_df['LineDescription'].unique()) 
    print(gdp_pct_change_df) #T10101 #Gross domestic product'

    print("PCE Data")
    pce_df = fetch_bea_data(api_key, 'NIPA', 'T20811', 'M', '2024', line_description='Personal consumption expenditures')
    print(pce_df)

    # Get and save BEA table names
    tables_df = get_bea_table_names(api_key)
    print (tables_df) # tables_df.to_csv('bea_table_names.csv', index=False)


if __name__ == "__main__":
    main()
