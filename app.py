#!/usr/bin/env python3

from aws_cdk import core

from hello_apig_wsgi.hello_apig_wsgi_stack import HelloApigWsgiStack


app = core.App()
HelloApigWsgiStack(app, "hello-apig-wsgi")

app.synth()
