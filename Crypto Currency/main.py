import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QLabel
import sys

coin_names = ["Bitcoin", "Ethereum", "Tether", "BNB", "Solana", "XRP", "USDC", "Cardano", "Avalanche", "Dogecoin", "Polkadot", "TRON", "Chainlink", "Polygon", "Toncoin", "Internet Computer", "Shiba Inu", "Dai", "Bitcoin Cash", "Litecoin", "Cosmos", "UNUS SED LEO", "Uniswap", "Injective", "NEAR Protocol", "Stellar", "Optimism", "OKB", "Ethereum Classic", "Lido DAO", "Stacks", "Filecoin", "Monero", "Hedera", "Aptos", "Kaspa", "Immutable", "Celestia", "Arbitrum", "Cronos", "VeChain", "TrueUSD", "Mantle", "First Digital USD", "THORChain", "The Graph", "Maker", "Sei", "Bitcoin SV", "Algorand", "ORDI", "Render", "SATS", "Flow", "Mina", "Fantom", "Theta Network", "Axie Infinity", "Synthetix", "The Sandbox", "BitTorrent (New)", "KuCoin Token", "BUSD", "Sui", "WEMIX", "Beam", "FTX Token", "Tezos", "Osmosis", "Decentraland", "Bitget Token", "Klaytn", "Neo", "Kava", "Helium", "EOS", "Oasis Network", "Astar", "IOTA", "PancakeSwap", "Gala", "USDD", "XDC Network", "Terra Classic", "WOO Network", "Akash Network", "Bonk", "Conflux", "eCash", "Frax Share", "Chiliz", "Rocket Pool", "Curve DAO Token", "Axelar", "Casper", "Blur", "Arweave", "1inch Network", "Flare", "Fetch.ai", "GMT", "Ronin", "ApeCoin", "Nexo", "Tether Gold", "GateToken", "Pepe", "Powerledger", "Gnosis", "GMX", "dYdX (ethDYDX)", "Core", "Trust Wallet Token", "Siacoin", "Terra", "Enjin Coin", "PAX Gold", "SKALE"]
working_coinname = ['Bitcoin', 'Ethereum', 'Tether', 'BNB', 'Solana', 'XRP', 'Cardano', 'Avalanche', 'Dogecoin', 'Polkadot', 'TRON', 'Chainlink', 'Polygon', 'Toncoin', 'Dai', 'Litecoin', 'Cosmos', 'Uniswap', 'Injective', 'Stellar', 'OKB', 'Stacks', 'Filecoin', 'Monero', 'Hedera', 'Aptos', 'Kaspa', 'Immutable', 'Celestia', 'Arbitrum', 'Cronos', 'VeChain', 'TrueUSD', 'Mantle', 'THORChain', 'Maker', 'Sei', 'Algorand', 'ORDI', 'Render', 'SATS', 'Flow', 'Mina', 'Fantom', 'Synthetix', 'Sui', 'WEMIX', 'Beam', 'Tezos', 'Osmosis', 'Decentraland', 'Klaytn', 'Neo', 'Kava', 'Helium', 'EOS', 'Astar', 'IOTA', 
'PancakeSwap', 'Gala', 'USDD', 'Bonk', 'eCash', 'Chiliz', 'Axelar', 'Casper', 'Blur', 'Arweave', 'Flare', 'Ronin', 'ApeCoin', 'Nexo', 'GateToken', 'Pepe', 'Gnosis', 'GMX', 'Core', 'Siacoin', 'Terra']

coins = []

#url = "https://coinmarketcap.com/currencies/tether/"
#response = requests.get(url)
#soup = BeautifulSoup(response.content, "html.parser")
#print(soup)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 150)
        self.setWindowTitle("CodersLegacy")
        combo = QComboBox(self)
        combo.addItems(working_coinname)
        combo.setStyleSheet("border :3px solid blue;")
        combo.move(20,20)
        button = QPushButton("Get Price", self)
        button.move(160, 20)
        # Connect the button click signal to click1 and pass the selected value
        button.clicked.connect(lambda: self.click1(combo.currentText()))
        self.label1 = QLabel(self)
        self.label1.setText('                                            ')
        self.label1.move(60, 60)
        self.label2 = QLabel(self)
        self.label2.setText('                                            ')
        self.label2.move(60, 100)
        
    def click1(self, selected_value):
        #self.label1.setText(f"Selected: {selected_value}")
        url = f"https://coinmarketcap.com/currencies/{selected_value}/" 
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        p = soup.find('span', class_='sc-f70bb44c-0 jxpCgO base-text')
        a = soup.find('div', class_='sc-aef7b723-0 sc-58c82cf9-0 hJFxIk')
        price = p.text
        volume = a.text
        self.label1.setText(f"{selected_value} Price: {price}")
        self.label2.setText(f"{selected_value} Volume: {volume}")
        
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
