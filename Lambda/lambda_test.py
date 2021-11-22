import json
import pandas as pd

def lambda_handler(event, context):
    url = "https://www.nfl.com/stats/player-stats/"

    df = pd.read_html(url)

    df= df[0]

    print(df.head())

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }