# Luxor-HashrateIndex Python Library and Command Line GraphQL API Client

We've decided to open-source our datasets for the community to build features, perform research and bring even more transparency to the Bitcoin mining industry.

Feel free to send your projects or questions our way to hashrateindex@luxor.tech or @hashrateindex on Twitter. Looking forward to see what y'all build!

## Get Started

To get started, you will need the following basic information:

- Endpoint: `https://api.hashrateindex.com/graphql`
- API Key: Hashrate Index Silver tier and above members gain enhanced access, including an API key for real-time data. For special requests or custom solutions, contact us at hashrateindex@luxor.tech.

**Code Snippet**

```
from hashrateindex import API
from resolvers import RESOLVERS

API = API(host = 'https://api.hashrateindex.com/graphql', method = 'POST', key = 'KEY')
RESOLVERS = RESOLVERS(df = False)

resp = API.method(parameters)
resolved = RESOLVERS.method(resp)
```

## Command Line Usage

To get started and get params help run:

```
python hashrateindex.py -h
```

Result:

```
Options:
  -h, --help
                        show this help message and exit
  -e HOST, --endpoint=HOST
                        API ENDPOINT
  -k KEY, --key=KEY
                        Profile API Key
  -m METHOD, --method=METHOD
                        API Request method
  -f FUNCTION, --function=FUNCTION
                        API Class method
  -q QUERY, --method=QUERY
                        API Request query
  -p PARAMS, --params=PARAMS
                        API Request params
  -d DF, --df=DF
                        Pandas DataFrame
```

Example usage:

```
python3 hashrateindex.py -k KEY -f get_bitcoin_overview
python3 hashrateindex.py -k KEY -f get_hashprice -p "_1_DAY",BTC
python3 hashrateindex.py -k KEY -f get_network_hashrate -p "_3_MONTHS"
python3 hashrateindex.py -k KEY -f get_network_difficulty -p "_3_MONTHS"
python3 hashrateindex.py -k KEY -f get_ohlc_prices -p "_3_MONTHS"
python3 hashrateindex.py -k KEY -f get_asic_price_index -p "_3_MONTHS",BTC
```
