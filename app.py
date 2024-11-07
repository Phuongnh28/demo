from flask import Flask, request, jsonify
import json
import random

# Load Q-table from file
with open("q_table.json", "r") as f:
    q_table = json.load(f)

app = Flask(__name__)

def choose_action(state, available_actions):
    if state not in q_table:
        return random.choice(available_actions)
    q_values = [q_table.get(f"{state}{a}", 0) for a in available_actions]
    return available_actions[q_values.index(max(q_values))]

@app.route("/get-ai-move", methods=["POST"])
def get_ai_move():
    data = request.get_json()
    board = data["board"]
    state = "".join([str(cell) if cell is not None else "-" for cell in board])
    available_actions = [i for i, cell in enumerate(board) if cell is None]

    action = choose_action(state, available_actions)
    return jsonify({"action": action})

if __name__ == "__main__":
    app.run(debug=True)
