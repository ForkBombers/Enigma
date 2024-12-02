import json
import os
from random import shuffle


class Songs_Queue:

    def __init__(self, song_names=None):
        self.file_path = "songs_queue.json"
        if song_names is not None:
            self.queue = song_names
            self.index = 0
            self.current_index = 0
            self.loop_mode = "off"  # Can be "off", "song", or "queue"
            self.save_to_json()
        else:
            self.load_from_json()
        self.user_feedback = {
        }  # In-memory feedback dictionary, no file storage

    def save_to_json(self):
        data = {
            "queue": self.queue,
            "index": self.index,
            "current_index": self.current_index
        }
        with open(self.file_path, 'w') as f:
            json.dump(data, f)

    def load_from_json(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            self.queue = data.get("queue", [])
            self.index = data.get("index", 0)
            self.current_index = data.get("current_index", 0)
        else:
            self.queue = []
            self.index = 0
            self.current_index = 0

    def add_feedback(self, song_name, feedback_type):
        # Store feedback in memory (no persistence)
        if song_name not in self.user_feedback:
            self.user_feedback[song_name] = {"liked": [], "disliked": []}

        if feedback_type == "like":
            if song_name not in self.user_feedback[song_name]["liked"]:
                self.user_feedback[song_name]["liked"].append(song_name)
            # Remove from dislikes if it exists
            if song_name in self.user_feedback[song_name]["disliked"]:
                self.user_feedback[song_name]["disliked"].remove(song_name)
        elif feedback_type == "dislike":
            if song_name not in self.user_feedback[song_name]["disliked"]:
                self.user_feedback[song_name]["disliked"].append(song_name)
            # Remove from likes if it exists
            if song_name in self.user_feedback[song_name]["liked"]:
                self.user_feedback[song_name]["liked"].remove(song_name)

    def toggle_loop(self):
        if self.loop_mode == "off":
            self.loop_mode = "song"
        elif self.loop_mode == "song":
            self.loop_mode = "queue"
        else:
            self.loop_mode = "off"
        return self.loop_mode

    def next_song(self):
        if not self.queue:
            return None
        if self.loop_mode == "song":
            return self.queue[self.index]
        self.index += 1
        if self.index >= len(self.queue):
            if self.loop_mode == "queue":
                self.index = 0
            else:
                self.index = len(self.queue) - 1
        self.current_index = self.index
        self.save_to_json()
        return self.queue[self.index]

    def prev_song(self):
        if not self.queue:
            return None
        if self.loop_mode == "song":
            return self.queue[self.index]
        # Decrement the index and wrap around if needed
        self.index = (self.index - 1) % len(self.queue)
        # self.index -= 1
        # if self.index < 0:
        #     if self.loop_mode == "queue":
        #         self.index = len(self.queue) - 1
        #     else:
        #         self.index = 0
        self.current_index = self.index
        self.save_to_json()
        return self.queue[self.index]

    def replay_current(self):
        if not self.queue:
            return None
        return self.queue[self.index]

    def get_len(self):
        return len(self.queue)

    def return_queue(self):
        return (self.queue, self.current_index)

    def shuffle_queue(self):
        shuffle(self.queue)
        self.save_to_json()
        self.index = 0
        self.current_index = 0
        self.save_to_json()

    def add_to_queue(self, song_name):
        self.queue.append(song_name)
        if len(self.queue) == 1:
            self.index = 0
            self.current_index = 0
        self.save_to_json()
        return len(self.queue) == 1

    def set_current_index(self, index):
        if 0 <= index < len(self.queue):
            self.index = index
            self.current_index = index
            self.save_to_json()
        else:
            raise IndexError("Index out of range")

    def get_song_at_index(self, index):
        if 0 <= index < len(self.queue):
            return self.queue[index]
        else:
            return None

    def jump_to_song(self, song_name):
        for i, song in enumerate(self.queue):
            if song_name.lower() in song.lower():
                self.index = i
                self.current_index = i
                self.save_to_json()
                return song
        return None

    def move_song(self, from_pos, to_pos):
        if 0 <= from_pos < len(self.queue) and 0 <= to_pos < len(self.queue):
            song = self.queue.pop(from_pos)
            self.queue.insert(to_pos, song)
            self.save_to_json()
            return True
        return False

    def get_current_song(self):
        if 0 <= self.current_index < len(self.queue):
            return self.queue[self.current_index]
        return None
