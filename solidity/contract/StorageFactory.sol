//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

import "./SimpleStorage.sol";

contract StorageFactory is SimpleStorage {
    SimpleStorage[] public SimpleStorageArray;

    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        SimpleStorageArray.push(simpleStorage);
    }

    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber)
        public
    {
        SimpleStorage(address(SimpleStorageArray[_simpleStorageIndex])).store(
            _simpleStorageNumber
        );
    }

    function sfGet(uint256 _simpleStorageIndex) public view returns (uint256) {
        return
            SimpleStorage(address(SimpleStorageArray[_simpleStorageIndex]))
                .retrieve();
    }
}
