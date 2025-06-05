// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IoTDataStorage {
    struct IoTData {
        uint256 timestamp;
        string deviceId;
        string dataType;
        string dataValue;
    }

    uint256 public constant MAX_ENTRIES = 100;
    IoTData[] public dataRecords;
    address public owner;

    event DataStored(
        uint256 timestamp,
        string deviceId,
        string dataType,
        string dataValue
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function storeData(
        uint256 _timestamp,
        string memory _deviceId,
        string memory _dataType,
        string memory _dataValue
    ) public onlyOwner {
        require(dataRecords.length < MAX_ENTRIES, "Storage limit reached");

        dataRecords.push(IoTData(_timestamp, _deviceId, _dataType, _dataValue));

        emit DataStored(_timestamp, _deviceId, _dataType, _dataValue);
    }

    function getTotalRecords() public view returns (uint256) {
        return dataRecords.length;
    }

    function getRecord(uint256 index) public view returns (
        uint256,
        string memory,
        string memory,
        string memory
    ) {
        require(index < dataRecords.length, "Index out of bounds");
        IoTData memory record = dataRecords[index];
        return (
            record.timestamp,
            record.deviceId,
            record.dataType,
            record.dataValue
        );
    }
}
