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
    return sorted(get_users_and_hours(), key=lambda x: x["gpu_time"], reverse=True)

html_content = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
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
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        footer {
            margin-top: 20px;
            font-size: 0.9rem;
        }
    </style>
    <script>
        async function fetchLeaderboard() {
            const response = await fetch('/leaderboard');
            const data = await response.json();
            const tableBody = document.getElementById('leaderboard-body');
            tableBody.innerHTML = '';
            data.forEach(entry => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${entry.user}</td><td>${entry.gpu_time} hours</td>`;
                tableBody.appendChild(row);
            });
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
                <th>User</th>
                <th>GPU Time Used</th>
            </tr>
        </thead>
        <tbody id=\"leaderboard-body\">
        </tbody>
    </table>
    <footer>
       <a href="https://github.com/Wicwik/devana-leaderboard" target="_blank">GitHub</a>
    </footer>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def get_homepage():
    return html_content
