# Aplicación con IA Generativa

En este proyecto crearás una aplicación en AWS que aprovecha IA generativa directo en el código. El objetivo es ir construyendo paso a paso las distintas funcionalidades de la aplicación, agregando cada vez más funcionalidades. A continuación los links a los capítulos:

## 1. [Construye un Asistente Personal con super poderes de IA Generativa](./01-personal-assistant/readme.md)

Acá creamos un asistente personal con capacidades de IA generativa de forma local y privada. Un paso a paso de cómo construir una aplicación conversacional que invoque modelos como Claude de Anthropic a través de Amazon Bedrock. Además  la interfaz con web con Streamlit y el backend con Langchain para interactuar con el modelo de lenguaje a través de prompts. 




## 2. [Despliega tu Asistente de IA Generativa en AWS](/02-personal-assistant-ecs/README.md)

<table style="border:none; width:100%"><tr><td style="width:60%">Este artículo de blog continúa el proyecto  anterior cubriendo cómo empaquetar la aplicación usando Docker, y desplegarla en AWS utilizando servicios como Elastic Container Service (ECS). Se integra la autenticación usando Amazon Cognito para permitir el acceso solo a usuarios autenticados.

Con esto el asistente está accesible de forma segura desde cualquier dispositivo como una aplicación web. </td><td>![](/02-personal-assistant-ecs/media/coover.png)</td></tr></table>