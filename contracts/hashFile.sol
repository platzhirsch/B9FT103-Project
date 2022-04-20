contract checkFiles {
    
    string public hash;
    address public owner;
    string public lastModifyedBy;

    mapping(address => string) collaborators;

    constructor() public {
        owner = msg.sender;
        hash = "None";
        collaborators[msg.sender] = "ContractOwner";
    }

    function setHash(string memory _hash) public onlyCollaborators {
        hash = _hash;
        lastModifyedBy = collaborators[msg.sender];
    }

    function getHash() view public returns (string memory) {
        return hash;
    }

    function addCollaborator(address _adress, string memory name) public onlyOwner {
        collaborators[ _adress] = name;
    }

    modifier onlyCollaborators(){
        require(bytes(collaborators[msg.sender]).length>0);
        _;
    }
    function getLastModifyed() view public returns (string memory){
        return lastModifyedBy;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        //executes futher code 
        _;
    }

    function setOwner(address _newOwner) public onlyOwner {
        // check if new adress is the zero-account
        require(_newOwner != address(0), "invalid adress");
        owner = _newOwner;
    }

}