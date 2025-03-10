FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV OPENAI_API_KEY="MY_OPENAI_API_KEY"
ENV AZURE_OCR_ENDPOINT="MY_AZURE_OCR_ENDPOINT"
ENV AZURE_OCR_API_KEY="MY_AZURE_OCR_API_KEY"

EXPOSE 8080 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]