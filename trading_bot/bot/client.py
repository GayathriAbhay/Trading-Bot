"""Binance Futures API client wrapper."""
import hmac
import hashlib
import requests
import logging
import time
from urllib.parse import urlencode

logger = logging.getLogger("trading_bot")


class BinanceAPIError(Exception):
    """Binance API error."""
    pass


class BinanceFuturesClient:
    """
    Wrapper for Binance Futures Testnet API.
    Supports USDT-M futures trading.
    """
    
    BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self, api_key, api_secret, testnet=True):
        """
        Initialize Binance Futures client.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Whether to use testnet (default True)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": api_key})
        
        logger.debug(f"Initialized BinanceFuturesClient (testnet={testnet})")
    
    def _generate_signature(self, params):
        """
        Generate HMAC SHA256 signature for request.
        
        Args:
            params: Request parameters dictionary
        
        Returns:
            str: HMAC SHA256 signature
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _request(self, method, endpoint, params=None, is_signed=False):
        """
        Make HTTP request to Binance API.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint
            params: Request parameters
            is_signed: Whether request needs to be signed
        
        Returns:
            dict: API response
        
        Raises:
            BinanceAPIError: If API returns an error
        """
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        
        if is_signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        logger.debug(f"{method} {endpoint} - params: {params}")
        
        try:
            if method == "GET":
                response = self.session.get(url, params=params)
            elif method == "POST":
                response = self.session.post(url, params=params)
            elif method == "DELETE":
                response = self.session.delete(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            data = response.json()
            
            logger.debug(f"Response: {data}")
            
            # Check for Binance API errors
            if "code" in data and data["code"] != 200:
                error_msg = data.get("msg", "Unknown error")
                logger.error(f"Binance API Error: {error_msg}")
                raise BinanceAPIError(f"API Error {data['code']}: {error_msg}")
            
            return data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {e}")
            raise BinanceAPIError(f"Network error: {e}")
    
    def ping(self):
        """
        Test connectivity to the Binance API.
        
        Returns:
            dict: Empty response if successful
        """
        logger.info("Testing connectivity to Binance Futures API...")
        return self._request("GET", "/fapi/v1/ping")
    
    def get_account(self):
        """
        Get account information.
        
        Returns:
            dict: Account details including balance
        """
        logger.info("Fetching account information...")
        return self._request("GET", "/fapi/v2/account", is_signed=True)
    
    def get_symbol_info(self, symbol):
        """
        Get symbol/trading pair information.
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
        
        Returns:
            dict: Symbol exchange info
        """
        logger.info(f"Fetching symbol info for {symbol}...")
        exchange_info = self._request("GET", "/fapi/v1/exchangeInfo")
        
        for symbol_data in exchange_info.get("symbols", []):
            if symbol_data["symbol"] == symbol:
                return symbol_data
        
        raise BinanceAPIError(f"Symbol {symbol} not found")
    
    def place_order(self, symbol, side, order_type, quantity, price=None, 
                    stop_price=None, time_in_force="GTC"):
        """
        Place a futures order on Binance Testnet.
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET, LIMIT, STOP_LOSS, TAKE_PROFIT, etc.
            quantity: Order quantity
            price: Limit price (required for LIMIT orders)
            stop_price: Stop price (for stop orders)
            time_in_force: GTC, IOC, FOK (default GTC)
        
        Returns:
            dict: Order response with orderId, status, etc.
        
        Raises:
            BinanceAPIError: If order placement fails
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        
        if order_type in ["LIMIT", "STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"]:
            params["price"] = price
            params["timeInForce"] = time_in_force
        
        if order_type in ["STOP_LOSS", "STOP_LOSS_LIMIT", "TAKE_PROFIT", "TAKE_PROFIT_LIMIT"]:
            params["stopPrice"] = stop_price
        
        logger.info(f"Placing {order_type} {side} order: {symbol} x{quantity}")
        return self._request("POST", "/fapi/v1/order", params=params, is_signed=True)
    
    def cancel_order(self, symbol, order_id=None, orig_client_order_id=None):
        """
        Cancel an open order.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID (or use origClientOrderId)
            orig_client_order_id: Original client order ID
        
        Returns:
            dict: Cancellation response
        
        Raises:
            BinanceAPIError: If cancellation fails
        """
        params = {"symbol": symbol}
        
        if order_id:
            params["orderId"] = order_id
        elif orig_client_order_id:
            params["origClientOrderId"] = orig_client_order_id
        else:
            raise ValueError("Either orderId or origClientOrderId is required")
        
        logger.info(f"Canceling order for {symbol}")
        return self._request("DELETE", "/fapi/v1/order", params=params, is_signed=True)
    
    def get_order(self, symbol, order_id=None, orig_client_order_id=None):
        """
        Query an order.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            orig_client_order_id: Original client order ID
        
        Returns:
            dict: Order details
        
        Raises:
            BinanceAPIError: If query fails
        """
        params = {"symbol": symbol}
        
        if order_id:
            params["orderId"] = order_id
        elif orig_client_order_id:
            params["origClientOrderId"] = orig_client_order_id
        else:
            raise ValueError("Either orderId or origClientOrderId is required")
        
        logger.debug(f"Querying order for {symbol}")
        return self._request("GET", "/fapi/v1/order", params=params, is_signed=True)
