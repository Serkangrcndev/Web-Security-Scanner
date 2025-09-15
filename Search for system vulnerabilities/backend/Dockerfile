# GuardMesh Backend Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    wget \
    git \
    unzip \
    nmap \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Nikto manually
RUN wget https://github.com/sullo/nikto/archive/master.zip \
    && unzip master.zip \
    && mv nikto-master /opt/nikto \
    && rm master.zip

# Install SQLMap manually
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap

# Install Go for Nuclei and ZAP
RUN wget -q https://go.dev/dl/go1.21.0.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz \
    && rm go1.21.0.linux-amd64.tar.gz

# Install Nuclei
ENV PATH=$PATH:/usr/local/go/bin
RUN go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Install OWASP ZAP (v2.16.1)
RUN wget https://github.com/zaproxy/zaproxy/releases/download/v2.16.1/ZAP_2.16.1_Linux.tar.gz \
    && tar -xzf ZAP_2.16.1_Linux.tar.gz \
    && mv ZAP_2.16.1 /opt/zap \
    && rm ZAP_2.16.1_Linux.tar.gz

# Install Shodan CLI
RUN pip install shodan

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (main.py, scanners, vs.)
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Add scanner tools to PATH
ENV PATH=$PATH:/opt/nikto/program:/opt/sqlmap:/opt/zap:/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
