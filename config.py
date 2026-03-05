"""
Project First Breath Configuration
Centralized configuration management with environment variable support
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

@dataclass
class ExchangeConfig:
    """Exchange API configuration"""
    name: str = "binance"
    api_key: Optional[str] = os.getenv("BINANCE_API_KEY")
    api_secret: Optional[str] = os.getenv("BINANCE_API_SECRET")
    testnet: bool = True  # Start with testnet for safety
    sandbox_mode: bool = True

@dataclass
class TradingConfig:
    """Trading parameters"""
    # Risk management
    max_position_size_usd: float = 10.0  # Start small
    stop_loss_pct: float = 1.0  # 1% stop loss
    take_profit_pct: float = 0.5  # 0.5% take profit
    
    # Profit allocation
    profit_to_stablecoin_ratio: float = 0.8  # 80% to stablecoin
    profit_to_principal_ratio: float = 0.2  # 20% to new principal
    
    # Target thresholds
    min_wallet_value_usd: float = 0.50
    max_ram_usage_pct: float = 85.0
    
    # Trading parameters
    timeframe: str = "1m"  # Lowest timeframe
    symbols: list = None
    
    def __post_init__(self):
        if self.symbols is None:
            self.symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

@dataclass
class FirebaseConfig:
    """Firebase configuration for state persistence"""
    project_id: Optional[str] = os.getenv("FIREBASE_PROJECT_ID")
    credentials_path: Optional[str] = os.getenv("FIREBASE_CREDENTIALS_PATH")
    collection_name: str = "first_breath_trades"

@dataclass
class MonitoringConfig:
    """Monitoring and logging configuration"""
    log_level: int = logging.INFO
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    telegram_bot_token: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")

class Config:
    """Main configuration class"""
    def __init__(self):
        self.exchange = ExchangeConfig()
        self.trading = TradingConfig()
        self.firebase = FirebaseConfig()
        self.monitoring = MonitoringConfig()
        
    def validate(self) -> bool:
        """Validate configuration"""
        missing_vars = []
        
        if not self.exchange.api_key:
            missing_vars.append("BINANCE_API_KEY")
        if not self.ex