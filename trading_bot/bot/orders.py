"""Order placement logic for the trading bot."""
import logging
from .client import BinanceFuturesClient, BinanceAPIError
from .validators import ValidationError, validate_order_params

logger = logging.getLogger("trading_bot")


class OrderManager:
    """Manages order placement and tracking."""
    
    def __init__(self, api_key, api_secret):
        """
        Initialize OrderManager.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
        """
        self.client = BinanceFuturesClient(api_key, api_secret, testnet=True)
        self.last_order = None
    
    def verify_connection(self):
        """
        Verify connection to Binance API.
        
        Returns:
            bool: True if connection successful
        
        Raises:
            BinanceAPIError: If connection fails
        """
        logger.info("Verifying connection to Binance Futures Testnet...")
        try:
            self.client.ping()
            logger.info("Connection verified successfully")
            return True
        except BinanceAPIError as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order.
        
        Args:
            symbol: Trading symbol
            side: BUY or SELL
            quantity: Order quantity
        
        Returns:
            dict: Order response
        
        Raises:
            ValidationError: If parameters are invalid
            BinanceAPIError: If order placement fails
        """
        # Validate parameters
        try:
            params = validate_order_params(symbol, side, "MARKET", quantity)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        # Place order
        try:
            order_response = self.client.place_order(
                symbol=params["symbol"],
                side=params["side"],
                order_type="MARKET",
                quantity=params["quantity"]
            )
            
            self.last_order = order_response
            logger.info(f"Market order placed successfully: {order_response}")
            return order_response
        
        except BinanceAPIError as e:
            logger.error(f"Failed to place market order: {e}")
            raise
    
    def place_limit_order(self, symbol, side, quantity, price):
        """
        Place a limit order.
        
        Args:
            symbol: Trading symbol
            side: BUY or SELL
            quantity: Order quantity
            price: Limit price
        
        Returns:
            dict: Order response
        
        Raises:
            ValidationError: If parameters are invalid
            BinanceAPIError: If order placement fails
        """
        # Validate parameters
        try:
            params = validate_order_params(symbol, side, "LIMIT", quantity, price)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        # Place order
        try:
            order_response = self.client.place_order(
                symbol=params["symbol"],
                side=params["side"],
                order_type="LIMIT",
                quantity=params["quantity"],
                price=params["price"],
                time_in_force="GTC"
            )
            
            self.last_order = order_response
            logger.info(f"Limit order placed successfully: {order_response}")
            return order_response
        
        except BinanceAPIError as e:
            logger.error(f"Failed to place limit order: {e}")
            raise
    
    def place_stop_loss_order(self, symbol, side, quantity, stop_price):
        """
        Place a stop-loss order.
        
        Args:
            symbol: Trading symbol
            side: BUY or SELL
            quantity: Order quantity
            stop_price: Stop trigger price
        
        Returns:
            dict: Order response
        
        Raises:
            ValidationError: If parameters are invalid
            BinanceAPIError: If order placement fails
        """
        try:
            params = validate_order_params(symbol, side, "STOP_LOSS", quantity, stop_price=stop_price)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        try:
            order_response = self.client.place_order(
                symbol=params["symbol"],
                side=params["side"],
                order_type="STOP_LOSS",
                quantity=params["quantity"],
                stop_price=params["stopPrice"]
            )
            
            self.last_order = order_response
            logger.info(f"Stop-loss order placed successfully: {order_response}")
            return order_response
        
        except BinanceAPIError as e:
            logger.error(f"Failed to place stop-loss order: {e}")
            raise
    
    def cancel_last_order(self, symbol):
        """
        Cancel the last placed order.
        
        Args:
            symbol: Trading symbol
        
        Returns:
            dict: Cancellation response
        
        Raises:
            BinanceAPIError: If cancellation fails
        """
        if not self.last_order:
            raise ValueError("No last order to cancel")
        
        order_id = self.last_order.get("orderId")
        if not order_id:
            raise ValueError("Order ID not found in last order")
        
        try:
            cancel_response = self.client.cancel_order(symbol, order_id=order_id)
            logger.info(f"Order cancelled successfully: {cancel_response}")
            return cancel_response
        
        except BinanceAPIError as e:
            logger.error(f"Failed to cancel order: {e}")
            raise
    
    def get_order_status(self, symbol, order_id):
        """
        Get the status of an order.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
        
        Returns:
            dict: Order details
        
        Raises:
            BinanceAPIError: If query fails
        """
        try:
            order = self.client.get_order(symbol, order_id=order_id)
            logger.info(f"Order status retrieved: {order}")
            return order
        
        except BinanceAPIError as e:
            logger.error(f"Failed to get order status: {e}")
            raise
