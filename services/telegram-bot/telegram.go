package main

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
	"log"
	"time"
)

const (
	BotWelcomeMessage   = "Привет! Я - Helpdesk-Guru, твой бот-помощник. Готов помочь тебе с ответами на вопросы, разъяснить что-то или просто поделиться полезной информацией.\n\nНе знаешь с чего начать? Просто задай мне вопрос. Если захочешь начать всё с начала, напиши команду /clear, и я забуду всё, что мы обсуждали до этого.\n\nЕсли что-то пойдёт не так, не волнуйся и пиши мне - я здесь, чтобы помочь!"
	BotClearMessage     = "Хорошо, все предыдущие вопросы и ответы были удалены. Мы можем начать с чистого листа! Если у тебя есть вопросы, просто задай их мне - я здесь, чтобы помочь!"
	BotRateLimitMessage = "Тебя слишком много, отдохни..."
)

const (
	rateLimit = 2
	duration  = 1 * time.Minute
)

type User struct {
	lastMessages []time.Time
	banned       bool
}

var users = make(map[int]*User)

func checkRateLimit(userID int) bool {
	user, exists := users[userID]
	if !exists {
		user = &User{}
		users[userID] = user
	}

	now := time.Now()

	for len(user.lastMessages) > 0 && now.Sub(user.lastMessages[0]) > duration {
		user.lastMessages = user.lastMessages[1:]
	}

	if user.banned || len(user.lastMessages) >= rateLimit {
		return false
	}

	user.lastMessages = append(user.lastMessages, now)
	return true
}

func startTelegramBot(config AppConfig) {
	bot, err := tgbotapi.NewBotAPI(config.TelegramBotToken)
	if err != nil {
		log.Fatalf("fail to create bot: %v", err)
	}

	bot.Debug = true

	log.Printf("Authorized on account %s", bot.Self.UserName)

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60

	updates, err := bot.GetUpdatesChan(u)
	if err != nil {
		log.Fatalf("fail to get updates: %v", err)
	}

	for update := range updates {
		if update.Message == nil || update.Message.Text == "" {
			continue
		}

		log.Printf("[%s] %s", update.Message.From.UserName, update.Message.Text)

		userID := update.Message.From.ID
		if !checkRateLimit(userID) {
			msg := tgbotapi.NewMessage(update.Message.Chat.ID, BotRateLimitMessage)
			_, err := bot.Send(msg)
			if err != nil {
				log.Fatalf("fail to send message: %v", err)
			}
			continue
		}

		var msg tgbotapi.MessageConfig

		switch update.Message.Command() {
		case "start":
			msg = tgbotapi.NewMessage(update.Message.Chat.ID, BotWelcomeMessage)
		case "clear":
			err := clearHistory()
			if err != nil {
				log.Printf("fail to clear history: %v", err)
			}

			msg = tgbotapi.NewMessage(update.Message.Chat.ID, BotClearMessage)
		default:
			answer, err := askGpt(update.Message.Text, update.Message.From.UserName, config.ContextName)
			if err != nil {
				log.Printf("fail to ask gpt: %v", err)
			}

			msg = tgbotapi.NewMessage(update.Message.Chat.ID, answer)
			msg.ReplyToMessageID = update.Message.MessageID
		}

		_, err := bot.Send(msg)
		if err != nil {
			log.Fatalf("fail to send message: %v", err)
		}

		log.Printf("[bot] %s", msg.Text)
	}
}
