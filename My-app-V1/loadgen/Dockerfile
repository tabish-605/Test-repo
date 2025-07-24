FROM python:3.11-alpine
# 1. Install transient build deps
RUN apk add --no-cache \
      build-base \        # pulls in gcc, musl-dev, make, etc.
      linux-headers \
      python3-dev
RUN pip install locust
COPY locustfile.py /locustfile.py
ENTRYPOINT ["locust", "-f", "/locustfile.py", "--host", "http://frontend"]
