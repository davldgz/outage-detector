import requests
import time

def check_url(url):
    pass

current_time1 = time.perf_counter()

response = requests.get('https://reddit.com', timeout=5)
current_time2 = time.perf_counter()
request_time = (current_time2 - current_time1) * 1000

print(response.status_code)
print(f"{round(request_time)} ms")