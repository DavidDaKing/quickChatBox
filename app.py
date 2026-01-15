from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
socketio = SocketIO(app, cors_allowed_origins="*")

@app.get("/")
def index():
    return render_template("index.html")

# Redirect any joining user to --> /join 
@socketio.on("join")
def on_join(data):
    pass

@socketio.on("chat")
def on_chat(data):
    room = (data.get("room") or "default").strip()
    name = (data.get("name") or "User").strip()[:32]
    text = (data.get("text") or "").strip()
    if not text:
        return
    payload = {"room": room, "name": name, "text": text, "ts": int(time.time() * 1000)}
    emit("chat", payload, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=80)

