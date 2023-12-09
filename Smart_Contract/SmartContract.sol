// SPDX-License-Identifier: MIT

pragma solidity ^0.8.22;

contract Shop {
    address owner;

    // Единица товара
    struct Item {
        uint itemId;
        string title;
        uint price;
        uint availableCount;
    }

    uint id_items = 0;

    // Ассоциативный массив товаров
    mapping(uint => Item) public itemsMap;

    // События
    event itemAdded(string title, uint price, uint availableCount);
    event itemWasSold(string title, uint count, uint price, uint senderValue, uint change);

    constructor() {
        owner = msg.sender;
        initItems();
    }

    // Модификатор доступа для операций, доступных только владельцу магазина
    modifier onlyOwner() {
        require(msg.sender == owner, "You're not the owner");
        _;
    }

    // Функция добавления товаров в магазин
    function addItemToShop(string memory title, uint price, uint availableCount) public onlyOwner {
        require(bytes(title).length > 0, "Item must have a name");
        require(price >= 0, "Price must be non negative");
        require(availableCount > 0, "You can't add non positive number of items");

        Item memory newItem = Item(id_items, title, price, availableCount);
        itemsMap[id_items] = newItem;
        id_items++;

        emit itemAdded(title, price, availableCount);
    }

    // Начальный ассортимент магазина
    function initItems() internal onlyOwner {
        addItemToShop("Apple", 10**18, 5);
        addItemToShop("Bread", 2 * 10**18, 5);
        addItemToShop("Pelmeni", 3 * 10**18, 5);
    }

    // Функция получения каталога магазина
    function getItems() public view returns (Item[] memory) {
        Item[] memory items = new Item[](id_items);
        for (uint i = 0; i < id_items; i++) {
            items[i] = itemsMap[i];
        }
        return items;
    }

    // Функция получения баланса
    function balanceOf(address adr) public view returns (uint) {
        return adr.balance;
    }

    // Функция, позволяющая данному контракту получать эфир
    receive() external payable {}

    // Функция для произведения продажи товара клиенту
    function buyItem(uint itemId, uint countOfItems) public payable  {
        address payable senderAddress = payable(msg.sender);
        // address payable contractAddress = payable(address(this));

        require(itemId < id_items, "This item doesn't exist");
        require(countOfItems > 0, "You can't buy nothing");

        Item storage itemToSell = itemsMap[itemId];
        require(itemToSell.availableCount >= countOfItems, "Number of items in the shop less than you want to buy");
        require(balanceOf(senderAddress) >= itemToSell.price * countOfItems, "You don't have enough money on your balance");
        require(msg.value >= itemToSell.price * countOfItems, "There are not enough money to perform the operation");

        uint change = msg.value - itemToSell.price * countOfItems;
        // contractAddress.transfer(itemToSell.price * countOfItems);

        if (change > 0) {
            senderAddress.transfer(change);
        }
        
        itemToSell.availableCount -= countOfItems;

        emit itemWasSold(itemToSell.title, countOfItems, itemToSell.price * countOfItems, msg.value, change);
    }

    // Функция для снятия денег со счёта контракта
    function withdrawMoney(uint value, bool withdrawAll) public onlyOwner {
        address payable ownerAddress = payable(owner);

        if (withdrawAll) {
            ownerAddress.transfer(balanceOf(address(this)));
        } else {
            ownerAddress.transfer(value);
        }
    }
}