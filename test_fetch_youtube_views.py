import unittest
from fetch_youtube_views import fetch_youtube_views

class TestFetchYouTubeViews(unittest.TestCase):
    def test_real_youtube_video(self):
        # 這裡請填入一個公開的 YouTube 影片連結
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        views = fetch_youtube_views(video_url)
        self.assertIsInstance(views, int)
        self.assertGreater(views, 0)

    def test_invalid_url(self):
        video_url = "https://www.youtube.com/watch?v=invalidid123"
        views = fetch_youtube_views(video_url)
        self.assertIsNone(views)

if __name__ == "__main__":
    unittest.main() 