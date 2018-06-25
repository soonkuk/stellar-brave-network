package transaction

import (
	"fmt"

	"github.com/soonkuk/stellar-brave-network/cli/command"
	"github.com/spf13/cobra"
	"github.com/stellar/go/build"
	"github.com/stellar/go/clients/horizon"
)

func NewTransactionCommand(cli *command.BraveCli) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "transaction",
		Short: "transaction",
		Long:  "",
	}

	fund := &cobra.Command{
		Use:   "fund",
		Short: "fund",
		Long:  "create account with initial balance",
		Run: func(cmd *cobra.Command, args []string) {
			seed := cmd.Flags().Lookup("seed").Value.String()
			address := cmd.Flags().Lookup("address").Value.String()
			amount := cmd.Flags().Lookup("amount").Value.String()

			tx, err := build.Transaction(
				build.Network{Passphrase: cli.Network.Passphrase},
				build.SourceAccount{AddressOrSeed: seed},
				build.AutoSequence{SequenceProvider: cli.HorizonClient1()},
				build.CreateAccount(
					build.Destination{AddressOrSeed: address},
					build.NativeAmount{Amount: amount},
				),
			)

			if err != nil {
				panic(err)
			}

			submit(cli.HorizonClient1(), tx, seed)
		},
	}

	fund.Flags().String("seed", "", "")
	fund.Flags().String("address", "", "")
	fund.Flags().String("amount", "", "")
	fund.MarkFlagRequired("seed")
	fund.MarkFlagRequired("address")
	fund.MarkFlagRequired("amount")

	payment := &cobra.Command{
		Use:   "payment",
		Short: "payment",
		Long:  "",
		Run: func(cmd *cobra.Command, args []string) {
			seed := cmd.Flags().Lookup("seed").Value.String()
			address := cmd.Flags().Lookup("address").Value.String()
			amount := cmd.Flags().Lookup("amount").Value.String()

			tx, err := build.Transaction(
				build.Network{Passphrase: cli.Network.Passphrase},
				build.SourceAccount{AddressOrSeed: seed},
				build.AutoSequence{SequenceProvider: cli.HorizonClient1()},
				build.Payment(
					build.Destination{AddressOrSeed: address},
					build.NativeAmount{Amount: amount},
				),
			)

			if err != nil {
				panic(err)
			}

			submit(cli.HorizonClient1(), tx, seed)
		},
	}

	payment.Flags().String("seed", "", "")
	payment.Flags().String("address", "", "")
	payment.Flags().String("amount", "", "")
	payment.MarkFlagRequired("seed")
	payment.MarkFlagRequired("address")
	payment.MarkFlagRequired("amount")

	payments := &cobra.Command{
		Use:   "payments",
		Short: "payments",
		Long:  "",
		Run: func(cmd *cobra.Command, args []string) {
			seed := cmd.Flags().Lookup("seed").Value.String()
			address1 := cmd.Flags().Lookup("address1").Value.String()
			address2 := cmd.Flags().Lookup("address2").Value.String()
			amount := cmd.Flags().Lookup("amount").Value.String()

			tx1, err1 := build.Transaction(
				build.Network{Passphrase: cli.Network.Passphrase},
				build.SourceAccount{AddressOrSeed: seed},
				build.AutoSequence{SequenceProvider: cli.HorizonClient1()},
				build.Payment(
					build.Destination{AddressOrSeed: address1},
					build.NativeAmount{Amount: amount},
				),
			)

			if err1 != nil {
				panic(err1)
			}

			tx2, err2 := build.Transaction(
				build.Network{Passphrase: cli.Network.Passphrase},
				build.SourceAccount{AddressOrSeed: seed},
				build.AutoSequence{SequenceProvider: cli.HorizonClient2()},
				build.Payment(
					build.Destination{AddressOrSeed: address2},
					build.NativeAmount{Amount: amount},
				),
			)

			if err2 != nil {
				panic(err2)
			}

			submit(cli.HorizonClient1(), tx1, seed)
			submit(cli.HorizonClient2(), tx2, seed)
		},
	}

	payments.Flags().String("seed", "", "")
	payments.Flags().String("address1", "", "")
	payments.Flags().String("address2", "", "")
	payments.Flags().String("amount", "", "")
	payments.MarkFlagRequired("seed")
	payments.MarkFlagRequired("address1")
	payments.MarkFlagRequired("address2")
	payments.MarkFlagRequired("amount")

	multipayment := &cobra.Command{
		Use:   "multipayment",
		Short: "multipayment",
		Long:  "",
		Run: func(cmd *cobra.Command, args []string) {
			seed1 := cmd.Flags().Lookup("seed1").Value.String()
			seed2 := cmd.Flags().Lookup("seed2").Value.String()
			seed3 := cmd.Flags().Lookup("seed3").Value.String()
			address1 := cmd.Flags().Lookup("address1").Value.String()
			address2 := cmd.Flags().Lookup("address2").Value.String()
			address3 := cmd.Flags().Lookup("address3").Value.String()
			amount := cmd.Flags().Lookup("amount").Value.String()

			tx1, err1 := build.Transaction(
				build.Network{Passphrase: cli.Network.Passphrase},
				build.SourceAccount{AddressOrSeed: seed1},
				build.AutoSequence{SequenceProvider: cli.HorizonClient1()},
				build.Payment(
					build.Destination{AddressOrSeed: address1},
					build.NativeAmount{Amount: amount},
				),
			)

			if err1 != nil {
				panic(err1)
			}

			tx2, err2 := build.Transaction(
				build.Network{Passphrase: cli.Network.Passphrase},
				build.SourceAccount{AddressOrSeed: seed2},
				build.AutoSequence{SequenceProvider: cli.HorizonClient2()},
				build.Payment(
					build.Destination{AddressOrSeed: address2},
					build.NativeAmount{Amount: amount},
				),
			)

			if err2 != nil {
				panic(err2)
			}

			tx3, err3 := build.Transaction(
				build.Network{Passphrase: cli.Network.Passphrase},
				build.SourceAccount{AddressOrSeed: seed3},
				build.AutoSequence{SequenceProvider: cli.HorizonClient3()},
				build.Payment(
					build.Destination{AddressOrSeed: address3},
					build.NativeAmount{Amount: amount},
				),
			)

			if err2 != nil {
				panic(err3)
			}

			submit(cli.HorizonClient1(), tx1, seed1)
			submit(cli.HorizonClient2(), tx2, seed2)
			submit(cli.HorizonClient3(), tx3, seed3)
		},
	}

	multipayment.Flags().String("seed1", "", "")
	multipayment.Flags().String("seed2", "", "")
	multipayment.Flags().String("seed3", "", "")
	multipayment.Flags().String("address1", "", "")
	multipayment.Flags().String("address2", "", "")
	multipayment.Flags().String("address3", "", "")
	multipayment.Flags().String("amount", "", "")
	multipayment.MarkFlagRequired("seed1")
	multipayment.MarkFlagRequired("seed2")
	multipayment.MarkFlagRequired("seed3")
	multipayment.MarkFlagRequired("address1")
	multipayment.MarkFlagRequired("address2")
	multipayment.MarkFlagRequired("address3")
	multipayment.MarkFlagRequired("amount")

	cmd.AddCommand(fund, payment, payments, multipayment)

	return cmd
}

func submit(client *horizon.Client, tx *build.TransactionBuilder, seed string) {
	if txe, err := tx.Sign(seed); err == nil {
		if blob, err := txe.Base64(); err == nil {
			if resp, err := client.SubmitTransaction(blob); err == nil {
				fmt.Println("transaction posted in ledger:", resp.Ledger)
			} else {
				panic(err)
			}
		} else {
			panic(err)
		}
	} else {
		panic(err)
	}
}
