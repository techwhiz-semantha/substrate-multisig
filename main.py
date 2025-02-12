from substrateinterface import SubstrateInterface, Keypair
from dotenv import load_dotenv

import os

load_dotenv()

TEAM_WALLET_SEED_PHRASE = os.getenv("TEAM_WALLET_SEED_PHRASE")
NUMBER_OF_TEAM_WALLETS = os.getenv("NUMBER_OF_TEAM_WALLETS")
sequence = max(int(NUMBER_OF_TEAM_WALLETS) - 1, 0)


def get_team_wallets(seed_phrase: str, sequence: int) -> list:
    parent = Keypair.create_from_mnemonic(seed_phrase)

    sequence_accounts = [
        Keypair.create_from_uri(seed_phrase + f"//{i}") for i in range(sequence)
    ]
    return [parent] + sequence_accounts


if __name__ == "__main__":
    team_wallets = get_team_wallets(TEAM_WALLET_SEED_PHRASE, sequence)
    for wallet in team_wallets:
        print(wallet.ss58_address)
