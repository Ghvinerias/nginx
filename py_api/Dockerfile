# Use the Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages

RUN pip install --proxy http://squid-test.lb.ge:8080 -r requirements.txt

# Expose the port the Flask app runs on
EXPOSE 5000

# Define the command to run the Flask application
CMD ["python", "app.py"]