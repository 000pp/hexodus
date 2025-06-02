import sqlite3
import argparse
from flask import Flask, render_template

from rich.console import Console
console = Console()

from pathlib import Path
import subprocess, sys, os
from signal import SIGTERM
from os import killpg

def start_flask():
    pid_file = Path(os.path.expanduser("~")) / ".hexodus" / "flask.pid"
    pid_file.parent.mkdir(exist_ok=True)

    if pid_file.exists():
        pid = int(pid_file.read_text())
        try:
            os.kill(pid, 0)
            console.print(f"[[yellow]![/]] Web app already running on http://127.0.0.1:1337 - (PID: [yellow]{pid}[/])")
            return
        except ProcessLookupError:
            pid_file.unlink()

    proc = subprocess.Popen(
        [sys.executable, "-m", "webapp", "--port", "1337"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    pid_file.write_text(str(proc.pid))
    console.print(f"[[green]+[/]] Web app started - http://127.0.0.1:1337 - (PID: [yellow]{proc.pid}[/])")


def stop_flask():
    pid_file = Path(os.path.expanduser("~")) / ".hexodus" / "flask.pid"
    if not pid_file.exists():
        console.print("[[yellow]![/]] No running web app found")
        return

    pid = int(pid_file.read_text())
    try:
        killpg(pid, SIGTERM)
        console.print(f"[[green]+[/]] Web app stopped successfully ([yellow]{pid}[/])")
    except ProcessLookupError:
        console.print(f"[[red]x[/]] Web app not found ([yellow]{pid}[/])")
    finally:
        pid_file.unlink()

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates")
    )

    @app.route("/")
    def index():
        db_path = os.path.join(os.path.expanduser("~"), ".hexodus", "data.db")
        conn = sqlite3.connect(db_path)
        sqlite_cursor = conn.cursor()

        sqlite_cursor.execute("PRAGMA table_info(data);")
        cols = [row[1] for row in sqlite_cursor.fetchall()]
        profiles = [c for c in cols if c not in ("module", "id")]

        sqlite_cursor.execute("SELECT * FROM data;")
        rows = sqlite_cursor.fetchall()
        conn.close()

        modules = []
        for row in rows:
            entry = { cols[i]: row[i] for i in range(len(cols)) }
            modules.append(entry)

        return render_template("index.html",
                               modules=modules,
                               profiles=profiles)

    return app

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=1337)
    args = p.parse_args()
    app = create_app()
    app.run(host="127.0.0.1", port=args.port, debug=False)