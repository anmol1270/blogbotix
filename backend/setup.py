from setuptools import setup, find_packages

setup(
    name="ai-blog-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "sqlalchemy>=1.4.23",
        "pydantic>=1.8.2",
        "pydantic-settings>=2.0.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "python-dotenv>=1.0.1",
        "alembic>=1.7.1",
        "psycopg2-binary>=2.9.1",
        "python-docx>=1.0.1",
        "PyPDF2>=3.0.1",
        "email-validator>=1.1.3",
    ],
) 