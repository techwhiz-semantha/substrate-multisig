# Project: Multisig Wallet Management

This project is designed to manage multisig wallets using the Substrate blockchain framework. It allows for the creation of team wallets, generation of a multisig account, and execution of transactions with multisig approval.

## Features

- **Team Wallet Generation**: Create multiple team wallets from a single seed phrase.
- **Multisig Account Creation**: Generate a deterministic multisig account with a specified threshold.
- **Transaction Execution**: Compose and submit transactions that require multisig approval.
- **Approval Process**: Approve transactions from multiple signatories to meet the multisig threshold.

## Prerequisites

- Python 3.7 or higher
- A Substrate-based blockchain node
- Access to the internet for connecting to the blockchain node

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/techwhiz-semantha/substrate-multisig.git
   cd substrate-multisig
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env.sample` to `.env` and fill in the required values:

     ```plaintext
     TEAM_WALLET_SEED_PHRASE=<your_private_key>
     NUMBER_OF_TEAM_WALLETS=10
     MULTISIG_THRESHOLD=3
     CHAIN_ENDPOINT=wss://rpc.dotters.network/paseo
     ```

## Usage

1. **Generate Team Wallets**:
   Run the main script to generate team wallets and a multisig account:

   ```bash
   python main.py
   ```

2. **Submit and Approve Transactions**:
   The script will automatically submit a transaction and prompt for approvals from the required number of signatories.

## Code Structure

- `main.py`: The main script to execute wallet generation and transaction submission.
- `utils.py`: Utility functions for keypair generation and substrate interface management.
- `.env.sample`: Sample environment configuration file.

## Important Notes

- Ensure that the `CHAIN_ENDPOINT` is correctly set to connect to your desired blockchain network.
- The seed phrase used should be kept secure and private.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
