import importlib.metadata
packages = [
"openai",
"qdrant-client",
"pandas",
"sqlalchemy",
"psycopg2-binary",
"python-dotenv",
"pydantic",
"fastapi",
"uvicorn",
"ipykernel"

    ]
for pkg in packages:
    try:
        version = importlib.metadata.version(pkg)
        print(f"{pkg}=={version}")
    except importlib.metadata.PackageNotFoundError:
        print(f"{pkg} (not installed)")