# Start with a Python 3.11 base image
FROM python:3.10.2-slim

# Set the working directory in the container
WORKDIR /app

# Install system packages required for Playwright and other dependencies
RUN apt-get update && apt-get install -y wget gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a virtual environment within the container
RUN python -m venv /opt/venv

# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file first to leverage Docker cache
COPY /api/requirements.txt ./

# Install Python dependencies in the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright separately as it requires additional steps
RUN pip install playwright==1.44.0 && \
    playwright install --with-deps

# Copy the rest of your application
COPY /api .

# Command to run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]