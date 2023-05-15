package main

import (
	"context"
	"fmt"
	pb "github.com/pkarpovich/helpdesk-guru/services/telegram-bot/lib"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"log"
)

var conn *grpc.ClientConn

func initGptServiceConnection() error {
	var err error
	conn, err = grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
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

func main() {
	err := initGptServiceConnection()
	if err != nil {
		log.Fatalf("fail to connect to gpt service: %v", err)
	}

	answer, err := askGpt("Как называется ваша компания?")
	if err != nil {
		log.Fatalf("fail to ask gpt: %v", err)
	}

	fmt.Println(answer)
}
