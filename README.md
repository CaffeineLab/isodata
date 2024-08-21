# ISODATA
This project just helps you get data from the major energy markets.  Currently PJM Public reports are supported.  Also - there is no 'secret-sauce' in here that you cannot glean from market documentation.

## Roadmap
After making this an installable PIP package, the future simply entails pulling all documents from all markets and then providing a simple consumer that will convert the response into a dataframe or dictionary for easy loading into backend systems.

## Installing And Documentation
```
pip install python-isodata
```
https://python-isodata.readthedocs.io/en/latest/


## Credentials
Your credential should look like this, and if required, your Certificate needs to be supplied just as two file paths would be to a requests post or get.
```
{
  "user": "caffeinelab",
  "credentials":
  {
    "pjm":
    {
      "username": "***USERNAME***",
      "password": "***PASSWORD***"
    },    
    "ercot_public_api":
      {
        "username": "***USERNAME***",
        "password": "***PASSWORD***",
        "primary_key": "***API_PRIMARY_KEY***",
        "auth_url": "https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/B2C_1_PUBAPI-ROPC-FLOW/oauth2/v2.0/token?username={username}&password={password}&grant_type=password&scope=openid+fec253ea-0d06-4272-a5e6-b478baeecd70+offline_access&client_id=fec253ea-0d06-4272-a5e6-b478baeecd70&response_type=id_token"
      }
  }
}
```

ERCOT User Guide: 

https://developer.ercot.com/applications/pubapi/user-guide/registration-and-authentication/

## Querying PJM
**market_day** is magical?

If you pass it as a string it will be converted into a datetime and if you forget it
altogether it just becomes datetime.utc_now().  As a side note - remember that if you
are using .isoformat(), you'll want to replace the microseconds with 0 before submitting
to the API.

```
from pathlib import Path
from isodata import Session

pjm = Session('pjm')
pjm.authorize(username=creds['credentials']['pjm']['username'],
              password=creds['credentials']['pjm']['password'],
              certificate=(path_cert, path_key))

for fp in Path('./isodata/pjm/query').glob('*.py'):
    logger.info(fp.name.replace('.py', ''))
    report = pjm.query(report=fp.name.replace('.py', ''))
    if report is not None:
        logger.debug(report[:120])

                  
```
## PJM Market Notes
it is on the client to procure appropriate credentials and possible NAESB approved certificate for connecting to the market API(s).

More information can be found on the PJM website:

https://www.pjm.com/markets-and-operations/etools/markets-gateway

https://www.pjm.com/-/media/etools/security/pki-faqs.ashx

https://www.pjm.com/-/media/etools/security/pki-authentication-guide.ashx

https://www.pjm.com/-/media/etools/markets-gateway/external-interface-specification-guide.ashx

While PJM does publish a wsdl (in a word doc) it hasn't been updated since 2016,
this along with there being no true service on the backend allows us to bypass more
complicated libraries for submitting simple requests for reports.  Because of this, 
the majority of pjm queries are just simple string builders with some simple token 
replacements.  If you want/need to use LXML to create your request, there is an 
example in pjm.query.QueryBidNodes

## Querying ERCOT

For a list of all Public Reports, refer to the ERCOT api-specs repo

https://github.com/ercot/api-specs/blob/main/pubapi/pubapi-apim-api.json

```
from isodata.sessions import Session

ercot = Session('ercot_public')
ercot.authorize(username=creds['credentials']['ercot_public_api']['username'],
                password=creds['credentials']['ercot_public_api']['password'],
                primary_key=creds['credentials']['ercot_public_api']['primary_key'],
                auth_url=creds['credentials']['ercot_public_api']['auth_url'])

# Fetch 'SCED Shadow Prices and Binding Transmission Constraints'
emil = 'NP6-86-CD'

# Fetch the list of documents on the first page
report_list, count = ercot.fetch_listing(emil_id=emil, page=0)

# Fetch the first file and save it locally, the 2nd element
# in the tuple is the link to the report.
data_file = ercot.fetch_url(report_list[0][2], 'path/to/save/report')

# Do what you want with the data in the file from here.
# Beware of zips with multiple files, or data_files that 
# are just plain .csv files.  An example for NP6-86-CD data is:
df = pd.read_csv(data_file, compression='zip')

```

## Additional Tools

[Caffeine Lab](https://caffeinelab.com) will publish more tools for energy traders at:

https://caffeinelab.com/mining-energy-data.html

