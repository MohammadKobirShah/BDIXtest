FROM python:3.11-slim

# Install dependencies
RUN pip install --no-cache-dir \
    requests \
    PySocks \
    rich \
    tabulate \
    geoip2 \
    speedtest-cli \
    pyyaml

# Create app directory
WORKDIR /app

# Copy project files
COPY check_proxies.py ./
COPY proxies.yaml ./
COPY requirements.txt ./

# Create output directory
RUN mkdir /output

# Entry point
CMD ["python", "check_proxies.py"]
