from playwright.sync_api import Page

class ChatGPTPage:
    def __init__(self, page: Page):
        self.page = page
        self.input_selector = 'textarea[placeholder="Message ChatGPT"]'  # Adjust this selector based on the actual element
        self.send_button_selector = 'button[data-testid="send-button"]'  # Adjust this selector based on the actual element
        self.response_selector = 'div[data-message-author-role="assistant"]'  # Adjust this selector based on the actual element
    
    def navigate(self, url: str):
        self.page.goto(url)

    def send_message(self, message: str):
        self.page.press_sequentially(self.input_selector,message) 
        self.page.click(self.send_button_selector)

    def get_response(self):
        # Wait for the response to appear and return the text
        self.page.wait_for_selector(self.response_selector)
        return self.page.inner_text(self.response_selector)


from playwright.sync_api import sync_playwright
import os 
# Path to your user data directory
user_data_dir = os.path.expanduser('~/snap/chromium/common/chromium')  # Update this as needed

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(user_data_dir, headless=False)
    page = browser.new_page()
    chatgpt = ChatGPTPage(page)

    chatgpt.navigate("https://chatgpt.com")
    chatgpt.send_message("What is the capital of the united states?")
    import time 
    time.sleep(3)
    response = chatgpt.get_response()
    print(response)

    browser.close()
