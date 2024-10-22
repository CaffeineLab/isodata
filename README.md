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

Important - do not change the ercot_public_api.auth_url.  
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

## Querying ERCOT Public API

Important - ERCOT throttles API usage, it is described as 30 API Calls per minute
so you may find yourself with 4xx errors from the service and then stuck waiting out
the time.  For simplicity, setting the throttle for 1 call per 2 seconds works well
enough.  More aggressive strategies may gain a bit of performance.  Finally, the rate
limit appears to be on the account, so be aware of this when pulling multiple reports,
and yes, you probably can do what you are thinking to get around it.

For a list of all Public Reports, refer to the ERCOT api-specs repo

https://github.com/ercot/api-specs/blob/main/pubapi/pubapi-apim-api.json

```
import json
import os
from isodata.src.isodata.sessions import Session

ercot = Session('ercot_public')
ercot.authorize(username=os.getenv('ERCOT_PUBLIC_USERNAME'),
                password=os.getenv('ERCOT_PUBLIC_PASSWORD'),
                primary_key=os.getenv('ERCOT_PUBLIC_PRIMARYKEY'),
                auth_url=os.getenv('ERCOT_PUBLIC_AUTHURL'))

# Retrieve the public report: SCED Shadow Prices and Binding Transmission Constraints
emil = 'NP6-86-CD'
page = 1
report_list, meta = ercot.fetch_listing(emil_id=emil, page=page)
print(f'{emil} Page {page} Returned {len(report_list)} documents\n')
print(json.dumps(meta, indent=4))

# Retrieve the first (most recent) file in the document list.
# Will raise a FileNotFound error if it cannot retrieve from ERCOT
data_file = ercot.fetch_url(report_list[0][2], f'/documents/ercot/{emil}')
```

Results should look similar to this:
```
NP6-86-CD Page 1 Returned 1000 documents

{
    "totalRecords": 103492,
    "pageSize": 1000,
    "totalPages": 104,
    "currentPage": 1,
    "query": {
        "parameterCount": 0,
        "parameters": {},
        "sortedBy": "postDatetime: DESC"
    }
}
```

## Querying ERCOT Private EMIL Documents

Using a certificate to retrieve the ERCOT private reports starts with breaking
the .pfx file into the discrete components for use with Python Requests Package.

```
openssl.exe pkcs12 -in your_account.pfx -clcerts -nokeys -out your_account.cert
openssl.exe pkcs12 -in your_account.pfx -nocerts -out your_account.key
```

Once you have the two components, you'll pass them to the authorize function.
Plenty of ways to secure your key, please don't expose it.

```
emil = "12335"

# Make sure this folder exists, we'll create it in the future.
out_box = f'/ercot_reports/{emil}'

cert_file = '/ercot_reports/your_account.cert'
key_file = '/ercot_reports/your_account.key'

ercot = Session(market='ercot_private', loglevel="INFO")
ercot.authorize(cert=(cert_file, key_file))
data, meta = ercot.fetch_listing(report_type_id=emil)
report = ercot.fetch_doc(data[0], out_box)
```



## Logging
The session now supports a parameter for setting the log level.  The default is
for no logging messages to be displayed.  Use the name of the log level to set the
minimum level to display to stdout.

```
# Example stdout logging
ercot = Session('ercot_public', loglevel='INFO')
```



## Additional Links and Tools

[PyPi](https://pypi.org/project/python-isodata/0.0.16/) published for simple PIP installation.

[Caffeine Lab](https://caffeinelab.com) will publish more tools for energy traders at:

https://caffeinelab.com/mining-energy-data.html

[Energy Market Montitor](https://energymarketmonitor.com) will publish some simple reports with data retrieved by python-isodata.

[ERCOT Constraints](https://energymarketmonitor.com/constraints) will publish some simple reports with data retrieved by python-isodata.

