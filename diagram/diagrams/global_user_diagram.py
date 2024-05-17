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

with Diagram("Global",direction='TB', show=False, filename=f"{OUTPUT_FOLDER}/global_user_diagram", graph_attr=graph_attr) as diagram:
    with Cluster("continuous_integration"):
        github = Github("GitHub")
        github_actions = GithubActions("GitHub Actions")

    with Cluster("web_service"):
        with Cluster("api"):
            with Cluster("docker1"):
                with Cluster("Client"):
                    service_client = Server("Client")
                    db_client = PostgreSQL("Client Database")
                    service_client >> db_client
            with Cluster("docker2"):
                with Cluster("Product"):
                    service_product = Server("Product")
                    db_product = PostgreSQL("Product Database")
                    service_product >> db_product
            with Cluster("docker3"):
                with Cluster("Command"):
                    service_command = Server("Command")
                    db_command = PostgreSQL("Command Database")
                    service_command >> db_command

        with Cluster("sonarqube", graph_attr={"pencolor": "#60193C", "bgcolor": "#fefefe"}):
            sonarqube = Custom("SonarQube", CUSTOM_IMAGE_PATH["sonarqube"])

        with Cluster("message_broker"):
            kafka = Kafka("Kafka")

    with Cluster("monitoring"):
        sentry = Sentry("Sentry")

    with Cluster(label="client"):
        client = User("Client")
        nginx = Nginx("Nginx")

    client >> nginx << Edge(label="rest", color="purple", ltail="cluster_user", lhead="cluster_web_service") >> [service_command, service_product, service_client]
    service_command << Edge(color="purple", ltail="cluster_api", lhead="cluster_sonarqube") >> sonarqube
    service_command << Edge(ltail="cluster_api", lhead="cluster_message_broker") >> kafka
    service_command << Edge(ltail="cluster_web_service", lhead="cluster_monitoring") >> sentry
    service_command << Edge(label="deployment", color="blue", ltail="cluster_web_service", lhead="cluster_continuous_integration") >> github >> github_actions

diagram
