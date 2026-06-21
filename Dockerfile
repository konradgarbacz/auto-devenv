FROM python:3.12.13-alpine
WORKDIR /Project-for-GitHub
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]