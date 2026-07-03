FROM python:3.11-slim-bookworm

WORKDIR /app

# Install Java and procps (contains the ps command)
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Configure Java
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]