from aws_cdk import core
import aws_cdk as cdk
from ec2.ec2_stack import Ec2Stack

app = core.App()


Ec2Stack(app, "Ec2Stack", env=cdk.Environment(account='851725626130', region='us-east-1'))  # Pass the environment as an argument

# Synthesize the CloudFormation template
app.synth()
