#|| Shree Swami Samartha ||
# 
# 
# Tasks:
# 1 Create a Dockerfile that builds your application.
# 2 Publish your Docker image (using Dockerfile) publicly to Docker Hub. (Your Docker image uses the same Dockerfile as this file in your GitHub repository)
# 3 Ensure Docker image is publicly accessible on and runs via podman run $IMAGE_NAME -e AIPROXY_TOKEN=$AIPROXY_TOKEN -p 8000:8000

FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app
 
RUN mkdir -p /data

COPY server.py /app

CMD ["uv","run","server.py"]
