from substrateinterface import Keypair
from dotenv import load_dotenv

import os

load_dotenv()


def get_keypair(seed_phrase: str) -> Keypair:
    return Keypair.create_from_mnemonic(seed_phrase)


def generate_derived_keypair(seed_phrase: str, derivation_path: str) -> Keypair:
    return Keypair.create_from_uri(seed_phrase + derivation_path)


def generate_derivation_accounts(seed_phrase: str, derivation_paths: list) -> list:
    return [generate_derived_keypair(seed_phrase, path) for path in derivation_paths]


def generate_sequence_accounts(seed_phrase: str, sequence: int) -> list:
    return [generate_derived_keypair(seed_phrase, f"//{i}") for i in range(sequence)]


if __name__ == "__main__":
    seed_phrase = os.getenv("TEAM_WALLET_SEED_PHRASE")
    sequence = 9

    keypair = get_keypair(seed_phrase)
    print("parent: ", keypair.ss58_address)

    sequence_accounts = generate_sequence_accounts(seed_phrase, sequence)
    for account in sequence_accounts:
        print(account.ss58_address)
