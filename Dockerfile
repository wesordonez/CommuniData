# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.6-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client \
    netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt list --installed | grep libpq


EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=data_visualizer.settings

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

RUN python -c "import psycopg2; print(psycopg2.__version__)"
RUN apt list --installed | grep libpq

WORKDIR /Data_Visualizer/app


# Copy entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
# RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . /Data_Visualizer

RUN python manage.py collectstatic --noinput

# Run entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /Data_Visualizer
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "data_visualizer.wsgi:application"]
