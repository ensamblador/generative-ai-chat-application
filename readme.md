# Aplicación con IA Generativa

En este proyecto crearás una aplicación en AWS que aprovecha IA generativa directo en el código. El objetivo es ir construyendo paso a paso las distintas funcionalidades de la aplicación, agregando cada vez más funcionalidades. A continuación los links a los capítulos:

## 1. [Construye un Asistente Personal con super poderes de IA Generativa](./01-personal-assistant/readme.md)

Acá creamos un asistente personal con capacidades de IA generativa de forma local y privada. Un paso a paso de cómo construir una aplicación conversacional que invoque modelos como Claude de Anthropic a través de Amazon Bedrock. Además  la interfaz con web con Streamlit y el backend con Langchain para interactuar con el modelo de lenguaje a través de prompts.





## 2. [Despliega tu Asistente de IA Generativa en AWS](/02-personal-assistant-ecs/README.md)

Este artículo de blog continúa el proyecto  anterior cubriendo cómo empaquetar la aplicación usando Docker, y desplegarla en AWS utilizando servicios como Elastic Container Service (ECS). Se integra la autenticación usando Amazon Cognito para permitir el acceso solo a usuarios autenticados.

Con esto el asistente está accesible de forma segura desde cualquier dispositivo como una aplicación web.


## 2. [Agrega y consulta documentos a tu Asistente de IA Generativa](/03-personal-assistant-add-data/readme.md)

Desde manuales de usuario, reportes técnicos e informes de investigación, hasta contratos legales y transcripciones de llamadas, las empresas acumulan una enorme cantidad de contenido en formato de texto no estructurado. Procesar y extraer conocimiento útil de estos documentos suele ser una tarea tediosa y propensa a errores cuando se hace manualmente. Además, encontrar y recuperar información específica entre cientos o miles de documentos puede ser como buscar una aguja en un pajar.

En este artículo, complementarás el asistente de IA conversacional para ayudar a resolver estos desafíos. Utilizando técnicas de búsqueda semántica en documentos utilizando modelos embeddings  y procesamiento con LLM para la respuesta.
