import pandas as pd
import requests
import json
import os


class BMEApiHandler:

    def __init__(self):
        self.url_base = 'https://miax-gateway-jog4ew3z3q-ew.a.run.app'
        self.competi = 'mia_11'
        self.user_key = os.environ["MIAX_API_KEY"]

    def get_ticker_master(self):
        url = f'{self.url_base}/data/ticker_master'
        params = {'competi': self.competi,
                'market': 'IBEX',
                'key': self.user_key}
        response = requests.get(url, params)
        tk_master = response.json()
        maestro_df = pd.DataFrame(tk_master['master'])
        return maestro_df

    def get_close_data(self, tck) -> pd.Series:
        url = f'{self.url_base}/data/time_series'
        params = {
            'market': 'IBEX',
            'key': self.user_key,
            'ticker': tck
        }
        response = requests.get(url, params)
        tk_data = response.json()
        series_data = pd.read_json(tk_data, typ='series')
        return series_data

    def send_alloc(self, algo_tag, str_date, allocation):
        url = f'{self.url_base}/participants/allocation'
        url_auth = f'{url}?key={self.user_key}'
        print(url_auth)
        params = {
            'competi': self.competi,
            'algo_tag': algo_tag,
            'market': 'IBEX',
            'date': str_date,
            'allocation': allocation
        }
        #print(json.dumps(params))
        response = requests.post(url_auth, data=json.dumps(params))
        print(response.json())

    def get_algos(self):
        url = f'{self.url_base}/participants/algorithms'
        params = {'competi': self.competi,
                'key': self.user_key}
        response = requests.get(url, params)
        algos = response.json()
        if algos:
            algos_df = pd.DataFrame(algos)
            return algos_df

    def allocs_to_frame(self, json_allocations):
        alloc_list = []
        for json_alloc in json_allocations:
            #print(json_alloc)
            allocs = pd.DataFrame(json_alloc['allocations'])
            allocs.set_index('ticker', inplace=True)
            alloc_serie = allocs['alloc']
            alloc_serie.name = json_alloc['date'] 
            alloc_list.append(alloc_serie)
        all_alloc_df = pd.concat(alloc_list, axis=1).T
        return all_alloc_df

    def get_allocations(self, algo_tag):
        url = f'{self.url_base}/participants/algo_allocations'
        params = {
            'key': self.user_key,
            'competi': self.competi,
            'algo_tag': algo_tag,
            'market': 'IBEX',
        }
        response = requests.get(url, params)
        df_allocs = self.allocs_to_frame(response.json())
        return df_allocs


    def delete_allocs(self, algo_tag):
        url = f'{self.url_base}/participants/delete_allocations'
        url_auth = f'{url}?key={self.user_key}'
        params = {
            'competi': self.competi,
            'algo_tag': algo_tag,
            'market': 'IBEX',
            }
        response = requests.post(url_auth, data=json.dumps(params))
        print(response.text)


    def backtest_algo(self, algo_tag):
        url = f'{self.url_base}/participants/exec_algo'
        url_auth = f'{url}?key={self.user_key}'
        params = {
            'competi': self.competi,
            'algo_tag': algo_tag,
            'market': 'IBEX',
            }
        response = requests.post(url_auth, data=json.dumps(params))
        if response.status_code == 200:
            exec_data = response.json()
            status = exec_data.get('status')
            res_data = exec_data.get('content')
            if res_data:
                performace = pd.Series(res_data['result'])
                trades = pd.DataFrame(res_data['trades'])
                return performace, trades
        else:
            exec_data = dict()
            print(response.text)

    def algo_exec_results(self, algo_tag):
        url = f'{self.url_base}/participants/algo_exec_results'
        params = {
            'key': self.user_key,
            'competi': self.competi,
            'algo_tag': algo_tag,
            'market': self.market,
        }     
        response = requests.get(url, params)
        exec_data = response.json()
        print(exec_data.get('status'))
        res_data = exec_data.get('content')
        if res_data:
            performace = pd.Series(res_data['result'])
            trades = pd.DataFrame(res_data['trades'])
            return performace, trades
