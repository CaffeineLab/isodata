# isodata

Your credential should look like this, and your PJM PKI Certificate needs to be supplied just as two file paths would be to a requests post or get.  More on this later.
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
To retrieve data:
```
from isodata import Session

pjm = Session('pjm')
pjm.authorize(username=creds['credentials']['pjm']['username'],
              password=creds['credentials']['pjm']['password'],
              certificate=(path_cert, path_key))
print(pjm.query(report='QueryBindingLimits', market_day="2023-10-19"))
                  
```