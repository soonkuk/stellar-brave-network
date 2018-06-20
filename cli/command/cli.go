package command

import (
	"net/http"
	"github.com/stellar/go/clients/horizon"
)

type BraveCli struct {
	Network struct {
		Passphrase string
		Horizon string
	}

	Account map[string]string
}

func (cli *BraveCli) HorizonClient1() *horizon.Client {
	return &horizon.Client{
		URL: "http://127.0.0.1:8000",
		HTTP: http.DefaultClient,
	}
}

func (cli *BraveCli) HorizonClient2() *horizon.Client {
	return &horizon.Client{
		URL: "http://127.0.0.1:8001",
		HTTP: http.DefaultClient,
	}
}
