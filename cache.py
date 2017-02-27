class Cache:
    size = 0
    current_size = 0
    video_sizes = []
    video_ids = []

    def __init__(self, cache_size, video_sizes):
        self.size = cache_size
        self.video_sizes = video_sizes
        self.video_ids = []

    def add_video(self, video_id):
        if (self.current_size + self.video_sizes[video_id]) > self.size or video_id in self.video_ids:
            return False
        self.video_ids.append(video_id)
        self.current_size += self.video_sizes[video_id]
        return True
