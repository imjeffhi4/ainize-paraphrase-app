FROM imjeffhi4/paraphrasemodel

WORKDIR /app

COPY ./public /app/public/
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "Paraphrase:app", "--host", "0.0.0.0", "--port", "8000"]