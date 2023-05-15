package main

import "os"

func getEnvOrDefault(key, defaultValue string) string {
	value := getEnv(key)
	if value == "" {
		return defaultValue
	}

	return value
}

func getEnv(key string) string {
	return os.Getenv(key)
}
