import pandas as pd
import time
from web3 import Web3
from datetime import datetime

# Load CSV
df = pd.read_csv("healthcare_data.csv")

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
assert web3.is_connected(), "Ganache not connected"
web3.eth.default_account = web3.eth.accounts[0]  # Owner account

# Load Contract
contract_address = "0x77e1bC2CF79882a0f8CC1221381700f9d2984c0d"
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
	},
	{
		"inputs": [
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
	}
]

contract = web3.eth.contract(address=contract_address, abi=abi)

# Get total stored
total_records = contract.functions.getTotalRecords().call()
print(f"Total records: {total_records}")

# Fetch first 10 or less
max_records = min(10, total_records)

print("\nFirst 10 Health Records:\n")
for i in range(max_records):
    record = contract.functions.getRecord(i).call()

    readable_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    timestamp, patient_id, heart_rate, blood_pressure, oxygen_level, body_temp = record
    body_temp_c = body_temp / 10  # If you encoded it *10 before storing

    print(f"Record #{i}")
    print(f"Timestamp     : {readable_time}")
    print(f"Patient ID   : {patient_id}")
    print(f"Heart Rate   : {heart_rate} BPM")
    print(f"Blood Pressure: {blood_pressure}")
    print(f"Oxygen Level : {oxygen_level}%")
    print(f"Temperature  : {body_temp_c:.1f}°C\n")