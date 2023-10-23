# ISODATA
This project just helps you get data from the major energy markets.  Currently PJM Public reports are supported.

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
    }
  }
}
```
## Querying
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

