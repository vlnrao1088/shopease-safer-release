FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# test stage = our QUALITY GATE (lint + unit tests + 80% coverage)
FROM base AS test
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY app.py test_app.py ./
RUN flake8 app.py test_app.py --max-line-length=100 && pytest -q --cov=app --cov-fail-under=100

# runtime stage = the small image we ship
FROM base AS runtime
COPY app.py .
RUN useradd --create-home appuser
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 CMD python -c "import urllib.request as u; u.urlopen('http://localhost:5000/health', timeout=2)"
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]