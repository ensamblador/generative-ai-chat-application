#!/usr/bin/env python3
import os

import aws_cdk as cdk

from personal_assistant_add_data import PersonalAssistantAddDataStack


app = cdk.App()
PersonalAssistantAddDataStack(app, "PERSONAL-ASSISTANT-ADD-DATA")

app.synth()
