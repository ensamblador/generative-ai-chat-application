FROM public.ecr.aws/docker/library/python:3.9-slim
WORKDIR /app
ADD .  /app
RUN pip3 install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "chatbot_app.py", "--server.port=8501"]