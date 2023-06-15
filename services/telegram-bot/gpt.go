package main

import (
	"context"
	"fmt"
	pb "github.com/pkarpovich/helpdesk-guru/services/telegram-bot/lib"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
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

func askGpt(query string) (string, error) {
	client := pb.NewGptServiceClient(conn)
	resp, err := client.Ask(context.Background(), &pb.AskRequest{Query: query})
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
