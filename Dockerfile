FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port NiceGUI/Uvicorn runs on
EXPOSE 8080

# Command to run the application using Gunicorn
CMD ["gunicorn", "ui:ui.run_with(port=8080, title='MMM Studio', reload=False)", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]