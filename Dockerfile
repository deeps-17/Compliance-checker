# Use official Python slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependencies first (Docker caching — only reinstalls if requirements change)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Health check so Docker knows if the container is running properly
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]