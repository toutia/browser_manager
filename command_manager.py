import browser_service_pb2
from trace_lens import TraceLens



class CommandManager:
    def __init__(self, page):
        self.page = page 
        self.message='Command Excecuted.'
    

    def format_selector(role, name):
        """Format a Playwright selector using role and name."""
        return f'role={role}[name="{name}"]'

   



    def execute(self, action , url, selector):
        
        
        if action == "goto" and url:
            self.page.goto(url)
      
       
        elif action == "click" and selector:
            self.page.locator(selector).click()
        elif action == "press_sequentially" and selector and url:
            self.page.locator(selector).press_sequentially(url)
        elif action == "inner_text" and selector:
            self.page.wait_for_selector(selector)
            self.message=  self.page.locator(selector).inner_text()
        
        else:
            return browser_service_pb2.Response(status="error", message="Unknown command.")

        # if the action is valid 
        # we can execute out TraceLens 
        print(self.page.url)
        trace_lens= TraceLens(current_page=self.page)
        transition_description=trace_lens.analyze_page_transition()
        print(transition_description)
        return browser_service_pb2.Response(status="success", message=self.message)


      

    def get_accessibility_info(self):
      
        # Extract accessible interactive elements along with bounding boxes
        accessible_elements = self.extract_accessible_elements(self.page)

        # Output the accessible elements
        for element in accessible_elements:
            print(f"Role: {element['role']}, Name: {element['name']}, Bounding Box: {element['bounding_box']}")

        return str(accessible_elements)