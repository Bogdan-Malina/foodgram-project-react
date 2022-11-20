FROM python:3.8.5
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]