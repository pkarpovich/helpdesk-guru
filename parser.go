package main

import (
	"bufio"
	"os"
	"strings"
)

func ParseFile(filepath string) ([]Message, error) {
	file, err := os.Open(filepath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var messages []Message
	scanner := bufio.NewScanner(file)
	role := ""
	content := ""

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())

		switch {
		case line == "":
			content = appendContent(&messages, role, content)
		case strings.HasPrefix(line, "-"):
			content = appendContent(&messages, role, content)
			role = roleSwitch(role)
			content = strings.TrimPrefix(line, "-")
		case content == "":
			content = line
		default:
			content = content + " " + line
		}
	}

	content = appendContent(&messages, role, content)

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return messages, nil
}

func appendContent(messages *[]Message, role string, content string) string {
	if content == "" {
		return content
	}

	*messages = append(*messages, Message{Role: role, Content: content})

	return content
}

func roleSwitch(role string) string {
	switch role {
	case "user":
		return "assistant"
	default:
		return "user"
	}
}
