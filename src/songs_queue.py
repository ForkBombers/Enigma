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
            self.save_to_json()
        else:
            self.load_from_json()

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

    def next_song(self):
        if not self.queue:
            return None
        if self.index >= len(self.queue):
            self.index = 0
        song = self.queue[self.index]
        self.current_index = self.index
        self.index += 1
        self.save_to_json()
        return song

    def prev_song(self):
        if not self.queue:
            return None
        self.index -= 1
        if self.index < 0:
            self.index = len(self.queue) - 1
        self.current_index = self.index
        self.save_to_json()
        return self.queue[self.index]

    def get_len(self):
        return len(self.queue)

    def return_queue(self):
        return (self.queue, self.current_index)

    def shuffle_queue(self):
        shuffle(self.queue)
        self.save_to_json()

    def add_to_queue(self, song_name):
        self.queue.append(song_name)
        self.save_to_json()
