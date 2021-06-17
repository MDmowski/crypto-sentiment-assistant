import json

from requests import Session, Timeout, TooManyRedirects
import pandas as pd


class StockHistory:
    url = 'https://min-api.cryptocompare.com'
    parameters = {
        'extraParams': 'cryptoStockChart',
    }
    headers = {
        'Accepts': 'application/json',
        'Apikey': '7832da29e85039a8db58851b5863f9b559966e19e34dcc48fbbe9110d55a0f9d',
    }

    def load_data(self, symbol, aggregation, currency, limit):
        req = f'/data/v2/histoday?fsym={symbol}&aggregate={aggregation}&tsym={currency}&limit={limit}'

        session = Session()
        session.headers.update(self.headers)

        try:
            response = session.get(self.url + req, params=self.parameters)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            return 0

        df = pd.DataFrame()

        from datetime import datetime
        for row in data['Data']['Data']:
            df = df.append({
                'date': datetime.fromtimestamp(row['time']).strftime('%Y-%m-%d'),
                'price': row['close']
            }, ignore_index=True)

        return df
