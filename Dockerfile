# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy application files
COPY main.py names.py ./

# Set ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Define PORT environment variable with default 8000
ENV PORT=8000

# Expose port
EXPOSE 8000

# Command to run the application using $PORT environment variable
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
