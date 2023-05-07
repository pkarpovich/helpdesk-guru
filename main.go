package main

import (
	"context"
	"fmt"
	"os"
)

func main() {
	token := os.Getenv("OPENAI_API_KEY")

	modelCtx := CreateModelContext(token, "gpt-3.5-turbo")
	modelCtx.InitMessageContext([]Message{
		{
			Role:    "user",
			Content: "Как называется Ваша компания и зарегистрирована ли она?",
		},
	})

	answer, err := modelCtx.Ask(context.Background())

	if err != nil {
		fmt.Printf("ChatCompletion error: %v\n", err)
		return
	}

	fmt.Println(answer)
}
