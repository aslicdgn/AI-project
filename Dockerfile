# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container (this will be the /app directory inside the container)
WORKDIR /app

# Copy the contents of the current directory into the container at /app
COPY . /app

# Install dependencies from requirements.txt (if you have one)
# If you don’t have a requirements.txt yet, you can skip this step or add it later.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# If you're running the try.py script, define the command to run it
CMD ["python", "try.py"]
