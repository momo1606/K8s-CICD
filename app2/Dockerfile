# Dockerfile for Container 2
FROM python:3.9-slim
 
WORKDIR /app
 
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
 
COPY . .

EXPOSE 6001

# Define environment variable
ENV NAME World


CMD ["hypercorn", "cont_2:app", "--bind", "0.0.0.0:6001"]