from constructs import Construct
from aws_cdk import (
    Stack,
    aws_s3_deployment as s3deploy,
    BundlingOptions,
    aws_ecr as ecr,
    aws_codepipeline as codepipeline,
    aws_s3 as s3,
    aws_codepipeline_actions as codepipeline_actions,
    RemovalPolicy,
    aws_iam as iam,
    aws_codebuild as codebuild,
    CfnOutput,
)


class ECRBuildAndPushFromS3(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        source_bucket,
        source_key,
        buildspec_location,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        stk = Stack.of(self)

        self.repo = ecr.Repository(self, "R")
        source_output = codepipeline.Artifact()

        self.build_output = codepipeline.Artifact()

        self.build_role = iam.Role(
            self,
            "CodeBuildRole",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonEC2ContainerRegistryPowerUser"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            ],
        )

        codebuild_environment = codebuild.BuildEnvironment(
            compute_type=codebuild.ComputeType.LARGE,
            privileged=True,
            build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_5,
        )
        
        codebuild_buildspec = codebuild.BuildSpec.from_asset(buildspec_location)

        source_stage = codepipeline.StageProps(
            stage_name="Source",
            actions=[
                codepipeline_actions.S3SourceAction(
                    action_name="S3Source",
                    bucket=source_bucket,
                    bucket_key=source_key,
                    output=source_output,
                ),
            ],
        )

        build_stage = codepipeline.StageProps(
            stage_name="BuildAndPush",
            actions=[
                codepipeline_actions.CodeBuildAction(
                    action_name="BuildAndPush",
                    project=codebuild.PipelineProject(
                        self,
                        "CB-Project",
                        role=self.build_role,
                        environment=codebuild_environment,
                        build_spec=codebuild_buildspec,
                    ),
                    outputs=[self.build_output],
                    input=source_output,
                    environment_variables={
                        "REPOSITORY_URI": codebuild.BuildEnvironmentVariable(
                            value=self.repo.repository_uri
                        ),
                        "IMAGE_REPO_NAME": codebuild.BuildEnvironmentVariable(
                            value=self.repo.repository_name
                        ),
                        "IMAGE_TAG": codebuild.BuildEnvironmentVariable(value="latest"),
                        "AWS_DEFAULT_REGION": codebuild.BuildEnvironmentVariable(
                            value=stk.region
                        ),
                        "AWS_ACCOUNT_ID": codebuild.BuildEnvironmentVariable(
                            value=stk.account
                        ),
                    },
                ),
            ],
        )

        pipe = codepipeline.Pipeline(
            self,
            "CP",
            artifact_bucket=source_bucket,
            stages=[source_stage, build_stage],
        )
        # pipe.role.add_to_principal_policy(iam.PolicyStatement(actions=["s3:*"], resources=["*"]))
        self.pipeline = pipe

    def add_deploy(self, fargate_service):

        self.pipeline.add_stage(
            stage_name="DeployToECS",
            actions=[
                codepipeline_actions.EcsDeployAction(
                    action_name="Deploy",
                    service=fargate_service,
                    input=self.build_output,
                )
            ],
        )
