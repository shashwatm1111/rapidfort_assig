# Step 1: Use a Python base image
FROM python:3.11-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy the application files
COPY . /app

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the app's port
EXPOSE 5000

# Step 6: Run the Flask app
CMD ["python", "app/app.py"]
