FROM python:3.11-slim

WORKDIR /radar

# Copy requirements and install dependencies
COPY radar_sim/requirements.txt .
RUN pip install -r requirements.txt


# Copy the application code
COPY radar_sim/ .

EXPOSE 5000

CMD ["python", "app.py"]
