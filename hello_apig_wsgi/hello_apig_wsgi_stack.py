from aws_cdk import (
    core,
    aws_lambda_python as lmb_py,
aws_apigateway as apigw,
    aws_apigatewayv2 as apigw_v2,
)


class HelloApigWsgiStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        wsgi_function = lmb_py.PythonFunction(
            self, "wsgi-function", entry="./lambdas/wsgi"
        )

        wsgi_integration = apigw_v2.LambdaProxyIntegration(
            handler=wsgi_function,
            payload_format_version=apigw_v2.PayloadFormatVersion.VERSION_1_0,
        )

        http_api = apigw_v2.HttpApi(self, "http-api", default_integration=wsgi_integration)

        asgi_function = lmb_py.PythonFunction(
            self,
            "asgi-function",
            entry="./lambdas/asgi",
        )

        http_api.add_routes(
            path="/asgi",
            methods=[apigw_v2.HttpMethod.GET],
            integration=apigw_v2.LambdaProxyIntegration(handler=asgi_function),
        )

        http_api.add_routes(
            path="/wsgi",
            methods=[apigw_v2.HttpMethod.GET],
            integration=wsgi_integration,
        )

        core.CfnOutput(self, "url", value=http_api.url)

        rest_api = apigw.LambdaRestApi(
            self,
            'rest-api',
            handler=wsgi_function
        )
