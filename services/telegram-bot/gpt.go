package main

import (
	"context"
	"fmt"
	pb "github.com/pkarpovich/helpdesk-guru/services/telegram-bot/lib"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"os"
)

var conn *grpc.ClientConn

func initGptServiceConnection() error {
	gptServiceAddress := getEnvOrDefault("GPT_SERVICE_ADDRESS", "localhost:50051")

	var err error
	conn, err = grpc.Dial(gptServiceAddress, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return fmt.Errorf("fail to dial: %v", err)
	}

	return nil
}

func askGpt(query, conversationId string) (string, error) {
	contextName := os.Getenv("CONTEXT_NAME")

	client := pb.NewGptServiceClient(conn)
	request := &pb.AskRequest{
		ConversationId: conversationId,
		ContextName:    contextName,
		Query:          query,
	}

	resp, err := client.Ask(context.Background(), request)
	if err != nil {
		return "", err
	}

	return resp.Answer, nil
}

func clearHistory() error {
	client := pb.NewGptServiceClient(conn)
	_, err := client.ClearHistory(context.Background(), &pb.ClearHistoryRequest{})
	if err != nil {
		return err
	}

	return nil
}
