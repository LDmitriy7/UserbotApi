FROM python:3.10-slim
WORKDIR /app
RUN pip install pdm
COPY pyproject.toml pdm.lock ./
RUN pdm install
COPY . .
CMD pdm start