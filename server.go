package main

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"time"
)

type ServerContext struct {
	ModelCtx *ModelContext
}

type ErrorResponse struct {
	Message string `json:"message"`
}

func NewServerContext(modelCtx *ModelContext) *ServerContext {
	return &ServerContext{ModelCtx: modelCtx}
}

func LoggerMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		bodyBytes, _ := io.ReadAll(r.Body)
		r.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))

		next.ServeHTTP(w, r)

		log.Printf("%s %s %s %v\nRequest body: %s", r.RemoteAddr, r.Method, r.URL, time.Since(start), string(bodyBytes))
	})
}

func WriteJSONError(w http.ResponseWriter, errMsg string, status int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(ErrorResponse{Message: errMsg})
}

type AskQuestionRequest struct {
	Question string `json:"question"`
}

type AskQuestionResponse struct {
	Answer string `json:"answer"`
}

func (ctx *ServerContext) AskQuestionHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		WriteJSONError(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var body AskQuestionRequest
	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		WriteJSONError(w, "Invalid JSON input", http.StatusBadRequest)
		return
	}

	answer, err := ctx.ModelCtx.Ask(context.Background(), Message{
		Content: body.Question,
		Role:    "user",
	})
	if err != nil {
		WriteJSONError(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(AskQuestionResponse{Answer: answer})
}

func (ctx *ServerContext) ClearMessagesHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		WriteJSONError(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	ctx.ModelCtx.ClearUserMessages()

	w.WriteHeader(http.StatusOK)
}

func StartServer(serverCtx *ServerContext, addr string) {
	mux := http.NewServeMux()
	mux.Handle("/ask", http.HandlerFunc(serverCtx.AskQuestionHandler))
	mux.Handle("/clear", http.HandlerFunc(serverCtx.ClearMessagesHandler))

	loggedMux := LoggerMiddleware(mux)
	http.ListenAndServe(addr, loggedMux)
}
