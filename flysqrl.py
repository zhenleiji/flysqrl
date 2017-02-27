import time
from endpoint import Endpoint
from cache import Cache

# 5 2 4 3 100 -  5 videos, 2 endpoints, 4 request descriptions, 3 caches 100MB each
INDEX_NUMBER_OF_VIDEOS = 0
INDEX_NUMBER_OF_ENDPOINTS = 1
INDEX_NUMBER_OF_REQUESTS = 2
INDEX_NUMBER_OF_CACHES = 3
INDEX_CACHE_SIZE = 4


def read(input):
    f = open(input, 'r')
    conf = [int(x) for x in f.readline().replace('\n', '').split(' ')]
    video_sizes = [int(x) for x in f.readline().replace('\n', '').split(' ')]

    endpoints = []
    for i in range(0, conf[INDEX_NUMBER_OF_ENDPOINTS]):
        endpoint_raw = [int(x) for x in f.readline().replace('\n', '').split(' ')]
        endpoint = Endpoint(i, endpoint_raw[0])
        for j in range(0, endpoint_raw[1]):
            cache_raw = [int(x) for x in f.readline().replace('\n', '').split(' ')]
            endpoint.add_cache(cache_raw[0], cache_raw[1])
        endpoints.append(endpoint)

    for i in range(0, int(conf[INDEX_NUMBER_OF_REQUESTS])):
        request_raw = [int(x) for x in f.readline().replace('\n', '').split(' ')]
        endpoints[request_raw[1]].add_request(request_raw[0], request_raw[2])
    f.close()
    return conf, video_sizes, endpoints


def write(output_file_path, caches):
    f = open(output_file_path, 'w')
    size = len(caches)
    f.write(str(size) + '\n')
    for i in range(0, size):
        f.write(str(i) + ' ')
        f.write(' '.join(str(video_id) for video_id in caches[i].video_ids))
        f.write('\n')
    f.close()


def get_rank_video(video_size):
    indexes = range(0, len(video_size))
    indexes.sort(lambda x, y: cmp(video_size[x], video_size[y]))
    return indexes


def get_rank_endpoint_latency(endpoints):
    indexes = range(0, len(endpoints))
    indexes.sort(lambda x, y: cmp(endpoints[x].latency, endpoints[y].latency), reverse=True)
    return indexes


def get_request_threshold(endpoints):
    requests = []
    for endpoint in endpoints:
        requests.extend(endpoint.requests.values())
    requests.sort()
    size = len(requests)

    return requests[size / 4], requests[size / 2], requests[size * 3 / 4]


def magic_algorithm(file_path):
    input = read(file_path)
    conf = input[0]
    video_sizes = input[1]
    endpoints = input[2]
    caches = []

    threshold = get_request_threshold(endpoints)

    for i in range(0, conf[INDEX_NUMBER_OF_CACHES]):
        caches.append(Cache(conf[INDEX_CACHE_SIZE], video_sizes))

    for endpoint_id in get_rank_endpoint_latency(endpoints):
        for video_id in endpoints[endpoint_id].get_rank_requests():
            if endpoints[endpoint_id].requests[video_id] > threshold[0]:
                for cache_id in endpoints[endpoint_id].get_rank_caches():
                    if endpoints[endpoint_id].caches[cache_id] < endpoints[endpoint_id].latency and \
                            caches[cache_id].add_video(video_id):
                        break

    for endpoint_id in get_rank_endpoint_latency(endpoints):
        for video_id in endpoints[endpoint_id].get_rank_requests():
            if endpoints[endpoint_id].requests[video_id] <= threshold[0]:
                for cache_id in endpoints[endpoint_id].get_rank_caches():
                    if endpoints[endpoint_id].caches[cache_id] < endpoints[endpoint_id].latency and \
                            caches[cache_id].add_video(video_id):
                        break

    return caches


## MAIN ##
file_names = ['kittens.in', 'me_at_the_zoo.in', 'trending_today.in', 'videos_worth_spreading.in']
file_paths = ['files/' + name for name in file_names]

for file_path in file_paths:
    print("Processing %s..." % file_path)
    start = time.time()
    caches = magic_algorithm(file_path)
    write(file_path + ".out", caches)
    end = time.time()
    print("Done in %.3fs\n" % (end - start))
