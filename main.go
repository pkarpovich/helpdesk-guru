package main

import (
	"log"
	"os"
)

func main() {
	token := os.Getenv("OPENAI_API_KEY")
	if token == "" {
		log.Fatal("OPENAI_API_KEY environment variable is not set")
		return
	}

	model := os.Getenv("OPENAI_MODEL")
	if model == "" {
		model = "gpt-3.5-turbo"
	}

	contextFile := os.Getenv("CONTEXT_FILE")
	if contextFile == "" {
		contextFile = "context.txt"
	}

	messages, err := ParseFile(contextFile)
	if err != nil {
		log.Fatalf("Error parsing file: %v\n", err)
		return
	}

	modelCtx := CreateModelContext(token, model)
	modelCtx.InitContextMessages(messages)

	serverCtx := NewServerContext(&modelCtx)
	StartServer(serverCtx, ":8443")
}
