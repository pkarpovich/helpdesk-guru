package main

import (
	"context"
	"fmt"
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

	answer, err := modelCtx.Ask(context.Background(), Message{Role: "user", Content: "Куда я могу написать?"})

	if err != nil {
		log.Printf("Error asking: %v\n", err)
		return
	}

	fmt.Println(answer)
}
