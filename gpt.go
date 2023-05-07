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
	authToken       string
	model           string
	contextMessages []Message
	userMessages    []Message
	client          *openai.Client
}

func CreateModelContext(authToken string, model string) ModelContext {
	client := openai.NewClient(authToken)

	return ModelContext{
		authToken:       authToken,
		model:           model,
		userMessages:    make([]Message, 0),
		contextMessages: make([]Message, 0),
		client:          client,
	}
}

func (mc *ModelContext) InitContextMessages(messages []Message) {
	mc.contextMessages = messages
}

func (mc *ModelContext) ClearUserMessages() {
	mc.userMessages = make([]Message, 0)
}

func (mc *ModelContext) Ask(ctx context.Context, message Message) (string, error) {
	mc.userMessages = append(mc.userMessages, message)

	messages := append(mc.contextMessages, mc.userMessages...)
	aiMessages := castToOpenAIMessages(messages)

	resp, err := mc.client.CreateChatCompletion(
		ctx,
		openai.ChatCompletionRequest{
			Model:    mc.model,
			Messages: aiMessages,
		},
	)

	if err != nil {
		return "", err
	}

	return resp.Choices[0].Message.Content, nil
}

func castToOpenAIMessages(messages []Message) []openai.ChatCompletionMessage {
	openAIMessages := make([]openai.ChatCompletionMessage, 0)

	for _, message := range messages {
		openAIMessages = append(openAIMessages, openai.ChatCompletionMessage{
			Role:    message.Role,
			Content: message.Content,
		})
	}

	return openAIMessages
}
