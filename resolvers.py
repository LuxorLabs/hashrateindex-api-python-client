# import packages
import pandas as pd
from typing import Dict, Any, Union

class RESOLVERS:
    """
    A class used to resolve (format) GraphQL API responses into a Python list 
    or Pandas DataFrame from HashrateIndex API.

    Methods
    -------
    ""

    """
    def __init__(self, df: bool = False):
        """
        Parameters
        ----------
        df : boolean
            A boolean flag that determines the output of each method. Default = True.
        """

        self.df = df

    
    def resolve_get_bitcoin_overview(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        
        data = json['data']['bitcoinOverviews']['nodes']
        
        if self.df:
            return pd.DataFrame(data)
        else:
            return data
    
    def resolve_get_hashprice(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        
        data = json['data']['getHashprice']['nodes']
        
        if self.df: 
            return pd.DataFrame(data)
        else:
            return data
    
    def resolve_get_network_hashrate(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        
        data = json['data']['getNetworkHashrate']['nodes']
        
        if self.df:
            return pd.DataFrame(data)
        else:
            return data
    
    def resolve_get_network_difficulty(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        
        data = json['data']['getChartBySlug']['data']
        
        if self.df:
            return pd.DataFrame(data)
        else:
            return data
    
    def resolve_get_ohlc_prices(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        
        data = json['data']['getChartBySlug']['data']
        
        if self.df:
            return pd.DataFrame(data)
        else:
            return data
    
    def resolve_get_asic_price_index(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        
        data = json['data']['getChartBySlug']['data']
        
        if self.df:
            return pd.DataFrame(data)
        else:
            return data
    
