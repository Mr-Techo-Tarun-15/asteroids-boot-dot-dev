import inspect
import json
import math
from datetime import datetime

__all__ = ["log_state", "log_event"]

_FPS = 60
_MAX_SECONDS = 16
_SPRITE_SAMPLE_LIMIT = 10

_frame_count = 0
_state_log_initialized = False
_event_log_initialized = False
_start_time = datetime.now()


def log_state(updatable, drawable, asteroids, shots):
    global _frame_count, _state_log_initialized

    # Stop logging after `_MAX_SECONDS` seconds
    if _frame_count > _FPS * _MAX_SECONDS:
        return

    # Take a snapshot approx. once per second
    _frame_count += 1
    if _frame_count % _FPS != 0:
        return

    now = datetime.now()

    screen_size = []
    game_state = {}

    # --- NEW: Process the 'updatable' group ---
    sprites_data_updatable = []
    for i, sprite in enumerate(updatable):
        if i >= _SPRITE_SAMPLE_LIMIT:
            break
        sprite_info = {"type": sprite.__class__.__name__}

        # Populate sprite_info with attributes
        if hasattr(sprite, "position"):
            sprite_info["pos"] = [
                round(sprite.position.x, 2),
                round(sprite.position.y, 2),
            ]

        if hasattr(sprite, "velocity"):
            sprite_info["vel"] = [
                round(sprite.velocity.x, 2),
                round(sprite.velocity.y, 2),
            ]

        if hasattr(sprite, "radius"):
            sprite_info["rad"] = sprite.radius

        if hasattr(sprite, "rotation"):
            sprite_info["rot"] = round(sprite.rotation, 2)

        sprites_data_updatable.append(sprite_info) # Append ONLY after sprite_info is fully populated

    # Add the updatable group's data to game_state
    game_state["updatable"] = {"count": len(updatable), "sprites": sprites_data_updatable}


    # --- NEW: Process the 'drawable' group ---
    sprites_data_drawable = []
    for i, sprite in enumerate(drawable):
        if i >= _SPRITE_SAMPLE_LIMIT:
            break
        sprite_info = {"type": sprite.__class__.__name__} # Initialize sprite_info first

        # Populate sprite_info with attributes
        if hasattr(sprite, "position"):
            sprite_info["pos"] = [
                round(sprite.position.x, 2),
                round(sprite.position.y, 2),
            ]

        if hasattr(sprite, "velocity"):
            sprite_info["vel"] = [
                round(sprite.velocity.x, 2),
                round(sprite.velocity.y, 2),
            ]

        if hasattr(sprite, "radius"):
            sprite_info["rad"] = sprite.radius

        if hasattr(sprite, "rotation"):
            sprite_info["rot"] = round(sprite.rotation, 2)

        sprites_data_drawable.append(sprite_info) # Append ONLY after sprite_info is fully populated

    # Add the drawable group's data to game_state
    game_state["drawable"] = {"count": len(drawable), "sprites": sprites_data_drawable}
    
    sprites_data_asteroids = []
    for i, sprite in enumerate(asteroids):
        if i >= _SPRITE_SAMPLE_LIMIT:
            break
        sprite_info = {"type": sprite.__class__.__name__}

        # Populate sprite_info with attributes
        if hasattr(sprite, "position"):
            sprite_info["pos"] = [
                round(sprite.position.x, 2),
                round(sprite.position.y, 2),
            ]

        if hasattr(sprite, "velocity"):
            sprite_info["vel"] = [
                round(sprite.velocity.x, 2),
                round(sprite.velocity.y, 2),
            ]

        if hasattr(sprite, "radius"):
            sprite_info["rad"] = sprite.radius

        if hasattr(sprite, "rotation"):
            sprite_info["rot"] = round(sprite.rotation, 2)

        sprites_data_asteroids.append(sprite_info) # Append ONLY after sprite_info is fully populated

    # Add the asteroids' group's data to game_state
    game_state["asteroids"] = {"count": len(asteroids), "sprites": sprites_data_asteroids}

    sprites_data_shots = []
    for i, sprite in enumerate(shots):
        if i >= _SPRITE_SAMPLE_LIMIT:
            break
        sprite_info = {"type": sprite.__class__.__name__}

        # Populate sprite_info with attributes
        if hasattr(sprite, "position"):
            sprite_info["pos"] = [
                round(sprite.position.x, 2),
                round(sprite.position.y, 2),
            ]

        if hasattr(sprite, "velocity"):
            sprite_info["vel"] = [
                round(sprite.velocity.x, 2),
                round(sprite.velocity.y, 2),
            ]

        if hasattr(sprite, "radius"):
            sprite_info["rad"] = sprite.radius

        if hasattr(sprite, "rotation"):
            sprite_info["rot"] = round(sprite.rotation, 2)

        sprites_data_shots.append(sprite_info) # Append ONLY after sprite_info is fully populated

    # Add the asteroids' group's data to game_state
    game_state["shots"] = {"count": len(shots), "sprites": sprites_data_shots}

    entry = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "screen_size": screen_size, # This will be empty, as we're not auto-detecting screen size
        **game_state, # This unpacks our collected 'updatable' and 'drawable' data
    }

    # New log file on each run
    mode = "w" if not _state_log_initialized else "a"
    with open("game_state.jsonl", mode) as f:
        f.write(json.dumps(entry) + "\n")

    _state_log_initialized = True

# The log_event function remains unchanged
def log_event(event_type, **details):
    global _event_log_initialized

    now = datetime.now()

    event = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "type": event_type,
        **details,
    }

    mode = "w" if not _event_log_initialized else "a"
    with open("game_events.jsonl", mode) as f:
        f.write(json.dumps(event) + "\n")

    _event_log_initialized = True