# BBall Trade Tracker
![Interface](public/sample.png)

# Introduction
BBall Trade Tracker is designed to help individuals find information on basketball transactions outside of the NBA. Unlike NBA contracts, international contract information is harder to find and not as readily publicized. Users can find when players are traded, how frequently teams sign and trade, and gain valuable insights quickly. To obtain the data, I use Python's BeautifulSoup to scrape data from Real GM's international transaction database. React, Python, Flask, and SQL are used in tandem to create a micro full-stack application. Feel free to play with the source yourself and send me any questions you have.

# Requirements
Python dependencies are listed in [requirements.txt](requirements.txt). To install dependencies, run:  
```bash
pip install -r requirements.txt
```
Node modules are purposely excluded from this repository. To install dependencies, run:
```bash
npm install
```

# Files
[realgm.py](src/realgm.py) is used to populate the SQL database.  
[server.py](src/server.py) configures a local Flask server.   
[App.js](src/App.js) renders the DOM using React components.

# Instructions  
#### Fetch data #### 
This will populate an .sqlite file. Navigate to src and run:  
```bash
python realgm.py
```
This script can be run sparingly. Rerun it to update the database.
#### Configure local server ####
Set up a local Flask server to access the database. This will provide access points to the sqlite file. Run:   
```bash
python server.py
```
#### Run React ####
To start the React application, Run:  
```bash
npm start
```


