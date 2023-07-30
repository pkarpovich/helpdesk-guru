package main

import (
	"github.com/joho/godotenv"
	"github.com/kelseyhightower/envconfig"
	"log"
)

type AppConfig struct {
	GptServiceAddress string `envconfig:"GPT_SERVICE_ADDRESS" default:"localhost:50051"`
	TelegramBotToken  string `envconfig:"TELEGRAM_BOT_TOKEN" required:"true"`
	ContextName       string `envconfig:"CONTEXT_NAME" required:"true"`
}

func loadConfig() AppConfig {
	var appConfig AppConfig

	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	err = envconfig.Process("", &appConfig)
	if err != nil {
		log.Fatalf(err.Error())
	}

	return appConfig
}
