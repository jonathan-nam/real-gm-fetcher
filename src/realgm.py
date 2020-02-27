import requests
import sqlite3
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime

def create_database():
    conn = sqlite3.connect('igm.sqlite')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS team")
    cursor.execute("DROP TABLE IF EXISTS player")
    cursor.execute("DROP TABLE IF EXISTS event")

    cursor.execute("""
    CREATE TABLE team (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE ON CONFLICT IGNORE
    )""")

    # I make the assumption here that players are unique to speed up querying.
    # A situation in which this is a potential problem
    # Transaction 1 - Thanasis Zafiris leaves team A.
    # Transaction 2 - Thanasis Zafiris joins team B.
    # Player in Transaction 2 could be different from player in the first
    
    cursor.execute("""
    CREATE TABLE player(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        team_id INTEGER,
        FOREIGN KEY(team_id) REFERENCES team(id) ON UPDATE CASCADE
    )""")

    cursor.execute("""
    CREATE TABLE event (
        id INTEGER PRIMARY KEY,
        year INTEGER,
        month TEXT,
        weekday TEXT,
        monthday INTEGER,
        player_id INTEGER,
        source_id INTEGER,
        destination_id INTEGER,
        description TEXT,
        FOREIGN KEY(player_id) REFERENCES player(id) ON UPDATE CASCADE,
        FOREIGN KEY(source_id) REFERENCES team(id) ON UPDATE CASCADE,
        FOREIGN KEY(destination_id) REFERENCES team(id) ON UPDATE CASCADE
    )""")

    conn.close()

def populate_database():
    TRANSACTIONS_URL = "https://basketball.realgm.com/international/transactions/"
    year = 2013

    conn = sqlite3.connect('igm.sqlite')
    cursor = conn.cursor()

    for year in range(2005, 2021):
        YEAR_TRANSACTIONS_URL = TRANSACTIONS_URL + str(year)
        r = requests.get(YEAR_TRANSACTIONS_URL)
        print(YEAR_TRANSACTIONS_URL)

        transactions_soup = BeautifulSoup(r.content, "lxml")

        for chart in transactions_soup.find_all("div", class_="portal widget fullpage")[::-1]:

            date = chart.text.splitlines()[1].strip()
            date = datetime.strptime(date, "%B %d, %Y")
            year = date.year
            month = date.strftime("%B")
            weekday = date.strftime("%A")
            monthday = date.day

            for list in chart.find_all("li"):
                # Event_dict as a whole is never used
                # But usage helps with readability
                event_dict = {}
                event_dict.update({'year' : year})
                event_dict.update({'month' : month})
                event_dict.update({'monthday' : monthday})
                event_dict.update({'weekday' : weekday})

                player_link = list.find("a")
                description = list.text
                status = list.find(text=True, recursive=False)
                player = player_link.string
                event_dict.update({'player' : player})

                # Transactions are standardized by starting and ending team.
                # "X leaves Y": starting team - Y, ending team - null
                # "X signs with Y": starting team - null, ending team - Y
                # "X, previously signed with Y, has signed with Z": starting team - Y, ending team - Z

                if "previously" in status:
                    event_dict.update({'source' : player_link.findNext('a').contents[0]})
                    event_dict.update({'destination' : player_link.findNext('a').findNext('a').contents[0]})
                elif "signed" or "joined" in status:
                    event_dict.update({'source' : '-'})
                    event_dict.update({'destination' : player_link.findNext('a').contents[0]})
                elif "left" in status:
                    event_dict.update({'source' : player_link.findNext('a').contents[0]})
                    event_dict.update({'destination' : '-'})
                    
                event_dict.update({'description' : list.text})
                cursor.execute('INSERT INTO team (name) VALUES (?)', (event_dict["source"], ))
                cursor.execute('INSERT INTO team (name) VALUES (?)', (event_dict["destination"], ))
                cursor.execute('SELECT id FROM team WHERE name=?', (event_dict["source"], ))
                source_id = cursor.fetchone()[0] 
                cursor.execute('SELECT id FROM team WHERE name=?', (event_dict["destination"], ))
                destination_id = cursor.fetchone()[0]

                cursor.execute('INSERT INTO player (name, team_id) VALUES (?, ?) ON CONFLICT (name) DO UPDATE SET team_id=?', (event_dict["player"], destination_id, destination_id))
                player_id = cursor.lastrowid
                cursor.execute('INSERT INTO event (year, month, weekday, monthday, description, player_id, source_id, destination_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                        (event_dict["year"], event_dict["month"], event_dict["weekday"], event_dict["monthday"], event_dict["description"], player_id, source_id, destination_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    populate_database()