from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as pipeline_actions
from aws_cdk import pipelines
from aws_cdk import aws_codebuild as codebuild

from .hello_apig_wsgi_stack import HelloApigWsgiStack

from pydantic import BaseSettings


class WebServiceStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.service = HelloApigWsgiStack(self, "WebService")


class PipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, config: BaseSettings, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()

        cloud_assembly_artifact = codepipeline.Artifact()

        source_action = pipeline_actions.GitHubSourceAction(
            action_name="GitHub",
            output=source_artifact,
            oauth_token=core.SecretValue.secrets_manager("github-token"),
            owner=config.gh_username,
            repo=config.gh_repo,
            trigger=pipeline_actions.GitHubTrigger.POLL,
        )

        synth_action = pipelines.SimpleSynthAction(
            source_artifact=source_artifact,
            cloud_assembly_artifact=cloud_assembly_artifact,
            install_commands=[
                "npm install -g aws-cdk",
                "pip install -r requirements.txt",
            ],
            test_commands=["pytest lambdas -v -m 'not integration'"],
            synth_command="cdk synth application",
            environment=codebuild.BuildEnvironment(privileged=True),
        )

        pipeline = pipelines.CdkPipeline(
            self,
            "pipeline",
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name="hello-pipeline",
            source_action=source_action,
            synth_action=synth_action,
        )

        pre_prod_app = WebServiceStage(
            self,
            "preprod",
            env={
                "account": config.account,
                "region": config.region,
            },
        )

        pre_prod_stage = pipeline.add_application_stage(pre_prod_app)

        pre_prod_stage.add_actions(
            pipelines.ShellScriptAction(
                action_name="integration_tests",
                run_order=pre_prod_stage.next_sequential_run_order(),
                additional_artifacts=[source_artifact],
                commands=[
                    "pip install -r requirements.txt",
                    "pytest lambdas -v -m integration",
                ],
                use_outputs={
                    "http_api_url": pipeline.stack_output(
                        pre_prod_app.service.http_api_url
                    )
                },
            )
        )

        pre_prod_stage.add_manual_approval_action(action_name="PromoteToProd")

        prod_app = WebServiceStage(
            self,
            "Prod",
            env={
                "account": config.account,
                "region": config.region,
            },
        )

        pipeline.add_application_stage(prod_app)
