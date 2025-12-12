FROM python:3.11-slim

WORKDIR /project

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# --- Копіюємо весь код проєкту в контейнер ---
COPY . /project

CMD ["python", "main.py"]