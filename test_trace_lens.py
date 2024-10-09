import grpc
import browser_service_pb2
import browser_service_pb2_grpc
import time
def run():
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = browser_service_pb2_grpc.BrowserServiceStub(channel)

        # Start the browser
        response = stub.StartBrowser(browser_service_pb2.Empty())
        print(f"Start Browser: {response.message}")
        time.sleep(3)
        # Execute a command
        # https://leetcode.com/accounts/login/ => cloudfare checkbox not detected
        # articles detected by accessibilty locator not found 
        #https://www.google.com/

        command = browser_service_pb2.Command(action="goto", url="https://www.google.com/")
        response = stub.ExecuteCommand(command)
        print(f"Execute Command: {response.message}")
        time.sleep(3)


        command = browser_service_pb2.Command(action="goto", url="https://drimvision.ai/")
        response = stub.ExecuteCommand(command)
        print(f"Execute Command: {response.message}")
        time.sleep(3)
         
        # # Shutdown the browser
        # response = stub.ShutdownBrowser(browser_service_pb2.Empty())
        # print(f"Shutdown Browser: {response.message}")

if __name__ == '__main__':
    run()
