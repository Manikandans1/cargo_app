# Use the official Python image.
FROM python:3.9

# Set the working directory.
WORKDIR /app

# Copy the requirements file and install the dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code.
COPY . .

# Expose the port your FastAPI app runs on.
EXPOSE 8000

# Command to run your FastAPI application.
CMD ["uvicorn", "your_app:app", "--host", "0.0.0.0", "--port", "8000"]
