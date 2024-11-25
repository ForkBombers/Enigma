import unittest
from src.songs_queue import Songs_Queue


class TestSongsQueue(unittest.TestCase):

    def setUp(self):
        self.sample_songs = ["Song A", "Song B", "Song C", "Song D", "Song E"]
        self.queue = Songs_Queue(self.sample_songs)

    def test_init(self):
        self.assertEqual(self.queue.queue, self.sample_songs)
        self.assertEqual(self.queue.index, 0)
        self.assertEqual(self.queue.current_index, 0)

    def test_next_song(self):
        # Test normal next song functionality
        for i in range(len(self.sample_songs)):
            expected_song = self.sample_songs[(i + 1) % len(self.sample_songs)]
            #self.assertEqual(self.queue.next_song(), self.sample_songs[i])
            self.assertEqual(self.queue.next_song(), expected_song)

        # Test wrapping around to the beginning
        self.assertEqual(self.queue.next_song(), self.sample_songs[1])

    def test_prev_song(self):
        # Move to the end of the queue
        for _ in range(len(self.sample_songs)):
            self.queue.next_song()

        # Test normal previous song functionality
        for i in range(len(self.sample_songs) - 1, -1, -1):
            self.assertEqual(self.queue.prev_song(), self.sample_songs[i])

        # Test wrapping around to the end
        self.assertEqual(self.queue.prev_song(), self.sample_songs[-1])

    def test_get_len(self):
        self.assertEqual(self.queue.get_len(), len(self.sample_songs))

    def test_return_queue(self):
        returned_queue, current_index = self.queue.return_queue()
        self.assertEqual(returned_queue, self.sample_songs)
        self.assertEqual(current_index, 0)

        # Test after moving to next song
        self.queue.next_song()
        returned_queue, current_index = self.queue.return_queue()
        self.assertEqual(
            current_index,
            1)  # Because next_song() updates current_index after returning

    def test_shuffle_queue(self):
        original_queue = self.queue.queue.copy()
        self.queue.shuffle_queue()
        self.assertNotEqual(self.queue.queue, original_queue)
        self.assertEqual(set(self.queue.queue), set(original_queue))

    def test_add_to_queue(self):
        new_song = "New Song"
        original_length = self.queue.get_len()
        self.queue.add_to_queue(new_song)
        self.assertEqual(self.queue.get_len(), original_length + 1)
        self.assertEqual(self.queue.queue[-1], new_song)


    def test_jump_to_song(self):
        self.assertEqual(self.queue.jump_to_song("Song C"), "Song C")
        self.assertEqual(self.queue.index, 2)
        self.assertEqual(self.queue.current_index, 2)
        self.assertIsNone(self.queue.jump_to_song("Nonexistent Song"))

    def test_get_current_song(self):
        self.assertEqual(self.queue.get_current_song(), "Song A")
        self.queue.next_song()
        self.assertEqual(self.queue.get_current_song(), "Song B")

    def test_empty_queue(self):
        empty_queue = Songs_Queue([])
        self.assertIsNone(empty_queue.next_song())
        self.assertIsNone(empty_queue.prev_song())
        self.assertIsNone(empty_queue.get_current_song())

    def test_set_current_index(self):
        self.queue.set_current_index(2)
        self.assertEqual(self.queue.index, 2)
        self.assertEqual(self.queue.current_index, 2)
        with self.assertRaises(IndexError):
            self.queue.set_current_index(10)

    def test_get_song_at_index(self):
        self.assertEqual(self.queue.get_song_at_index(0), "Song A")
        self.assertEqual(self.queue.get_song_at_index(2), "Song C")
        self.assertIsNone(self.queue.get_song_at_index(10))

    def test_save_and_load_json(self):
        original_queue = self.queue.queue.copy()
        original_index = self.queue.index
        original_current_index = self.queue.current_index
    
        self.queue.save_to_json()
        new_queue = Songs_Queue()  # This should load from the JSON file
    
        self.assertEqual(new_queue.queue, original_queue)
        self.assertEqual(new_queue.index, original_index)
        self.assertEqual(new_queue.current_index, original_current_index)


if __name__ == '__main__':
    unittest.main()
