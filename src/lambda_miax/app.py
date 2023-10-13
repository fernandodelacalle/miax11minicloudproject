import datetime

from api_handler import BMEApiHandler
from dynamo_handler import DynamoHandle

def handler(event, context):
    apih = BMEApiHandler()
    dynh = DynamoHandle(table_name='IBEX_TEST')
    maestro = apih.get_ticker_master()

    # dynh.create_table()

    now_str = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    for tck in maestro.ticker.to_list():
        print(tck)
        df_tck = apih.get_close_data(tck)
        print(df_tck)

        dynh.upload_close_data(df_tck, tck)
        out_path = f's3://miax11minicloudproject/{now_str}/{tck}.csv'
        print(out_path)
        df_tck.to_csv(out_path)
