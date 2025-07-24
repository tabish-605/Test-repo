FROM python:3.11-alpine
RUN pip install locust
COPY locustfile.py /locustfile.py
ENTRYPOINT ["locust", "-f", "/locustfile.py", "--host", "http://frontend"]