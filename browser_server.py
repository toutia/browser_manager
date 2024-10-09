from concurrent import futures
import grpc
from playwright.sync_api import sync_playwright
import browser_service_pb2
import browser_service_pb2_grpc
import threading
import time

from command_manager import CommandManager
"""

Using gRPC to manage a Playwright browser instance offers several advantages, including performance, type safety, and better handling of concurrent requests.
By encapsulating the browser management logic in a gRPC server, you can efficiently execute commands and maintain a persistent browser session across multiple clients.
This architecture can be particularly useful for applications where low latency and real-time interaction with a browser are essential.
~/.cache/ms-playwright/chromium-1134/chrome-linux$ ./chrome  --remote-debugging-port=9222 --user-data-dir=./user_data:
"""
class BrowserManager(browser_service_pb2_grpc.BrowserServiceServicer):
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.lock = threading.Lock()
     

    def StartBrowser(self, request, context):
        with self.lock:
            if self.playwright is None:
                self.playwright = sync_playwright().start()
                self.browser = self.playwright.chromium.connect_over_cdp('http://127.0.0.1:9222/')
       

                # Retrieve the first context of the browser.
                default_context = self.browser.contexts[0]

                # Retrieve the first page in the context.
                self.page = default_context.pages[0]
                return browser_service_pb2.Response(status="success", message="Browser started.")
            return browser_service_pb2.Response(status="error", message="Browser is already running.")

    def ExecuteCommand(self, request, context):
        with self.lock:
            if self.page is None:
                return browser_service_pb2.Response(status="error", message="Browser is not started.")
            try:
                command_executer= CommandManager(self.page)

                return command_executer.execute(request.action, request.url, request.selector)
            except Exception as e:
                return browser_service_pb2.Response(status="error", message=str(e))

    def ShutdownBrowser(self, request, context):
        with self.lock:
            if self.page:
                self.page.close()
                self.page = None
            if self.browser:
                self.browser.close()
                self.browser = None
            if self.playwright:
                self.playwright.stop()
                self.playwright = None
            return browser_service_pb2.Response(status="success", message="Browser shutdown.")

    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    browser_service_pb2_grpc.add_BrowserServiceServicer_to_server(BrowserManager(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("gRPC server running on port 50052...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
