# Use the Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages

RUN pip install -r wheelhouse/requirements.txt --no-index --find-links wheelhouse

# Expose the port the Flask app runs on
EXPOSE 5000

# Define the command to run the Flask application
CMD ["python", "app.py"]