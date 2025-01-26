# Task for Kiwi.com 2022 april

Create an application that is able to parse information about flight from email and return it in structured python dictionary. Your application should be able to parse emails from `Norwegian airlines` and `Latam airlines`. HTML files for emails are included in `data` directory.

You can create python script, CLI application or web application (choice is up to you).

Example of output for email `18304199.html`:

```
{
	"reservation_number": "P6UZTX",
	"old_flights": [
		{
			"carrier": "DY",
			"carrier_number": "7196",
			"departure": {
				"airport": "BARCELONA",
				"airport_iata": "BCN",
				"datetime": datetime.datetime(2018, 9, 30, 19, 40),
			},
			"arrival": {
				"airport": "NEWARK LIBERTY INTERNATIONAL AIRPORT",
				"airport_iata": "EWR",
				"datetime": datetime.datetime(2018, 9, 30, 22, 15),
			},
		},
	],
	"new_flights": [
		{
			"carrier": "DY",
			"carrier_number": "7196",
			"departure": {
				"airport": "BARCELONA",
				"airport_iata": "BCN",
				"datetime": datetime.datetime(2018, 9, 30, 18, 25),
			},
			"arrival": {
				"airport": "NEWARK LIBERTY INTERNATIONAL AIRPORT",
				"airport_iata": "EWR",
				"datetime": datetime.datetime(2018, 9, 30, 21, 0),
			},
		},
	],
}
```

# Useful python modules

For parsing of html page you can use useful python modules:

- `re` (https://docs.python.org/3/library/re.html)
- `lxml` (https://lxml.de/lxmlhtml.html)
- `bs4` (https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- `requests-html` (https://html.python-requests.org/)

For working with json:

- `json` (https://docs.python.org/3/library/json.html)

