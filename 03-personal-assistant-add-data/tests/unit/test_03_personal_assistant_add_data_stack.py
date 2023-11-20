import aws_cdk as core
import aws_cdk.assertions as assertions

from 03_personal_assistant_add_data.03_personal_assistant_add_data_stack import 03PersonalAssistantAddDataStack

# example tests. To run these tests, uncomment this file along with the example
# resource in 03_personal_assistant_add_data/03_personal_assistant_add_data_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = 03PersonalAssistantAddDataStack(app, "03-personal-assistant-add-data")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
