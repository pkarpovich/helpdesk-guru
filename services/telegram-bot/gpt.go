package main

import (
	"context"
	"fmt"
	pb "github.com/pkarpovich/helpdesk-guru/services/telegram-bot/lib"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

var conn *grpc.ClientConn

func initGptServiceConnection(config AppConfig) error {
	var err error
	conn, err = grpc.Dial(config.GptServiceAddress, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return fmt.Errorf("fail to dial: %v", err)
	}

	return nil
}

func askGpt(query, conversationId, contextName string) (string, error) {
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
