from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse
from .influx import get_users_and_hours

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserGPUTime(BaseModel):
    user: str
    gpu_time: int

@app.get("/leaderboard", response_model=List[UserGPUTime])
def get_leaderboard():
    print(get_users_and_hours())
    return get_users_and_hours()

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Devana Leaderboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #f4f4f4;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
        }
        table {
            width: 60%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }
        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #007BFF;
            color: white;
            cursor: pointer;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
    </style>
    <script>
        async function fetchLeaderboard() {
            const response = await fetch('/leaderboard');
            const data = await response.json();
            populateTable(data);
        }

        function populateTable(data) {
            const tableBody = document.getElementById('leaderboard-body');
            tableBody.innerHTML = '';
            data.forEach(entry => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${entry.user}</td><td>${entry.gpu_time} hours</td>`;
                tableBody.appendChild(row);
            });
        }

        function sortTable(columnIndex, isNumeric = false) {
            const table = document.querySelector("table");
            const tbody = document.getElementById("leaderboard-body");
            const rows = Array.from(tbody.querySelectorAll("tr"));

            const sortedRows = rows.sort((a, b) => {
                const aValue = a.cells[columnIndex].textContent.trim();
                const bValue = b.cells[columnIndex].textContent.trim();
                
                if (isNumeric) {
                    return parseFloat(aValue) - parseFloat(bValue);
                } else {
                    return aValue.localeCompare(bValue);
                }
            });

            tbody.innerHTML = '';
            sortedRows.forEach(row => tbody.appendChild(row));
        }

        setInterval(fetchLeaderboard, 5000);
        window.onload = fetchLeaderboard;
    </script>
</head>
<body>
    <h1>Devana Leaderboard</h1>
    <table>
        <thead>
            <tr>
                <th onclick="sortTable(0, false)">User</th>
                <th onclick="sortTable(1, true)">GPU Time Used</th>
            </tr>
        </thead>
        <tbody id="leaderboard-body">
        </tbody>
    </table>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def get_homepage():
    return html_content
