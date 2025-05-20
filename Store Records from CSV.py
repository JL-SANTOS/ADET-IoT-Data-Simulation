import pandas as pd
import datetime
from web3 import Web3

# Load CSV
df = pd.read_csv("healthcare_data.csv")

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
assert web3.is_connected(), "Ganache not connected"
web3.eth.default_account = web3.eth.accounts[0]  # Owner account

# Load Contract
contract_address = "0x77e1bC2CF79882a0f8CC1221381700f9d2984c0d"  # Replace this
abi = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "patientId",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "heartRate",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "bloodPressure",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "oxygenLevel",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "bodyTemp",
				"type": "uint256"
			}
		],
		"name": "HealthDataStored",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_timestamp",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_patientId",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_heartRate",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_bloodPressure",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_oxygenLevel",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_bodyTemp",
				"type": "uint256"
			}
		],
		"name": "storeData",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getRecord",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTotalRecords",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "healthRecords",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "patientId",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "heartRate",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "bloodPressure",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "oxygenLevel",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "bodyTemp",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "MAX_ENTRIES",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

contract = web3.eth.contract(address=contract_address, abi=abi)

# Function to convert float temp to int (36.5°C -> 365)
def encode_temp(temp):
    return int(float(temp) * 10)

# Convert timestamp string to UNIX integer (if it's in datetime format)
def parse_csv_timestamp(ts):
    return int(pd.to_datetime(ts).timestamp())

# Updated function to send data
def store_health_data(row):
    timestamp = parse_csv_timestamp(row["timestamp"])
    
    txn = contract.functions.storeData(
        timestamp,
        str(row["patient_id"]),
        int(row["heart_rate"]),
        str(row["blood_pressure"]),
        int(row["oxygen_level"]),
        encode_temp(row["body_temp"])
    ).transact({'from': web3.eth.default_account})
    
    receipt = web3.eth.wait_for_transaction_receipt(txn)
    print(f"Stored {row['patient_id']} @ {timestamp} | Tx: {receipt.transactionHash.hex()}")


# Loop through CSV rows and send data
for _, row in df.iterrows():
    store_health_data(row)
    time.sleep(1)  # optional, avoid flooding
