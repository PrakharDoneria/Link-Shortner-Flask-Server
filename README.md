# Flask URL Shortener

A simple URL shortening service built with Flask and MySQL.

## Introduction

This project provides a basic implementation of a URL shortening service using Python's Flask framework for the backend and MySQL for data storage. It allows users to generate shortcodes for long URLs, which can then be used to redirect to the original URLs.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/prakhardoneria/link-shortner-flask-server.git
   cd link-shortner-flask-server
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure MySQL:
   
   - Create a MySQL database.
   - Update the `mysql_config` dictionary in `main.py` with your MySQL database configuration.

## Usage

1. Start the Flask application:

   ```bash
   python app.py
   ```

2. Use the provided API endpoints to interact with the service.

## Endpoints

- `POST /short`: Shorten a long URL.
  - Request Body: `{"long": "original_long_url"}`
  - Response Body: `{"shortened_url": "shortened_url"}`
- `GET /<shortcode>`: Redirect to the original URL associated with the provided shortcode.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvement, feel free to open an issue or submit a pull request.

