import pandas as pd
from web3 import Web3
import time



df = pd.read_csv("healthcare_data.csv")

long_format_data = []
for _, row in df.iterrows():
    unix_ts = int(pd.to_datetime(row["timestamp"]).timestamp())
    pid = row["patient_id"]

    long_format_data.extend([
        {"timestamp": unix_ts, "patient_id": pid, "data_type": "heart_rate", "data_value": str(row["heart_rate"])},
        {"timestamp": unix_ts, "patient_id": pid, "data_type": "blood_pressure", "data_value": str(row["blood_pressure"])},
        {"timestamp": unix_ts, "patient_id": pid, "data_type": "oxygen_level", "data_value": str(row["oxygen_level"])},
        {"timestamp": unix_ts, "patient_id": pid, "data_type": "body_temp", "data_value": str(row["body_temp"])},
    ])

df_long = pd.DataFrame(long_format_data)

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("Connected to Ganache successfully!")
else:
    print("Connection failed. Ensure Ganache is running.")


contract_address = "0x6ddaa7081cF17C0C2c8D7F52cD12d53D8C73EC3f"

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
				"name": "deviceId",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "dataType",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "dataValue",
				"type": "string"
			}
		],
		"name": "DataStored",
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
				"name": "_deviceId",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_dataType",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_dataValue",
				"type": "string"
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
				"name": "",
				"type": "uint256"
			}
		],
		"name": "dataRecords",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "deviceId",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "dataType",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "dataValue",
				"type": "string"
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
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
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

web3.eth.default_account = web3.eth.accounts[0]



def send_iot_data(timestamp, patient_id, data_type, data_value):
    txn = contract.functions.storeData(timestamp, patient_id, data_type, data_value).transact({
        'from': web3.eth.default_account,
        'gas': 3000000
    })
    receipt = web3.eth.wait_for_transaction_receipt(txn)
    print(f"✅ Sent {data_type} = {data_value} for {patient_id} at {timestamp} | Txn: {receipt.transactionHash.hex()}")


for _, row in df_long.iterrows():
    send_iot_data(row["timestamp"], row["patient_id"], row["data_type"], row["data_value"])
    time.sleep(1)

