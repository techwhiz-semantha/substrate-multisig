from substrateinterface import SubstrateInterface, Keypair
from dotenv import load_dotenv

import os

from utils import generate_multisig_account

load_dotenv()

TEAM_WALLET_SEED_PHRASE = os.getenv("TEAM_WALLET_SEED_PHRASE")
NUMBER_OF_TEAM_WALLETS = os.getenv("NUMBER_OF_TEAM_WALLETS")
MULTISIG_THRESHOLD = os.getenv("MULTISIG_THRESHOLD")
sequence = max(int(NUMBER_OF_TEAM_WALLETS) - 1, 0)


def get_team_wallets(seed_phrase: str, sequence: int) -> list:
    parent = Keypair.create_from_mnemonic(seed_phrase)

    sequence_accounts = [
        Keypair.create_from_uri(seed_phrase + f"//{i}") for i in range(sequence)
    ]
    return [parent] + sequence_accounts


if __name__ == "__main__":
    # todo: generate team wallets
    team_wallets = get_team_wallets(TEAM_WALLET_SEED_PHRASE, sequence)
    print("team wallets:")
    for account in team_wallets:
        print(f"- {account.ss58_address}")

    # todo: create multisig account
    multisig_account = generate_multisig_account(
        [wallet.ss58_address for wallet in team_wallets],
        threshold=int(MULTISIG_THRESHOLD),
    )
    print(
        f"multisig account ({MULTISIG_THRESHOLD}/{NUMBER_OF_TEAM_WALLETS}): ",
        multisig_account.ss58_address,
    )

    # todo: trigger multisig extrinsic (from parent account)
    # todo: approve multisig extrinsic (from team wallets)
