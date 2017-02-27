class Endpoint:
    index = 0
    latency = 0
    caches = {}
    requests = {}

    def __init__(self, index, latency):
        self.index = index
        self.latency = latency
        self.caches = {}
        self.requests = {}

    def add_cache(self, index, latency):
        self.caches[index] = latency

    def add_request(self, video_id, number_of_request):
        if video_id in self.requests:
            self.requests[video_id] += number_of_request
        else:
            self.requests[video_id] = number_of_request

    # Video Ids
    def get_rank_requests(self):
        keys = self.requests.keys()
        keys.sort(lambda x, y: cmp(self.requests[x], self.requests[y]), reverse=True)
        return keys

    # Cache Ids
    def get_rank_caches(self):
        keys = self.caches.keys()
        keys.sort(lambda x, y: cmp(self.caches[x], self.caches[y]))
        return keys
