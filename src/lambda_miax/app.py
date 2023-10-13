import datetime

from api_handler import BMEApiHandler


def handler(event, context):
    apih = BMEApiHandler()
    maestro = apih.get_ticker_master()

    now_str = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    for tck in maestro.ticker.to_list():
        print(tck)
        df_tck = apih.get_close_data(tck)
        out_path = f's3://miax11minicloudproject/{now_str}/{tck}.csv'
        print(out_path)
        df_tck.to_csv(out_path)
