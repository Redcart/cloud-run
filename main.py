import os

from fastapi import FastAPI
from google.cloud import secretmanager


GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
INPUT_DATASET = os.getenv("INPUT_DATASET")
OUTPUT_DATASET = os.getenv("OUTPUT_DATASET")
API_KEY = os.getenv("API_KEY", "Not found in environment variables")
GITHUB_SECRET_VAR = os.getenv("SECRET_VAR", "Not found in environment variables")

app = FastAPI()

def get_secret(secret_name: str, version: str = "latest") -> str:
    # In a real application, you would retrieve the secret from a secure vault or secret manager
    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/{GCP_PROJECT_ID}/secrets/{secret_name}/versions/{version}"
    response = client.access_secret_version(request={"name": secret_path})
    return response.payload.data.decode("UTF-8")

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Non sensitive environment variables injected at deployment time 
@app.get("/display/env-variables")
async def display_env_variables():
    return {"message": f"INPUT_DATASET: {INPUT_DATASET}, OUTPUT_DATASET: {OUTPUT_DATASET}"}

# Sensitive environment variable retrieved at deployment time from GitHub Secrets
@app.get("/display/secrets-github")
async def display_secrets_github():
    return {"message": f"SECRET_VAR from GitHub Secrets: {GITHUB_SECRET_VAR}"}

# Sensitive environment variable injected at deployment time from Secret Manager
@app.get("/display/secrets")
async def display_secrets():
    return {"message": f"API_KEY: {API_KEY}"}

# Sensitive environment variable retrieved at runtime from Secret Manager
@app.get("/display/secrets-runtime")
async def display_secrets_runtime():
    password = get_secret(secret_name="PASSWORD")
    return {"message": f"PASSWORD: {password}"}