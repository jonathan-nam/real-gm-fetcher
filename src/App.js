import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [table, setTable] = useState(null);

  const playerfetch = async () => {
    const response = await axios.get("http://localhost:3000/player");
    setTable(response.data);
  };

  const teamfetch = async () => {
    const response = await axios.get("http://localhost:3000/team");
    setTable(response.data);
  };

  const transactionfetch = async () => {
    const response = await axios.get("http://localhost:3000/transaction");
    setTable(response.data);
  };

  const tableStyle = {
    margin: "0 auto",
    border: "1px solid"
  };

  return (
    <div className="App">
      <h2>BBall Trade Tracker</h2>
      <div>
        <button className="fetch" onClick={playerfetch}>
          Player Fetch
        </button>
        <input className="player" placeholder="Enter player here" />
      </div>
      <div>
        <button className="fetch" onClick={teamfetch}>
          Team Fetch
        </button>
        <input className="team" placeholder="Enter team here" />
      </div>
      <div>
        <button className="fetch" onClick={transactionfetch}>
          Transaction Fetch
        </button>
        <input className="date" placeholder="Enter date here" />
        <input className="player" placeholder="Enter player here" />
        <input className="team" placeholder="Enter team here" />
      </div>
      <table name="Players" style={tableStyle}>
        <thead>
          <tr>
            <th>Player ID</th>
            <th>Name</th>
            <th>Team ID</th>
          </tr>
        </thead>
        <tbody>
          {table &&
            table.map((entry, index) => {
              return (
                <tr>
                  <th>{entry.player_id}</th>
                  <th>{entry.player_name}</th>
                  <th>{entry.belong_id}</th>
                </tr>
              );
            })}
        </tbody>
      </table>
      <table name="Teams" style={tableStyle}>
        <thead>
          <tr>
            <th>Team ID</th>
            <th>Name</th>
          </tr>
        </thead>
        <tbody>
          {table &&
            table.map((entry, index) => {
              return (
                <tr>
                  <th>{entry.team_id}</th>
                  <th>{entry.team_name}</th>
                </tr>
              );
            })}
        </tbody>
      </table>
      <table name="Transactions" style={tableStyle}>
        <thead>
          <tr>
            <th>Transaction ID</th>
            <th>Year</th>
            <th>Month</th>
            <th>Weekday</th>
            <th>Monthday</th>
            <th>Description</th>
            <th>Source ID</th>
            <th>Destination ID</th>
            <th>Player ID</th>
          </tr>
        </thead>
        <tbody>
          {table &&
            table.map((entry, index) => {
              return (
                <tr>
                  <th>{entry.transaction_id}</th>
                  <th>{entry.year}</th>
                  <th>{entry.month}</th>
                  <th>{entry.weekday}</th>
                  <th>{entry.monthday}</th>
                  <th>{entry.description}</th>
                  <th>{entry.source_id}</th>
                  <th>{entry.dest_id}</th>
                  <th>{entry.player}</th>
                </tr>
              );
            })}
        </tbody>
      </table>
    </div>
  );
}

export default App;
