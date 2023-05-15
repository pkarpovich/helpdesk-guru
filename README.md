# Helpdesk Guru

Helpdesk-Guru is an intelligent Telegram bot powered by Golang, designed to help answer user queries by interacting with a Python-based GPT service. The bot utilizes information from parsed user documents to provide accurate responses, and includes user query rate-limiting and conversation reset features for enhanced usability. Docker Compose is used for effortless setup and deployment.

## Features

- Responds to user messages with generated text from GPT.
- Rate limit for user queries to prevent spamming.
- Clear command to erase previous queries and responses.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker & Docker Compose
- A Telegram Bot Token (you can obtain this by creating a bot on Telegram)
- OpenAI API Key

### Environment Variable

The project uses the following environment variables:

- `TELEGRAM_BOT_TOKEN` - Your telegram bot token.
- `OPENAI_API_KEY` - Your OpenAI API key.
- `OPENAI_MODEL` - The model to use with OpenAI.
- `PERSIST_DIRECTORY` - The directory for persisting data.

Create a `.env` file in the project root directory and add your environment variables:

```bash
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_MODEL=YOUR_OPENAI_MODEL
PERSIST_DIRECTORY=YOUR_PERSIST_DIRECTORY
```

### Running the Bot and GPT Service with Docker Compose
You can run the entire system using Docker Compose:

```bash
docker-compose up --build
```
This will build the Docker images if they do not exist and start the services, namely, the telegram bot and the GPT service.

### Usage

Once started, you can interact with the bot on Telegram. You can use the following commands:

- `/start`: The bot will respond with a welcome message.
- `/clear`: The bot will clear its memory of previous queries and responses.
- For any other text, the bot will interact with the GPT service to generate a meaningful response.

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
