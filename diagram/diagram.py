from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from constant import OUTPUT_FOLDER, CUSTOM_IMAGE_PATH
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx

# ----------------------------------------
# Global User Diagram : User <->  3 APIs <-> 1 Broker Message Queue
# ----------------------------------------
with Diagram("Global", show=False, filename="output/global_user_diagram"):
    nginx = Nginx("Nginx")
    user = Custom("USERS", CUSTOM_IMAGE_PATH["user"])

    with Cluster("Continuous Integration"):
        github = Custom("GitHub", CUSTOM_IMAGE_PATH["github"])
        github_actions = Custom("GitHub Actions", CUSTOM_IMAGE_PATH["github_actions"])
        github >> github_actions
        
    with Cluster("Service Cluster"):    
        with Cluster("API Services"):
            db1 = PostgreSQL("Database1")
            db2 = PostgreSQL("Database2")
            db3 = PostgreSQL("Database3")
            
            apisvc = [
                Server("Client"),
                Server("Command"),
                Server("Product")
            ]

            with Cluster("Database Cluster"):            
                apisvc[0] >> db1
                apisvc[1] >> db2
                apisvc[2] >> db3
                            
            user>> nginx >> apisvc


        with Cluster("Message Broker"):
            kafka = Custom("Kafka", CUSTOM_IMAGE_PATH["kafka"])
        
        with Cluster("Monitoring"):    
            sentry = Custom("Sentry", CUSTOM_IMAGE_PATH["sentry"])
            
            sentry << Edge(label="deployment", color="blue") >> github

    
    
    apisvc[1] >> kafka << Edge(label="logs", color="brown") >> sentry
    
    