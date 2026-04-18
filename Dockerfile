FROM python:3.12-slim

# Install uv
RUN pip install uv

# Set work directory
WORKDIR /app

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run app with uv + uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]