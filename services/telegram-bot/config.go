package main

import (
	"github.com/joho/godotenv"
	"github.com/kelseyhightower/envconfig"
	"log"
	"os"
)

type AppConfig struct {
	GptServiceAddress string `envconfig:"GPT_SERVICE_ADDRESS" default:"localhost:50051"`
	TelegramBotToken  string `envconfig:"TELEGRAM_BOT_TOKEN" required:"true"`
	AppEnvironment    string `envconfig:"APP_ENV" default:"development"`
	ContextName       string `envconfig:"CONTEXT_NAME" required:"true"`
}

func loadConfig() AppConfig {
	var appConfig AppConfig

	loadEnvVariablesIfNeeded()

	err := envconfig.Process("", &appConfig)
	if err != nil {
		log.Fatalf(err.Error())
	}

	return appConfig
}

func loadEnvVariablesIfNeeded() {
	env := os.Getenv("APP_ENV")
	if env == "production" {
		return
	}

	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

}
