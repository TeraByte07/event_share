# **Event Management API**

A FastAPI-based backend service for creating, updating, and managing events with support for image uploads. Built with FastAPI, SQLAlchemy, and PostgreSQL

## Features

Create, read, update, and delete events

Upload and update event banners/images

Store event details (name, description, date, etc.)

Database integration with SQLAlchemy

FastAPI docs with Swagger UI and ReDoc

## Tech Stack

FastAPI – API framework

SQLAlchemy – ORM for database interactions

PostgreSQL / SQLite – database

Pydantic – request/response validation

Uvicorn – ASGI server

## Project Structure

    event_api/
    │── app/
    │   ├── models/
    │   ├── routes/
    │   ├── services/
    │   ├── schemas/
    │   └── main.py
    │
    ├── requirements.txt
    └── README.md

## Installation & Setup

### 1: Clone the repository

    git clone https://github.com/your-username/event-api.git
    cd event-api

### 2: Create and activate a virtual environment

    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows

### 3: Install dependencies

    pip install -r requirements.txt

### 4: Run the server

    uvicorn app.main:app --reload

