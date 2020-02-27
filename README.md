![Interface](public/sample.png)

# Introduction
Real GM Fetcher is designed to help individuals query international basketball transactions. Unlike NBA transactions, this information is harder to find and not as readily publicized. Using this tool can provide valuable insights quickly. React, Python and SQL are used in tandem to create a micro full-stack application.

# Requirements
Listed in [requirements.txt](requirements.txt).  
This application uses React.js to render the DOM. Make sure to install React using your JS package manager.

# Files
[realgm.py](src/realgm.py) is used to populate the SQL database.  
[server.py](src/server.py) configures a local Flask server.   
[App.js](src/App.js) calls endpoints and renders the DOM using React components.

# Instructions  
Fetch data. This will populate an .sqlite file. Navigate to src and run:  
```python
python realgm.py
```
The application is configured to run through a local Flask server. This will provide access points to the sqlite file. Run: 
```python
python server.py
```
The local host will return a JSON. To interact with the web interface, go to https://p1dsd.csb.app/
