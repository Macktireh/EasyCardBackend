# EasyCardBackend

## Project Description

EasyCardBackend is a backend service designed to support the EasyCardGUIDesktop application. This API provides endpoints for user authentication, credit card management and card extraction functionalities using artificial intelligence.

## Features

- **User Authentication**: Provides endpoints for user login and signup.
- **Credit Card Management**: Offers endpoints to create, retrieve, update, and delete credit card information.
- **Card Extraction**: Allows users to extract credit card numbers from images through dedicated endpoints.

## API Documentation

### Auth

- **User Login**: POST - `http://localhost:5000/api/auth/login`
- **User Signup**: POST - `http://localhost:5000/api/auth/signup`
- **Verify API Key**: GET - `http://localhost:5000/api/auth/verify`

### Card

- **Create New Card**: POST - `http://localhost:5000/api/cards`
- **List All Registered Cards**: GET - `http://localhost:5000/api/cards`
- **Create All New Card**: POST - `http://localhost:5000/api/cards/all`
- **Extract Card Number**: POST - `http://localhost:5000/api/cards/extract`
- **Update Card**: PATCH - `http://localhost:5000/api/cards/:publicId`
- **Delete Card**: DELETE - `http://localhost:5000/api/cards/:publicId`
- **Get Card by ID**: GET - `http://localhost:5000/api/cards/:publicId`

## Prerequisites

- Python 3.10 or higher
- Tesseract-OCR (download [here](https://github.com/tesseract-ocr/tesseract))

## Installation

### 1. Clone the Project

```bash
git clone https://github.com/Macktireh/EasyCardBackend.git
```

```bash
cd EasyCardBackend
```

### 2. Install Dependencies

```bash
poetry install
```

## Configuration

Before running the EasyCardBackend service, ensure that the database configurations are set up correctly. You can configure the database connection details in the `config/settings.py` file.

Additionally, make sure to create a `.env` file based on the provided example file `.env.example`. You can copy the contents of `.env.example` and save it as `.env`, then update the variables with your actual values.

## Usage

### Running the Server

```bash
python app.py
```

The server will start running at `http://localhost:5000`.

## License

This project is licensed under the [MIT License](LICENSE).
