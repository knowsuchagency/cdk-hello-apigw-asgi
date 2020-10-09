from aws_cdk import (
    core,
    aws_lambda as lmb,
    aws_lambda_python as lmb_py,
    aws_apigateway as apigw,
    aws_apigatewayv2 as apigw_v2,
    aws_appsync as appsync,
    aws_dynamodb as dynamodb,
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

        http_api = apigw_v2.HttpApi(
            self, "http-api", default_integration=wsgi_integration
        )

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

        graphql_api = appsync.GraphqlApi(
            self,
            "graphql-api",
            name="notes-example-api",
            schema=appsync.Schema.from_asset("./graphql/schema.graphql"),
        )

        core.CfnOutput(self, "graphql url", value=graphql_api.graphql_url)

        core.CfnOutput(self, "graphql api key", value=graphql_api.api_key)

        graphql_handler = lmb_py.PythonFunction(
            self,
            "graphql-handler",
            entry="./lambdas/graphql",
            runtime=lmb.Runtime.PYTHON_3_8,
        )

        data_source = graphql_api.add_lambda_data_source(
            "lambdaDatasource", graphql_handler
        )

        data_source.create_resolver(type_name="Query", field_name="getNoteById")

        data_source.create_resolver(type_name="Query", field_name="listNotes")

        data_source.create_resolver(type_name="Mutation", field_name="createNote")

        data_source.create_resolver(type_name="Mutation", field_name="deleteNote")

        data_source.create_resolver(type_name="Mutation", field_name="updateNote")

        dynamo_table = dynamodb.Table(
            self,
            "notes-table",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=dynamodb.Attribute(
                name="id", type=dynamodb.AttributeType.STRING
            ),
        )

        dynamo_table.grant_read_write_data(graphql_handler)

        graphql_handler.add_environment("NOTES_TABLE", dynamo_table.table_name)
