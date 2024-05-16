from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from constant import OUTPUT_FOLDER, CUSTOM_IMAGE_PATH
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx

# ----------------------------------------
# Global User Diagram : User <->  3 APIs <-> 1 Broker Message Queue
# ----------------------------------------

graph_attr = {
    "layout":"dot",
    "compound":"true",
    "center":"true",
    }

with Diagram("Global",direction='TB', show=False, filename=f"{OUTPUT_FOLDER}/global_user_diagram", graph_attr=graph_attr) as diagram:
    with Cluster("continuous_integration"):
        github = Custom("GitHub", CUSTOM_IMAGE_PATH["github"])
        github_actions = Custom("GitHub Actions", CUSTOM_IMAGE_PATH["github_actions"])
        
    
    with Cluster("web_service"):    
        with Cluster("api"):
            with Cluster("docker1"):
                with Cluster("Client", graph_attr={"pencolor": "#000", "bgcolor": "#fff"}):
                    service_client  = Server("Client")
                    db_client = PostgreSQL("Client Database")
                    service_client >> db_client
            with Cluster("docker2"):                    
                with Cluster("Product", graph_attr={"pencolor": "#000", "bgcolor": "#fff"}):
                    service_product = Server("Product")
                    db_product = PostgreSQL("Product Database")
                    service_product >> db_product
            with Cluster("docker3"):                    
                with Cluster("Command", graph_attr={"pencolor": "#000", "bgcolor": "#fff"}):
                    service_command = Server("Command")
                    db_command = PostgreSQL("Command Database")
                    service_command >> db_command
            
        with Cluster("sonarqube", graph_attr={"pencolor": "#60193C", "bgcolor": "#fefefe"}):
            sonarqube = Custom("SonarQube", CUSTOM_IMAGE_PATH["sonarqube"])
                    

        with Cluster("message_broker"):
            kafka = Custom("Kafka", CUSTOM_IMAGE_PATH["kafka"])
        

    with Cluster("monitoring"):    
        sentry = Custom("Sentry", CUSTOM_IMAGE_PATH["sentry"])
        
    with Cluster(label="client"):
        client = Custom("Client", CUSTOM_IMAGE_PATH["user"])
        nginx = Nginx("Nginx")



    client >> nginx << Edge(label="rest", color="purple",ltail="cluster_user", lhead="cluster_web_service") >> [service_command, service_product, service_client]
    service_command << Edge(color="purple",ltail="cluster_api", lhead="cluster_sonarqube") >> sonarqube            
    service_command << Edge(ltail="cluster_api", lhead="cluster_message_broker") >> kafka
    service_command << Edge(ltail="cluster_web_service", lhead="cluster_monitoring") >> sentry
    service_command << Edge(label="deployment", color="blue",ltail="cluster_web_service", lhead="cluster_continuous_integration") >>  github >> github_actions
    
    
diagram