import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="hello_apig_wsgi",
    version="0.0.1",
    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "hello_apig_wsgi"},
    packages=setuptools.find_packages(where="hello_apig_wsgi"),
    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws_lambda_python",
        "aws-cdk.aws_apigateway",
        "aws-cdk.aws_apigatewayv2",
        "aws-cdk.aws_efs",
        "aws-cdk.aws-appsync",
        "aws-cdk.aws_dynamodb",
        "aws-cdk.aws_codedeploy",
        "aws-cdk.aws_codepipeline",
        "aws-cdk.aws_codepipeline_actions",
        "aws-cdk.aws_cloudwatch",
        "aws-cdk.pipelines",
        "mangum",
        "apig-wsgi",
        "flask",
        "quart",
        "uvicorn",
        "boto3",
        "pydantic",
        "pytest",
        "requests",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
