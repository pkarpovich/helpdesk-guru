package main

import "log"

func main() {
	err := initGptServiceConnection()
	if err != nil {
		log.Fatalf("fail to connect to gpt service: %v", err)
	}

	startTelegramBot()
}
