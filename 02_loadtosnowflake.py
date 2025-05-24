import snowflake.connector
import json

def load():
    DB_CONFIG = {
        "user": "miles",
        "password": "yourpass",
        "account": "youraccount",
        "warehouse": "ETL_WH",
        "database": "WEATHER_DB",
        "schema": "RAW"   # load to WEATHER_DB/RAW
        }
    
    db = snowflake.connector.connect(**DB_CONFIG)  # connect to snowflake
    cursor = db.cursor()
    
    with open('/opt/airflow/data/raw_weather.json', 'r') as f: # path in the airflow container
        raw_data = json.load(f)
    
    # for local machine run
    #with open('/Users/Zjxi/Desktop/elt/extracted_data.json', 'r') as f:
    #    raw_data = json.load(f)
    

    # load data to WEATHER_DB/RAW/WEATHER_TABLE
    for record in raw_data:
        city, datetime_val = record['city'], record['datetime']
        raw_json = json.dumps(record)
        stmt = '''
            INSERT INTO WEATHER_TABLE (city, observation_time, raw_json)
            VALUES (%s, %s, %s)'''
        cursor.execute(stmt, (city, datetime_val, raw_json))

    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    load()



