import json
from datetime import datetime

from core.storage import data_path


ROBOT_DIR = data_path("robotics")
STATE_FILE = data_path("robotics", "robot_state.json")
LOG_FILE = data_path("logs", "robotics.log")


def initialize():
    ROBOT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not STATE_FILE.is_file():
        state = {
            "robot_name": "RIGAN ROBOT",
            "position_x": 0,
            "position_y": 0,
            "direction": "NORTH",
            "status": "STOPPED"
        }

        save_state(state)


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=4)


def get_state():
    initialize()

    with open(STATE_FILE, encoding="utf-8") as file:
        return json.load(file)


def log_action(action):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"{datetime.now()} | {action}\n"
        )


def move_robot(direction):
    state = get_state()

    movements = {
        "NORTH": (0, 1),
        "SOUTH": (0, -1),
        "EAST": (1, 0),
        "WEST": (-1, 0)
    }

    direction = direction.upper()

    if direction not in movements:
        return "ERROR: UNKNOWN DIRECTION"

    dx, dy = movements[direction]

    state["position_x"] += dx
    state["position_y"] += dy
    state["direction"] = direction
    state["status"] = "MOVING"

    save_state(state)
    log_action(f"Robot moved {direction}")

    return "ROBOT MOVED SUCCESSFULLY"


def stop_robot():
    state = get_state()
    state["status"] = "STOPPED"

    save_state(state)
    log_action("Robot stopped")

    return "ROBOT STOPPED"


def robot_status():
    return get_state()


def engine_status():
    return {
        "engine": "RIGAN ROBOTICS ENGINE",
        "status": "ACTIVE",
        "mode": "OFFLINE SIMULATION"
    }
