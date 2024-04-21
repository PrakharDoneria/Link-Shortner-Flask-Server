# Flask URL Shortener

A simple URL shortening service built with Flask and MySQL.

## Introduction

This project provides a basic implementation of a URL shortening service using Python's Flask framework for the backend and MySQL for data storage. It allows users to generate shortcodes for long URLs, which can then be used to redirect to the original URLs.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/prakhardoneria/link-shortner-flask-server.git
   cd link-shortner-flask-server
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   This command will install all the required dependencies specified in the `requirements.txt` file.

3. **Configure MySQL**:

   - Create a MySQL database.
   - Update the `mysql_config` dictionary in `main.py` with your MySQL database configuration.

## Usage

1. **Start the Flask application**:

   ```bash
   python main.py
   ```

2. **Use the provided API endpoints to interact with the service**.

## Endpoints

- `POST /short`: Shorten a long URL.
  - Request Body: `{"long": "original_long_url"}`
  - Response Body: `{"shortened_url": "shortened_url"}`
- `GET /<shortcode>`: Redirect to the original URL associated with the provided shortcode.

## Hosting

You have several options for hosting your Flask application:

1. **Self-hosting**: Deploy your Flask application on a server of your choice. This could be a physical server or a cloud-based server provided by services like AWS, Google Cloud, or DigitalOcean.

2. **Platform as a Service (PaaS)**: Platforms like Heroku, PythonAnywhere, and AWS Elastic Beanstalk simplify the deployment process for Flask applications. You can deploy your application with just a few commands or clicks.

3. **Containerization**: Containerize your Flask application using Docker and deploy it on container orchestration platforms like Kubernetes. This gives you flexibility and scalability in managing your application.

Choose the hosting option that best fits your requirements and expertise.

## Installation

To install the project dependencies, run:

```bash
pip install -r requirements.txt
```

## Build

Since this is a Python Flask application, there's no explicit build step required. However, you may need to perform some setup tasks like configuring the database before running the application.

## Run

To run the Flask application, execute the following command:

```bash
python main.py
```

This command will start the Flask development server, and your application will be accessible at `http://localhost:5002` by default.

If you want to specify a different port, you can do so by passing the `--port` argument:

```bash
python main.py --port 8080
```

This will start the application on port 8080 instead of the default port 5002.

Remember to ensure that your MySQL database is running and properly configured before starting the Flask application.

## Updates

- Added functionality to check if a long URL already exists in the database and return the corresponding short URL if it does.
- If the long URL doesn't exist, a new short URL is generated and stored in the database.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvement, feel free to open an issue or submit a pull request.
