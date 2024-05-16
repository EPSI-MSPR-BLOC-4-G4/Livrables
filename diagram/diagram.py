from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from constant import OUTPUT_FOLDER, CUSTOM_IMAGE_PATH
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx

from diagrams.azure.network import Subnets
# ----------------------------------------
# Global User Diagram : User <->  3 APIs <-> 1 Broker Message Queue
# ----------------------------------------

graph_attr = {
    "layout":"dot",
    "compound":"true",
    }

class Subnet(Cluster):
    # fmt: off
    _default_graph_attrs = {
        "shape": "box",
        "style": "",
        "labeljust": "l",
        "pencolor": "#00D110",
        "fontname": "sans-serif",
        "fontsize": "12",
    }
    # fmt: on
    _icon = Subnets


with Diagram("Global", show=False, filename="output/global_user_diagram", graph_attr=graph_attr) as diagram:
    with Cluster(label="client"):
        
        nginx = Nginx("Nginx")
        client = Custom("Client", CUSTOM_IMAGE_PATH["user"])

    with Cluster("continuous_integration"):
        github = Custom("GitHub", CUSTOM_IMAGE_PATH["github"])
        github_actions = Custom("GitHub Actions", CUSTOM_IMAGE_PATH["github_actions"])
        
    
    with Subnet("web_service"):    
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
        
            client >> nginx << Edge(label="rest", color="purple",ltail="cluster_user", lhead="cluster_web_service") >> service_client
            service_command << Edge(color="purple",ltail="cluster_api", lhead="cluster_sonarqube") >> sonarqube        
        
    with Cluster("monitoring"):    
        sentry = Custom("Sentry", CUSTOM_IMAGE_PATH["sentry"])
        

    service_command << Edge(ltail="cluster_api", lhead="cluster_message_broker") >> kafka << Edge(label="logs", color="brown",ltail="cluster_web_service", lhead="cluster_monitoring") >> sentry
    kafka << Edge(label="deployment", color="blue",ltail="cluster_web_service", lhead="cluster_continuous_integration") >>  github >> github_actions
    
    
diagram


# from diagrams import Diagram, Edge, Cluster
# from diagrams.aws.compute import EC2, ApplicationAutoScaling
# from diagrams.aws.network import ELB, VPC, PrivateSubnet, PublicSubnet
# from diagrams.onprem.compute import Server
# from diagrams.onprem.container import Docker


# class Region(Cluster):
#   _default_graph_attrs = {
#       "shape": "box",
#       "style": "dotted",
#       "labeljust": "l",
#       "pencolor": "#AEB6BE",
#       "fontname": "Sans-Serif",
#       "fontsize": "12",
#   }


# class AvailabilityZone(Cluster):
#     # fmt: off
#     _default_graph_attrs = {
#         "shape": "box",
#         "style": "dashed",
#         "labeljust": "l",
#         "pencolor": "#27a0ff",
#         "fontname": "sans-serif",
#         "fontsize": "12",
#     }
#     # fmt: on


# class VirtualPrivateCloud(Cluster):
#     # fmt: off
#     _default_graph_attrs = {
#         "shape": "box",
#         "style": "",
#         "labeljust": "l",
#         "pencolor": "#00D110",
#         "fontname": "sans-serif",
#         "fontsize": "12",
#     }
#     # fmt: on
#     _icon = VPC


# class PrivateSubnet(Cluster):
#     # fmt: off
#     _default_graph_attrs = {
#         "shape": "box",
#         "style": "",
#         "labeljust": "l",
#         "pencolor": "#329CFF",
#         "fontname": "sans-serif",
#         "fontsize": "12",
#     }
#     # fmt: on
#     _icon = PrivateSubnet


# class PublicSubnet(Cluster):
#     # fmt: off
#     _default_graph_attrs = {
#         "shape": "box",
#         "style": "",
#         "labeljust": "l",
#         "pencolor": "#00D110",
#         "fontname": "sans-serif",
#         "fontsize": "12",
#     }
#     # fmt: on
#     _icon = PublicSubnet


# class SecurityGroup(Cluster):
#     # fmt: off
#     _default_graph_attrs = {
#         "shape": "box",
#         "style": "dashed",
#         "labeljust": "l",
#         "pencolor": "#FF361E",
#         "fontname": "Sans-Serif",
#         "fontsize": "12",
#     }
#     # fmt: on


# class AutoScalling(Cluster):
#     # fmt: off
#     _default_graph_attrs = {
#         "shape": "box",
#         "style": "dashed",
#         "labeljust": "l",
#         "pencolor": "#FF7D1E",
#         "fontname": "Sans-Serif",
#         "fontsize": "12",
#     }
#     # fmt: on
#     _icon = ApplicationAutoScaling


# class EC2Contents(Cluster):
#     # fmt: off
#     _default_graph_attrs = {
#         "shape": "box",
#         "style": "",
#         "labeljust": "l",
#         "pencolor": "#FFB432",
#         "fontname": "Sans-Serif",
#         "fontsize": "12",
#     }
#     # fmt: on
#     _icon = EC2


# class ServerContents(Cluster):
#     # fmt: off
#     _default_graph_attrs = {
#         "shape": "box",
#         "style": "rounded,dotted",
#         "labeljust": "l",
#         "pencolor": "#A0A0A0",
#         "fontname": "Sans-Serif",
#         "fontsize": "12",
#     }
#     # fmt: on
#     _icon = Server


# with Diagram(name="", direction="TB", filename="aws"):
#     with Cluster("AWS", graph_attr={"fontsize": "15"}): # overwrite attributes for the default cluster
#         with Region("eu-west-1", graph_attr={"pencolor": "#60193C", "bgcolor": "#E587B5"}): # one cluster defined but with overwritten attributes
#             with AvailabilityZone("eu-west-1a"):
#                 with VirtualPrivateCloud(""):
#                     with PrivateSubnet("Private"):
#                         with SecurityGroup("web sg"):
#                             with AutoScalling(""):
#                                 with EC2Contents("A"):
#                                     d1 = Docker("Container")
#                                 with ServerContents("A1"):
#                                     d2 = Docker("Container")

#                     with PublicSubnet("Public"):
#                         with SecurityGroup("elb sg"):
#                             lb = ELB()

#     lb >> Edge(forward=True, reverse=True) >> d1
#     lb >> Edge(forward=True, reverse=True) >> d2