from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from constant import OUTPUT_FOLDER, CUSTOM_IMAGE_PATH

with Diagram(f"NAME", show=False, filename="output/global_user_diagram"):
    custom_user = Custom("USERS", CUSTOM_IMAGE_PATH["user"])
    
    
    with Cluster("User"):
        custom_user >> custom_user
        
        