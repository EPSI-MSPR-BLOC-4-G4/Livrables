import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.monitoring import Sentry
from diagrams.onprem.queue import Kafka
from diagrams.ibm.user import User
from diagrams.custom import Custom

from constant import OUTPUT_FOLDER, CUSTOM_IMAGE_PATH

# ----------------------------------------
# Global User Diagram : User <->  3 APIs <-> 1 Broker Message Queue
# ----------------------------------------

graph_attr = {
    "layout": "dot",
    "compound": "true",
    "center": "true",
}

# ----------------------------------------
# Define the diagram
# ----------------------------------------
with Diagram("Global",direction='TB', show=False, filename=f"{OUTPUT_FOLDER}/global_user_diagram", graph_attr=graph_attr) as diagram:
    
    # ----------------------------------------
    # 1) Cluster : continuous_integration
    # ----------------------------------------
    with Cluster("continuous_integration", graph_attr={"fontsize:":"20"}):
        github = Github("GitHub")
        github_actions = GithubActions("GitHub Actions")

    # ----------------------------------------
    # 2) Cluster : web_service
    # ----------------------------------------
    with Cluster("web_service"):
        
        # ----------------------------------------
        # 2-1) Cluster : api
        # ----------------------------------------
        with Cluster("api"):
            
            # ----------------------------------------
            # 2-1-1) Cluster : docker_client
            # ----------------------------------------
            with Cluster("docker_client"):
                
                # ----------------------------------------
                # 2-1-1-1) Cluster : Client
                # ----------------------------------------
                with Cluster("client"):
                    service_client = Server("Client")
                    db_client = PostgreSQL("Client Database")
                   
                    
            # ----------------------------------------
            # 2-1-2) Cluster : docker_product
            # ----------------------------------------
            with Cluster("docker_product"):
                
                # ----------------------------------------
                # 2-1-2-1) Cluster : Product
                # ----------------------------------------
                with Cluster("product"):
                    service_product = Server("Product")
                    db_product = PostgreSQL("Product Database")
                    
            # ----------------------------------------
            # 2-1-3) Cluster : docker_command
            # ----------------------------------------
            with Cluster("docker_command"):
                
                # ----------------------------------------
                # 2-1-3-1) Cluster : Command
                # ----------------------------------------
                with Cluster("command"):
                    service_command = Server("Command")
                    db_command = PostgreSQL("Command Database")
                    

        # ----------------------------------------
        # 3) Cluster : sonarqube
        # ----------------------------------------
        with Cluster("code_quality", graph_attr={"pencolor": "#60193C", "bgcolor": "#fefefe"}):
            sonarqube = Custom("SonarQube", CUSTOM_IMAGE_PATH["sonarqube"])

        # ----------------------------------------
        # 4) Cluster : message_broker
        # ----------------------------------------
        with Cluster("message_broker"):
            kafka = Kafka("Kafka")

    # ----------------------------------------
    # 5) Cluster : monitoring
    # ----------------------------------------
    with Cluster("monitoring"):
        sentry = Sentry("Sentry")

    # ----------------------------------------
    # 6) Cluster : user
    # ----------------------------------------
    with Cluster(label="client"):
        client = Custom("Client", CUSTOM_IMAGE_PATH["client"])
        nginx = Nginx("Nginx")
        
    
    # ----------------------------------------
    # Define the connections
    # ----------------------------------------
    service_client >> db_client        
    service_product >> db_product
    service_command >> db_command
    client >> nginx << Edge(label="API REST", color="purple", ltail="cluster_user", lhead="cluster_web_service") >> [service_product]
    service_command << Edge(label="code quality", color="purple", ltail="cluster_api", lhead="cluster_code_quality") >> sonarqube
    service_command << Edge(label="message", ltail="cluster_api", lhead="cluster_message_broker") >> kafka
    service_command << Edge(label="monitoring", ltail="cluster_web_service", lhead="cluster_monitoring") >> sentry
    service_command << Edge(label="deployment", color="blue", ltail="cluster_web_service", lhead="cluster_continuous_integration") >> github >> github_actions

diagram

