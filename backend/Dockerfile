FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create the database
RUN python init_db.py

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "src/main.py"]

