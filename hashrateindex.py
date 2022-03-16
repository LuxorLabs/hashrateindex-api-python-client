# import packages
import json
import logging
import requests
import optparse
from typing import Dict, Any
from resolvers import RESOLVERS

# set logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(),
              logging.FileHandler('requests.log')])


class API:
    """
    A class used to interact with Luxor's HashrateIndex GraphQL API.

    Methods
    -------
    request(query, params)
        Base function to execute operations against Luxor's GraphQL API
    
    get_bitcoin_overview()
        Contains Bitcoin network data overview stats.
        
    get_hashprice(inputInterval, currency)
        Returns Bitcoin hashprice for a specified interval
    
    get_network_hashrate(inputInterval)
        Returns the network hashrate for a specified interval
    
    get_network_difficulty(inputInterval)
        Returns the network difficulty and bitcoin price.
    
    get_ohlc_prices(inputInterval)
        Returns the Bitcoin OLHC prices at a specified interval.
    
    get_asic_price_index(inputInterval, currency)
        Returns the ASIC price index in USD for a given time interval.
    """
    def __init__(self,
                 host: str,
                 key: str,
                 method: str,
                 verbose: bool = False):
        """
        Parameters
        ----------

        host : str
            Base endpoint for all API requests. Default is: https://api.hashrateindex.com/graphql

        key : str
            Random generated API Key. Default is an empty string.
        
        method : str
            API request METHOD. Default is `POST`.
        
        query : str
            API request QUERY. Default is an empty string.

        params : str
            API request PARAMS. Default is an empty string.

        verbose : boolean
            Boolean flag that controls if API querys are logged.
        """

        self.host = host
        self.key = key
        self.method = method
        self.verbose = verbose

    def request(self, query: str, params: Dict[str, Any] = None):
        """
        Base function to execute operations against Luxor's GraphQL API

        Parameters
        ----------
        query : str
            GraphQL compliant query string.
        params : dictionary
            dictionary containing the query parameters, values depend on query.
        """

        headers = {
            'Content-Type': 'application/json',
            'x-hi-api-key': f"{self.key}",
        }

        s = requests.Session()
        s.headers = headers

        if self.verbose:
            logging.info(query)

        response = s.request(self.method,
                             self.host,
                             data=json.dumps({
                                 'query': query,
                                 'variables': params
                             }).encode('utf-8'))

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(
                str(response.status_code) + ": " + str(response.reason) + ": " +
                str(response.content.decode()))
        else:
            raise Exception(str(response.status_code) + ": " + str(response.reason))

    # Define API Methods
    def get_bitcoin_overview(self) -> requests.Request:
        """
        Contains Bitcoin network data overview stats.
        """

        query = """query bitcoinOverviews($last: Int!) {bitcoinOverviews(last: $last) {
            nodes{
                timestamp
                hashpriceUsd
                networkHashrate7D
                networkDiff
                estDiffAdj
                coinbaseRewards24H
                feesBlocks24H
                marketcap
                nextHalvingCount
                nextHalvingDate
                txRateAvg7D
            }
        }}"""
        
        params = {'last': 1}

        return self.request(query, params)

    def get_hashprice(self, inputInterval: str, currency: str) -> requests.Request:
        """
        Returns Bitcoin hashprice for a given interval

        Parameters
        ---------
        inputInterval : str
            intervals to generate the timeseries, options are: `_1_DAY`, `_7_DAYS`, `_1_MONTH`, `_3_MONTHS`, `_1_YEAR` and `ALL`
        currency : str
            currency for ASIC price, options are: `USD`, `BTC`
        """
        if currency.lower() not in ['btc', 'usd']:
            raise Exception(f'Invalid currency input')

        field = f"{currency.lower()}Hashprice"
        query = """query get_hashprice($inputInterval: ChartsInterval!, $first: Int) {{
            getHashprice(inputInterval: $inputInterval, first: $first) {{
                nodes {{
                    timestamp
                    {field}
                }}
            }}
        }}""".format(field=field)
        
        params = {
            'inputInterval': inputInterval,
            'first': 10000
        }
        
        return self.request(query, params)

    def get_network_hashrate(self, inputInterval: str) -> requests.Request:
        """
        Returns the network hashrate for a given interval

        Parameters
        ---------
        inputInterval : str
            intervals to generate the timeseries, options are: `_1_DAY`, `_7_DAYS`, `_1_MONTH`, `_3_MONTHS`, `_1_YEAR` and `ALL`
        """

        query = """query get_network_hashrate($inputInterval: ChartsInterval!, $first: Int) {
            getNetworkHashrate(inputInterval: $inputInterval, first: $first) {
                nodes {
                    timestamp
                    networkHashrate
                }
            }
        }"""
        params = {
            'inputInterval': inputInterval,
            'first': 10000,
        }
        return self.request(query, params)

    def get_network_difficulty(self, inputInterval: str) -> requests.Request:
        """
        Returns the network difficulty

        Parameters
        ---------
        inputInterval : str
            intervals to generate the timeseries, options are: `_3_MONTHS`, `_6_MONTHS`, `_1_YEAR`, `_3_YEAR` and `ALL`
        """

        query = """query get_price_difficulty($inputInterval: ChartsInterval, $inputSlug: String) {
            getChartBySlug(inputInterval: $inputInterval, inputSlug: $inputSlug) {
                data
            }
        }"""
        params = {
            'inputInterval': inputInterval,
            'inputSlug': 'bitcoin-price-and-difficulty',
        }

        result = self.request(query, params)

        for element in result["data"]["getChartBySlug"]["data"]:
            del element["price"]
        return result

    def get_ohlc_prices(self, inputInterval: str) -> requests.Request:
        """
        Returns the Bitcoin OLHC prices at a specified interval

        Parameters
        ---------
        inputInterval : str
            intervals to generate the timeseries, options are: `_1_DAY`, `_7_DAYS`, `_1_MONTH`, `_3_MONTHS`, `_1_YEAR` and `ALL`
        """

        query = """query get_ohlc_prices($inputInterval: ChartsInterval, $inputSlug: String) {
            getChartBySlug(inputInterval: $inputInterval, inputSlug: $inputSlug) {
                data
            }
        }"""
        params = {
            'inputInterval': inputInterval,
            'inputSlug': 'bitcoin-ohlc',
        }
        return self.request(query, params)

    def get_asic_price_index(self, inputInterval: str, currency: str) -> requests.Request:
        """
        Returns the ASIC price index in USD for a given time interval

        Parameters
        ---------
        inputInterval : str
            intervals to generate the timeseries, options are: `_3_MONTHS`, `_6_MONTHS`, `_1_YEAR` and `ALL`
        currency : str
            currency for ASIC price, options are: `USD`, `BTC`
        """

        query = """query get_asic_price_index($inputInterval: ChartsInterval, $inputSlug: String) {
            getChartBySlug(inputInterval: $inputInterval, inputSlug: $inputSlug) {
                data
            }
        }"""

        if currency.lower() not in ['btc', 'usd']:
            raise Exception(f'Invalid currency input')

        params = {
            'inputInterval': inputInterval,
            'inputSlug': f'asic-price-index-{currency.lower()}',
        }
        return self.request(query, params)
    
    def exec(self, method: str, params: Dict[str, Any]) -> requests.Request:
        """
        Helper function for dynamically calling functions safely.

        Parameters
        ----------
        method : str
            Class method to call
        params : dictionary
            Params to construct the method call
        """

        if hasattr(self, method) and callable(getattr(self, method)):
            func = getattr(self, method)

            if not len(params):
                return func()

            args = []
            for arg in params.split(','):
                if arg.isdigit():
                    args.append(
                        int(arg)
                    )  
                    # TODO: get typed arguments. If a str param is passed with integers can be converted incorrectly as int
                else:
                    args.append(arg)

            return func(*args)
        raise Exception(f'failed to execute {method}')

if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option('-e',
                      '--endpoint',
                      dest='host',
                      help='API ENDPOINT',
                      default='https://api.hashrateindex.com/graphql')
    parser.add_option('-k',
                      '--key',
                      dest='key',
                      help='Hashrate Index API Key',
                      default='')
    parser.add_option('-m',
                      '--method',
                      dest='method',
                      help='API Request method',
                      default='POST')
    parser.add_option('-f',
                      '--function',
                      dest='function',
                      help='API Class method',
                      default='')
    parser.add_option('-q',
                      '--query',
                      dest='query',
                      help='API Request query',
                      default='')
    parser.add_option('-p',
                      '--params',
                      dest='params',
                      help='API Request params',
                      default='')
    parser.add_option('-d',
                      '--df',
                      dest='df',
                      help='Pandas DataFrame',
                      default=False)

    options, args = parser.parse_args()

    API = API(options.host, options.key, options.method)
    RESOLVERS = RESOLVERS(options.df)

    if options.query == '':
        if options.function == '':
            raise Exception('must provide function or query')

        if not options.function in dir(API):
            raise Exception('function not found')

    params = ''
    if options.params is not None:
        params = options.params

    try:
        if options.query == '':
            resp = API.exec(options.function, options.params)
        else:
            resp = API.request(options.query, options.params)
        logging.info(resp)

    except Exception as error:
        logging.critical(error, exc_info=True)
        exit(1)

    exit(0)
