pragma solidity ^0.4.6;

contract Owned {
    modifier only_owner { if (msg.sender != owner) return _; }
    event NewOwner (address indexed old, address indexed current);

    function setOwner(address _new) only_owner {
        owner = _new; 
        emit NewOwner(owner, _new);
    }

    address public owner = msg.sender;
}
