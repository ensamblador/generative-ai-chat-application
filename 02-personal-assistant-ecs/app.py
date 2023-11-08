#!/usr/bin/env python3
import os

import aws_cdk as cdk

from personal_assistant_ecs import PersonalAssistantECS


app = cdk.App()

stk = PersonalAssistantECS(app, "PERSONAL-ASSISTANT-ECS")

app.synth()
