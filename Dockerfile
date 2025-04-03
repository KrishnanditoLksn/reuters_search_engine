FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    default-jdk \
    ant \
    git \
    build-essential \
    python3-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/default-java

# Create app directory
WORKDIR /app

# Download and build PyLucene
RUN wget https://downloads.apache.org/lucene/pylucene/pylucene-9.5.0-src.tar.gz \
    && tar -xzf pylucene-9.5.0-src.tar.gz \
    && cd pylucene-9.5.0 \
    && cd jcc \
    && python3 setup.py build \
    && python3 setup.py install \
    && cd .. \
    && make all install JCC='python -m jcc' ANT=ant PYTHON=python

# Set up working directory
WORKDIR /app/code

# Create a test script
RUN echo 'import lucene; print(f"PyLucene version: {lucene.VERSION}")' > test_lucene.py

# Command to run when container starts
CMD ["python", "test_lucene.py"]