import http.client
import threading
import sys
import os
from config import host, port


def check_user_existence():
    conn = http.client.HTTPConnection(host, port)
    try:
        conn.request("GET", "/api/user/load_test?username=or-tab")
        response = conn.getresponse()
        response_data = response.read().decode("utf-8")
        print(f"Response from server: {response_data}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        conn.close()


def run_load_test():
    num_requests = 200
    threads = []
    for _ in range(num_requests):
        thread = threading.Thread(target=check_user_existence)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
