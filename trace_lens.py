from urllib.parse import urlparse
import redis
import json
import time
import threading
from PIL import Image, ImageDraw
"""
this  service's core functionality is  tracing and analyzing page elements after command execution.
much like a lens bringing interactive elements, results, and errors into focus.

"""



class TraceLens:
    def __init__(self,current_page=None, new_page=False):
        """
        Initialize the TraceLens service.
        Set up any necessary state variables such as logs for detected errors,
        navigations (e.g., new pages or redirects), and interactive elements.
        """
        self.new_page=new_page
        self.page = current_page   # Store the current page state
        self.interactive_elements = []
        self.errors = []
        self.navigation_description = ""
        self.screenshot=""
        # Initialize Redis connection
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

        # Store page elements in Redis (using a hash with the page URL as key)
    def store_page_elements(self, elements):
        # parsed_url = urlparse(self.page.url)
        # domain = parsed_url.netloc
        redis_key = f'{self.page.url}'
        mapping = {f'element:{i}': json.dumps(el) for i, el in enumerate(elements)}
        self.redis_client.hset(redis_key, mapping=mapping)

    def check_elements_exist(self):
        redis_key = f'{self.page.url}'
        exists = self.redis_client.exists(redis_key)
        return exists > 0  # Returns True if exists, otherwise False

    def update_page_elements(self, elements):
        if self.check_elements_exist():
            self.store_page_elements(elements)
            return True
        else:
            print("Page elements do not exist to update.")
            return False



    def analyze_page_transition(self):
        """
        Analyze whether a new page or state has been loaded (transition).
        
        Returns:
            str: Description of the page transition (e.g., navigation success).
        """
        # TODO 
        #relying on the page url here wich not a reliable option 
        
      

        # if not self.new_page:
        #     self.navigation_description = "No page transition detected."
        # else:
        self.navigation_description = self._describe_new_page()
       
        
        return self.navigation_description


    
    def _draw_bounding_box(self, image_path, bounding_box):
        """Draw a bounding box on the image."""
        # Open the image
        image = Image.open(image_path)
        
        # Initialize ImageDraw
        draw = ImageDraw.Draw(image)
        
        # Get bounding box coordinates
        x = bounding_box['x']
        y = bounding_box['y']
        width = bounding_box['width']
        height = bounding_box['height']
        
        # Define the box corners (top-left and bottom-right)
        top_left = (x, y)
        bottom_right = (x + width, y + height)
        
        # Draw the rectangle (bounding box)
        draw.rectangle([top_left, bottom_right], outline="red", width=3)
        
        # Save the image with bounding box
        image.save("screenshots/screenshot.png")


    def trace_action(self, action_description, current_page_content):
        """
        Trace the result of a user action (like form submission) and capture the results.

        Args:
            action_description (str): Description of the action (e.g., "Submitted form").
            current_page_content (str or HTML object): Content of the page after the action.

        Returns:
            str: Detailed outcome description (e.g., "Form submitted, you are now on dashboard").
        """
        if self._detect_errors():
            self.errors.append({
                'action': action_description,
                'error': "Error detected after performing the action",
                'message': "This need to be extract dynamically"
            })
            return "Error occurred during action."
        
        # Analyze the new page if no errors were detected
        self.current_page = current_page_content
        outcome_description = self._describe_action_outcome(action_description, current_page_content)
        return outcome_description



    def _describe_new_page(self):
        """
        Private helper method to describe the new page after an transition.

        Args:
            page_content (str or HTML object): The current page content.
        
        Returns:
            str: A summary of the new page (e.g., "Dashboard with transaction options").
        """
        # Simplified logic: This could inspect HTML elements to describe the new page
        interactive_elements = self._find_interactive_elements()
        description = f"New page loaded with the following interactive elements: {', '.join(json.dumps(e)   for e in interactive_elements)}."
   
        return description

    def _detect_errors(self):
        """
        Private helper method to detect errors after an action (like form submission).

        Args:
            page_content (str or HTML object): The page content to inspect for errors.

        Returns:
            bool: True if errors are found, False otherwise.
        """
        # Simplified logic: Detecting error messages or alert boxes
        # Example: Check for typical error messages (like 'error', 'invalid', etc.)

        # get the full text of he page 
        body_inner_text= self.current_page.locator('body').inner_text()
        error_keywords = ['error', 'invalid', 'failed', 'not found']
        for keyword in error_keywords:
            if keyword in body_inner_text.lower():
                return True
        return False

    def _describe_action_outcome(self, action_description, page_content):
        """
        Private helper method to describe the outcome after performing an action.

        Args:
            action_description (str): Description of the action (e.g., "Submitted form").
            page_content (str or HTML object): The page content after the action.
        
        Returns:
            str: A human-readable description of the action outcome (e.g., "Form submitted successfully, now on dashboard").
        """
        # This can include more logic to analyze forms, transitions, etc.
        if "dashboard" in page_content.lower():
            return f"{action_description} successful. You are now on the dashboard."

        # Fallback outcome description
        return f"{action_description} executed. Page loaded successfully."

    def _find_interactive_elements(self):
        """
        Private helper method to find and identify interactive elements on the page.
        
        

        Returns:
            list: A list of identified interactive elements (e.g., buttons, forms, links).
        """
        
        accessibility_snapshot = self.page.accessibility.snapshot(interesting_only=True)

        # Function to recursively search for interactive elements in the accessibility tree
        def find_interactive_elements(node, elements=[]):
            # If the node has a role, name and is focusable, it's likely interactive
            if node.get('role') and  node.get('name'):
                elements.append(node)
            
            # Recursively check children
            for child in node.get('children', []):
                find_interactive_elements(child, elements)
            
            return elements

        # Get all interactive elements in the accessibility tree
        interactive_elements = find_interactive_elements(accessibility_snapshot)

        
        
        # Find locators and bounding boxes for these elements
        
        for node in interactive_elements:
            # role = node['role']
            # name = node.get('name', None)
            # # Using locators to query element in DOM
            # try:
            #     # Optionally wait for it to be visible
            #     # locator.wait_for(state='visible', timeout=1000)

            #     # # Then you can get the bounding box or perform other actions
            #     # bounding_box = self.page.get_by_role(role, name=name).bounding_box()
            #     if bounding_box:
            self.interactive_elements.append({
                "role": node.get("role"),
                "name": node.get("name"),
                "value": node.get("value"),
                "checked": node.get("checked"),
                "disabled": node.get("disabled"),
                "expanded": node.get("expanded"),
                "focusable": node.get("focusable"),
                "pressed": node.get("pressed"),
                "selected": node.get("selected"),
                "readonly": node.get("readonly"),
                "required": node.get("required"),
                "autocomplete": node.get("autocomplete"),
                "placeholder": node.get("placeholder"),
                "role_description": node.get("role_description"),
                "hidden": node.get("hidden"),
                "orientation": node.get("orientation"),
                "children": [],  # Children will be populated recursively
                # 'bounding_box': bounding_box
            })

            self.store_page_elements(self.interactive_elements)

                # self.draw_bounding_box("screenshots/screenshot.png", bounding_box)
                # print('FOUND')
                # print( self.page.get_by_role(role, name=name))
            # except Exception as e :
            #     print(e)
                # print(role,name)
        return self.interactive_elements
    
        
        
    

  

    def get_summary(self):
        """
        Provides a summary of the last traced action, errors, and current interactive elements.
        
        Returns:
            dict: A summary containing the navigation description, errors, and current page elements.
        """
        return {
            'navigation_description': self.navigation_description,
            'errors': self.errors,
            'interactive_elements': self.interactive_elements
        }
