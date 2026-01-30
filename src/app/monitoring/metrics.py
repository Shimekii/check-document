from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'project_http_request_total',
    'Total http request',
    ['method', 'path', 'status']
)

REQUEST_LATENCY = Histogram(
    'project_http_request_duration_second',
    'HTTP request latency',
    ['method', 'path', 'status'],
    buckets=(0.1, 0.25, 0.5, 1, 2.5, 5, 10)
)