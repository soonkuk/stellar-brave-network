package commands

import (
	"github.com/spf13/cobra"
	"github.com/soonkuk/stellar-brave-network/cli/command"
	"github.com/soonkuk/stellar-brave-network/cli/command/account"
	"github.com/soonkuk/stellar-brave-network/cli/command/keypair"
	"github.com/soonkuk/stellar-brave-network/cli/command/transaction"
)

func AddCommands(cmd *cobra.Command, cli *command.BraveCli) {
	cmd.AddCommand(
		keypair.NewKeyPairCommand(cli),
		account.NewAccountCommand(cli),
		transaction.NewTransactionCommand(cli),
	)
}
