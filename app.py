#!/usr/bin/env python3

from aws_cdk import core

from hello_apig_wsgi.pipeline_stack import PipelineStack
from pydantic import BaseSettings


class Config(BaseSettings):
    """https://pydantic-docs.helpmanual.io/usage/settings/"""

    account: str = "385504394431"

    region: str = "us-east-2"

    gh_username: str = "knowsuchagency"

    gh_repo: str = "cdk-hello-apigw-asgi"


config = Config()

app = core.App()
PipelineStack(
    app,
    "hello-apig-wsgi-pipeline",
    config,
    env={"account": config.account, "region": config.region},
)

app.synth()
