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
        command = browser_service_pb2.Command(action="goto", url="https://chatgpt.com")
        response = stub.ExecuteCommand(command)
        print(f"Execute Command: {response.message}")
        time.sleep(3)
        


        # sendf message intent of chatgpt site containes : press seqentially and click 
        command = browser_service_pb2.Command(action="press_sequentially", url="what is the capital of france" , selector='textarea[placeholder="Message ChatGPT"]')
        response = stub.ExecuteCommand(command)
        print(f"Execute Command: {response.message}")

        time.sleep(1)
         

        command = browser_service_pb2.Command(action="click",  selector='button[data-testid="send-button"]')
        response = stub.ExecuteCommand(command)
        print(f"Execute Command: {response.message}")


        # get response 
        
        command = browser_service_pb2.Command(action="inner_text",  selector='div[data-message-author-role="assistant"]')
        response = stub.ExecuteCommand(command)
        print(f"Execute Command: {response.message}")



        # # Shutdown the browser
        # response = stub.ShutdownBrowser(browser_service_pb2.Empty())
        # print(f"Shutdown Browser: {response.message}")

if __name__ == '__main__':
    run()
