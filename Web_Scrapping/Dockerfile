# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install necessary system packages
RUN apt-get update \
    && apt-get install -y wget gnupg unzip curl xvfb libxi6 libgconf-2-4 libxrandr2 libxss1 libxtst6 libxcursor1 libnss3 libasound2 fonts-liberation libappindicator3-1 libxkbcommon-x11-0 xdg-utils \
    && wget -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i /tmp/google-chrome-stable_current_amd64.deb || apt-get -fy install \
    && rm /tmp/google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip


# Ensure the Chrome binary is accessible
ENV PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/google-chrome:${PATH}"

# Make port 80 available to the world outside this container
EXPOSE 80

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Define the entrypoint command
CMD ["python", "app.py"]
