import pandas as pd
import requests
import csv
from io import StringIO


#url = "https://data.ny.gov/resource/wujg-7c2s.json?$limit=50&$offset=150" # hourly 
url = "https://data.ny.gov/resource/sayj-mze2.json" #daily with 12971 rows ~ 12,000 rows 
#response = requests.get(url)
limit = 1000
offsets = [i * 1000 for i in range(1000)] # a million rows 
df = []



def retrieve_data_and_upload_to_csv():
    for offset in offsets: 
        url = f"https://data.ny.gov/resource/wujg-7c2s.json?$limit={limit}&$offset={offset}"
        response = requests.get(url)
        if response.status_code == 200: 
            data = response.json()
            df.append(data)
            print("Appending:", data)
        else: 
            print(f"Error: {response.status_code} at {offset}")


    final_df = pd.DataFrame([item for sublist in df for item in sublist])

    with open ("updated_hourly.csv", mode = "w", newline = '', encoding = 'utf-8') as file: 
        writer = csv.writer(file)
        writer.writerow(final_df.columns)
        writer.writerows(final_df.values)

    print(final_df.head())

    print(f"Total rows retrieved: {len(final_df)}")

def data_analysis():
    num_of_lines = 5
    lines = []
    with open("hourly.csv", mode = "r", newline = '', encoding = 'utf-8') as file: 
        df = pd.read_csv(file)
    print(df.columns)
    print(df.head())


# invoke functions 
retrieve_data_and_upload_to_csv()




        







        



            
            

