# 🌟 Instagram Service API 🌟

![Python](https://img.shields.io/badge/Python-3.11.4-blue?style=for-the-badge&logo=python)
![gRPC](https://img.shields.io/badge/gRPC-Unary-green?style=for-the-badge&logo=grpc)
![Status](https://img.shields.io/badge/Status-Active-green?style=for-the-badge&logo=check-circle)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=open-source-initiative)

Welcome to the **Instagram Service API** project! This project utilizes Python to create an API for interacting with Instagram, and communicates with other services via gRPC. ✨


## 📖 Description

> The Instagram Service API handles interactions with Instagram, including sending and reading direct messages. It communicates with other microservices through unary gRPC calls.

🛠 **Technologies Used**:
- **Python**: The main programming language used.
- **instagrapi**: A library for interacting with Instagram.
- **gRPC**: A high-performance RPC framework.
- **Docker Compose**: For containerizing the application.
- **GitHub Actions**: For continuous integration and deployment.

## Overview

`instagram-service` is a microservice designed to interact with Instagram's API, providing functionality to send and read direct messages. This service is part of a larger project and communicates with other services via gRPC (unary). It is built using Python and leverages the `instagrapi` library for Instagram API interactions.

## Features

- **Login to Instagram**: Authenticate and log in to an Instagram account.
- **Send Direct Messages**: Programmatically send direct messages to Instagram users.
- **Read Direct Messages**: Retrieve and read direct messages from Instagram.

## Installation

### Prerequisites

- Python 3.11.4
- Docker Compose (for containerized deployment)

### Local Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/pkarpovich/helpdesk-guru.git
    cd helpdesk-guru
    ```

2. Install dependencies:

    ```bash
    poetry install
    ```

### Docker Setup

1. Pull Docker image:

    ```bash
    docker compose pull
    ```

2. Run the Docker container:

    ```bash
    docker compose up -d --build 
    ```

### gRPC Communication
> This service communicates with other microservices using gRPC. The protobuf definitions are compiled using betterproto. Ensure your .proto files are placed in the protos directory.

### Compiling Protobuf Files

```bash
make build_proto
```
### Testing
Tests are written using pytest. To run tests, execute:
```bash
 poetry run pytest tests
```

## 📄 Licence
> This project is licensed under the MIT License - see the LICENSE file for details.

