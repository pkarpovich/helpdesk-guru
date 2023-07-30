package main

import (
	"log"
)

func main() {
	config := loadConfig()

	err := initGptServiceConnection(config)
	if err != nil {
		log.Fatalf("fail to connect to gpt service: %v", err)
	}

	startTelegramBot(config)
}
