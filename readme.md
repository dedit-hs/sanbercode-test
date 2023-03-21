# Sanbercode Assessment Test

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://docs.python.org/3/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAPI](https://img.shields.io/badge/openapi-6BA539?style=for-the-badge&logo=openapi-initiative&logoColor=fff)](https://www.openapis.org/)
[![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io/)

## Description

*Assessment Test untuk Junior Backend @IT Consultant*

Membuat API sederhana dengan bahasa pemrograman python menggunakan Microframework FastAPI.

## Installation

- Jalankan docker-compose build:

  ```docker-compose build
  ```

- Jalankan perintah docker-compose up:

  ```docker-compose up
  ```

- Lakukan migrasi database menggunakan alembic:

  ```docker-compose run app alembic revision --autogenerate -m "pesan_revisi"
  ```

- Terakhir, Jalankan perintah :

  ```docker-compose run app alembic upgrade head
  ```

- Buka `localhost:8000/docs` untuk melihat API Documentation.
