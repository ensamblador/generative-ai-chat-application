import aws_cdk as core
import aws_cdk.assertions as assertions

from 02_personal_assistant_ecs.02_personal_assistant_ecs_stack import 02PersonalAssistantEcsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in 02_personal_assistant_ecs/02_personal_assistant_ecs_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = 02PersonalAssistantEcsStack(app, "02-personal-assistant-ecs")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
