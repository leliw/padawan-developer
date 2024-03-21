FROM python:3.11.7-slim

ENV WEBSITE_PORT=8000
EXPOSE 8000
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
RUN python -m pip install --upgrade pip
# Install pip requirements
COPY backend/requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY ./backend/ /app

VOLUME /workspace

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:$WEBSITE_PORT", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
