from substrateinterface import Keypair, SubstrateInterface
from dotenv import load_dotenv

import os

load_dotenv()


chain_endpoint = os.getenv("CHAIN_ENDPOINT") or "wss://rpc.polkadot.io"
print(f"chain endpoint: {chain_endpoint}")
substrate = SubstrateInterface(url=os.getenv("CHAIN_ENDPOINT"))


def get_keypair(seed_phrase: str) -> Keypair:
    return Keypair.create_from_mnemonic(seed_phrase)


def generate_derived_keypair(seed_phrase: str, derivation_path: str) -> Keypair:
    return Keypair.create_from_uri(seed_phrase + derivation_path)


def generate_derivation_accounts(seed_phrase: str, derivation_paths: list) -> list:
    return [generate_derived_keypair(seed_phrase, path) for path in derivation_paths]


def generate_sequence_accounts(seed_phrase: str, sequence: int) -> list:
    return [generate_derived_keypair(seed_phrase, f"//{i}") for i in range(sequence)]


def generate_multisig_account(signatories: list, threshold: int) -> Keypair:
    return substrate.generate_multisig_account(signatories, threshold)


if __name__ == "__main__":
    seed_phrase = os.getenv("TEAM_WALLET_SEED_PHRASE")
    sequence = int(os.getenv("NUMBER_OF_TEAM_WALLETS"))
    sequence_accounts = generate_sequence_accounts(seed_phrase, sequence)
    for account in sequence_accounts:
        print(account.ss58_address)
