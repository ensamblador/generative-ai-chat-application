from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2_actions as elb_actions,
    aws_elasticloadbalancingv2 as elb
)
from aws_cdk.aws_ec2 import SecurityGroup, Port, Peer



# This tutorial uses Route53/ACM to https 
# https://github.com/MauriceBrg/cognito-alb-fargate-demo/blob/master/infrastructure/demo_stack.py

class ECSDeployWithLoadBalancer(Construct):
    def __init__(self, scope: Construct, id: str, repo,  cluster, env={"foo": "bar"}, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.ecs_role = iam.Role( self,"Role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryPowerUser")],
        )

        self.task_image_opts = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_ecr_repository(repo, "latest"),
            container_port=8501,
            environment=env,
            container_name="streamlit-chat",
            task_role=self.ecs_role
        )
        self.ecs_role.add_to_policy( iam.PolicyStatement(actions=["bedrock:*"], resources=["*"]))

        ecs_deployment = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "app",
            cluster=cluster,
            memory_limit_mib=1024,
            cpu=512,
            task_image_options=self.task_image_opts,
        )
        self.service = ecs_deployment.service





class ECSDeployWithPublicIP(Construct):
    def __init__(self, scope: Construct, id: str, repo,  cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.ecs_role = iam.Role( self,"ECSRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryPowerUser")],
        )

        self.ecs_role.add_to_policy( iam.PolicyStatement(actions=["bedrock:*"], resources=["*"]))

        task_definition = ecs.FargateTaskDefinition(
            self,
            "FTD",
            cpu=1024,
            memory_limit_mib=2048,
            task_role=self.ecs_role
        )

        task_definition.add_container(
            "streamlit",image=ecs.ContainerImage.from_ecr_repository(repo),
            port_mappings=[ ecs.PortMapping(container_port=8501, app_protocol=ecs.AppProtocol.http2, name= "streamlit-8501")])

        security_group = SecurityGroup(self, "SG", vpc=cluster.vpc, allow_all_outbound=True,  security_group_name="ToStreamlit",)
        
        security_group.add_ingress_rule(peer=Peer.any_ipv4(), connection=Port.tcp(8501), description="Allow Streamlit")

        ecs_service =  ecs.FargateService(
            self, "FS", cluster=cluster,
            assign_public_ip=True,
            task_definition=task_definition,
            security_groups=[security_group]
        )    

        self.service = ecs_service
