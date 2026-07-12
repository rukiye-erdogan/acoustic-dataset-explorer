FROM python:3.11-slim

LABEL org.opencontainers.image.title="Acoustic Dataset Explorer"
LABEL org.opencontainers.image.description="Interactive Streamlit dashboard for exploring standardised acoustic metadata."
LABEL org.opencontainers.image.source="https://github.com/rukiye-erdogan/acoustic-dataset-explorer"
LABEL org.opencontainers.image.url="https://acoustic-dataset-explorer.streamlit.app"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Rukiye Erdogan"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/home/appuser

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt \
    && groupadd --gid 10001 appuser \
    && useradd \
        --uid 10001 \
        --gid appuser \
        --create-home \
        --shell /usr/sbin/nologin \
        appuser

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health', timeout=3)" || exit 1

CMD ["streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true"]
