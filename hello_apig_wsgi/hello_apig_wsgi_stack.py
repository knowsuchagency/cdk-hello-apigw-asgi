from aws_cdk import (
    core,
    aws_apigateway as apigw,
    aws_lambda_python as lmb_py,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_lambda as lmb,
)


class HelloApigWsgiStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        vpc = ec2.Vpc(self, "vpc")

        file_system = efs.FileSystem(self, "filesystem", vpc=vpc)

        access_point = file_system.add_access_point(
            "access-point", posix_user=efs.PosixUser(uid="0", gid="0")
        )

        mount_path = "/mnt/openapi"

        function = lmb_py.PythonFunction(
            self,
            "function",
            entry="./lambdas",
            vpc=vpc,
            filesystem=lmb.FileSystem.from_efs_access_point(access_point, mount_path),
            environment={"mount_path": mount_path},
        )

        api = apigw.LambdaRestApi(
            self,
            "api",
            handler=function,
        )
