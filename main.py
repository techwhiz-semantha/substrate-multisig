from substrateinterface import Keypair
from dotenv import load_dotenv

import os

from utils import generate_multisig_account, get_substrate

load_dotenv()

TEAM_WALLET_SEED_PHRASE = os.getenv("TEAM_WALLET_SEED_PHRASE")
NUMBER_OF_TEAM_WALLETS = os.getenv("NUMBER_OF_TEAM_WALLETS")
MULTISIG_THRESHOLD = os.getenv("MULTISIG_THRESHOLD")
sequence = int(NUMBER_OF_TEAM_WALLETS)


def get_team_wallets(seed_phrase: str, sequence: int):
    withdrawal_account = Keypair.create_from_mnemonic(seed_phrase)

    sequence_accounts = [
        Keypair.create_from_uri(seed_phrase + f"//{i}") for i in range(sequence)
    ]
    return withdrawal_account, sequence_accounts


if __name__ == "__main__":
    # todo: generate team wallets
    withdrawal_wallet, team_wallets = get_team_wallets(
        TEAM_WALLET_SEED_PHRASE, sequence
    )
    print(f"Withdrawal Wallet: {withdrawal_wallet.ss58_address:<25}")
    print("Team Wallets:")
    for account in team_wallets:
        print(f"{'':<5}- {account.ss58_address}")

    # todo: create multisig account
    multisig_account = generate_multisig_account(
        [wallet.ss58_address for wallet in team_wallets],
        threshold=int(MULTISIG_THRESHOLD),
    )
    print(
        f"Multisig Account ({MULTISIG_THRESHOLD}/{NUMBER_OF_TEAM_WALLETS}): {multisig_account.ss58_address:<25}"
    )

    # todo: compose withdrawal call
    substrate = get_substrate()
    call = substrate.compose_call(
        call_module="Balances",
        call_function="transfer_all",
        call_params={"dest": withdrawal_wallet.ss58_address, "keep_alive": True},
    )
    print(f"{'Call:':<25} {call}")
    print(f"{'Call Data:':<25} {call.data}")

    # todo: trigger multisig extrinsic (from team_wallets[0])
    extrinsic = substrate.create_multisig_extrinsic(
        call, team_wallets[0], multisig_account, era={"period": 64}
    )
    print(f"{'Extrinsic:':<25} {extrinsic}")

    print("\n\n🙋 Submitting extrinsic...")
    receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    if not receipt.is_success:
        print(f"{'⚠️ Error:':<25} {receipt.error_message}")
        exit()
    else:
        # print(f"{'✅ Success:':<25} {receipt.triggered_events}")
        print("✅ Success")

    # todo: approve multisig extrinsic (from team wallets)
    for keypair in team_wallets[1 : int(MULTISIG_THRESHOLD)]:
        print(f"👌 Approving from {keypair.ss58_address}...")
        extrinsic = substrate.create_multisig_extrinsic(
            call, keypair, multisig_account, era={"period": 64}
        )
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        if receipt.is_success:
            print("✅ Success")
            # print(f"{'✅ Success:':<25} {receipt.triggered_events}")
        else:
            print(f"{'⚠️ Error:':<25} {receipt.error_message}")
