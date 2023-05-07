package main

import (
	"context"
	"github.com/sashabaranov/go-openai"
)

type Message struct {
	Role    string
	Content string
}

type ModelContext struct {
	authToken string
	model     string
	messages  []Message
	client    *openai.Client
}

func CreateModelContext(authToken string, model string) ModelContext {
	client := openai.NewClient(authToken)

	return ModelContext{
		authToken: authToken,
		model:     model,
		messages:  make([]Message, 0),
		client:    client,
	}
}

func (mc *ModelContext) InitMessageContext(messages []Message) {
	mc.messages = messages
}

func (mc *ModelContext) Ask(ctx context.Context) (string, error) {
	messages := make([]openai.ChatCompletionMessage, 0)

	for _, message := range mc.messages {
		messages = append(messages, openai.ChatCompletionMessage{
			Role:    message.Role,
			Content: message.Content,
		})
	}

	resp, err := mc.client.CreateChatCompletion(
		ctx,
		openai.ChatCompletionRequest{
			Model:    mc.model,
			Messages: messages,
		},
	)

	if err != nil {
		return "", err
	}

	return resp.Choices[0].Message.Content, nil
}
