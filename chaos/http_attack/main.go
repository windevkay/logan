package main

import (
	"bytes"
	"crypto/rand"
	"flag"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
)

type config struct {
	url  string
	verb string
}

func main() {
	var cfg config

	flag.StringVar(&cfg.url, "url", "", "target url")
	flag.StringVar(&cfg.verb, "verb", "", "request verb")

	flag.Parse()

	terminate := make(chan int)

	go func() {
		quit := make(chan os.Signal, 1)
		signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
		s := <-quit

		log.Println("attempting to terminate actions: ", s.String())

		terminate <- 1
	}()

	// generate 100mb of random data
	data := make([]byte, 100*1024*1024)
	_, err := rand.Read(data)
	if err != nil {
		log.Fatal("error generating POST data", err)
	}

	for {
		if cfg.verb == http.MethodGet {
			http.Get(cfg.url)
		} else {
			_, err := http.Post(cfg.url, "application/octet-stream", bytes.NewBuffer(data))
			log.Println("targetting endpoint", err)
		}

		select {
		case t := <-terminate:
			if t == 1 {
				return
			}
		default:
		}
	}
}
