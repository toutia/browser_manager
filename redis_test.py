import redis
import json
import time
import threading
# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

# Simulated page elements (from an accessibility snapshot)
page_elements = [
    {"role": "button", "name": "Submit", "focusable": True},
    {"role": "textbox", "name": "Username", "focusable": True},
]

# Store page elements in Redis (using a hash with the page URL as key)
def store_page_elements(page_url, elements):
    r.hset(f'page:{page_url}', mapping={i: json.dumps(el) for i, el in enumerate(elements)})

# Simulate page analysis
def analyze_page(page_url):
    # Here you can use Playwright or other tools to analyze the page
    store_page_elements(page_url, page_elements)
    description = "This is the login page. You can enter your username and click the submit button v2."

    # Publish description to the Redis channel for TTS
    r.publish('page_descriptions', description)
    print("published")


def subscribe_to_channel():
    pubsub = r.pubsub()
    pubsub.subscribe('page_descriptions')  # Subscribe to the channel 'my_channel'

    print("Subscribed to channel. Waiting for messages...")
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received message: {message['data'].decode('utf-8')}")



# Simulate running the analysis process for different pages
def main():

    # Run subscription in a separate thread
    thread = threading.Thread(target=subscribe_to_channel)
    thread.start()


    
    page_url = "example.com/login"
    print(f"Analyzing page: {page_url}")
    analyze_page(page_url)
    time.sleep(1)

    

if __name__ == "__main__":
    main()
