// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// 2022: B9FT103 Blockchain & Distributed Ledger Technologies CA 2
// Team B

contract checkFiles {
    
    string public hash;
    address public owner;
    string public lastModifyedBy;

    mapping(address => string) collaborators;

    constructor() {
        // set contract owner to adress who deployed contract
        owner = msg.sender;
        hash = "None";
        collaborators[msg.sender] = "ContractOwner";
    }

    //add a collaborator to the mapping 
    function addCollaborator(address _adress, string memory name) public onlyOwner {
        collaborators[ _adress] = name;
    }

    //delete a collaborator 
    function deleteCollaborator(address _adress) public onlyOwner {
        delete collaborators[_adress];
    }

    //###### Setters ######

    //set the file hash and update name of collaborator who changed it
    function setHash(string memory _hash) public onlyCollaborators {
        hash = _hash;
        lastModifyedBy = collaborators[msg.sender];
    }

    //set new contract owner 
    function setOwner(address _newOwner) public onlyOwner {
        // check if new adress is the zero-account
        require(_newOwner != address(0), "invalid adress");
        owner = _newOwner;
    }
    
    
    //###### Getters ######

    //return name of collaborator who did the last changes 
    function getLastModifyed() view public returns (string memory){
        return lastModifyedBy;
    }

    //return stored filehash 
    function getHash() view public returns (string memory) {
        return hash;
    }

    //###### Modifiers ######
    
    //modifyer to execute further code when address is a collaborator
    modifier onlyCollaborators(){
        require(bytes(collaborators[msg.sender]).length>0, "not a collaborator");
        //executes futher code 
        _;
    }
    //modifyer to execute further code when address is a contract owner 
    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }
}