# HSN-TSN

## Description
I wanted to scrape vehicle data from the European automotive website ([kfzteile24](https://www..de/) and [die versicherer](https://www.dieversicherer.de/versicherer/auto/typklassenabfrage)) and compare it with the data in the company's SQL database to verify accuracy. So, I developed a Python program that connects to the SQL database, automatically extracts relevant keywords, and transmits them to the website for automated searching. The program records all necessary search results, and I also built a GUI to make it easier for staff to use.

## Dependencies
* [Tkinter](https://docs.python.org/3/library/tkinter.html)
* [requests](https://pypi.org/project/requests/)
* [pandas](https://pandas.pydata.org/)
* [selenium](https://pypi.org/project/selenium/)
* [lxml](https://pypi.org/project/lxml/)

## File introduction
- **crawler1bynetwork.py**: Use the Network tab in the webpage's source code ([kfzteile24](https://www..de/)) to identify changes after searching, download the required data, and save it in CSV format.
- **crawler1.py**: Use the Python library Selenium to automate web browsing ([kfzteile24](https://www..de/)), extract the required data, and save it in CSV format.
- **crawler2.py**: Use the Python library Selenium to automate web browsing ([die versicherer](https://www.dieversicherer.de/versicherer/auto/typklassenabfrage)), extract the required data, and save it in CSV format.
- **HSN_TSN_app.py**: Use python library Tkinter to create a simple GUI with buttons to select the start and end dates for the search. After entering the dates, click the download button to retrieve the data within the specified time range.
