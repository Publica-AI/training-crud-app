#  Introduction to FastAPI Course

This project provides a hands-on introduction to FastAPI by guiding learners through a progressive transformation—from basic HTTP request handling to building a fully functional CRUD API.

## Project Structure

### `http.py`
Demonstrates how to handle basic HTTP requests using Python’s built-in `http.server` module. This file introduces core web concepts like handling `GET` and `POST` requests without any external frameworks.

### `main_intro.py`
Reimplements the logic from `http.py` using FastAPI. This shows how FastAPI simplifies API development with cleaner syntax, automatic routing, and integrated documentation.

### `code.py`
Explains how to define and document **two related tables** (e.g., Users and Contacts) within one Swagger (OpenAPI) interface using FastAPI models. The examples use data from:
- `user.csv`
- `contact.csv`

### `main.py`
Contains a complete CRUD (Create, Read, Update, Delete) implementation for managing contact records. This is the final and most complete version of the API, showcasing FastAPI’s full capabilities.

##  Learning Goals

- Understand basic HTTP request handling with `http.server`.
- Transition from low-level HTTP to FastAPI for cleaner and scalable APIs.
- Learn how to represent multiple data models in Swagger UI using FastAPI.
- Implement full CRUD functionality for a real-world use case.

---

Feel free to fork this project, try out the examples, and build your own API with FastAPI!

