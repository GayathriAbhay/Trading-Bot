"""Input validation for trading bot."""
import logging

logger = logging.getLogger("trading_bot")

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_symbol(symbol):
    """
    Validate trading symbol format.
    
    Args:
        symbol: Trading symbol (e.g., BTCUSDT)
    
    Raises:
        ValidationError: If symbol is invalid
    """
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    symbol = symbol.upper().strip()
    
    if len(symbol) < 6:
        raise ValidationError(f"Symbol '{symbol}' appears invalid (too short)")
    
    # Check if it contains only alphanumeric characters
    if not symbol.isalnum():
        raise ValidationError(f"Symbol '{symbol}' contains invalid characters")
    
    # Basic check: should end with USDT for USDT-M futures
    if not symbol.endswith(("USDT", "BUSD", "USDC")):
        logger.warning(f"Symbol '{symbol}' may not be a USDT-M futures pair")
    
    return symbol


def validate_side(side):
    """
    Validate order side.
    
    Args:
        side: Order side (BUY or SELL)
    
    Raises:
        ValidationError: If side is invalid
    """
    side = side.upper().strip()
    
    if side not in ["BUY", "SELL"]:
        raise ValidationError(f"Side must be BUY or SELL, got '{side}'")
    
    return side


def validate_order_type(order_type):
    """
    Validate order type.
    
    Args:
        order_type: Order type (MARKET, LIMIT, STOP_LOSS, TAKE_PROFIT, etc.)
    
    Raises:
        ValidationError: If order type is invalid
    """
    order_type = order_type.upper().strip()
    
    valid_types = ["MARKET", "LIMIT", "STOP_LOSS", "TAKE_PROFIT", "STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"]
    
    if order_type not in valid_types:
        raise ValidationError(f"Order type must be one of {valid_types}, got '{order_type}'")
    
    return order_type


def validate_quantity(quantity):
    """
    Validate order quantity.
    
    Args:
        quantity: Order quantity
    
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Quantity must be a valid number, got '{quantity}'")
    
    if qty <= 0:
        raise ValidationError(f"Quantity must be positive, got {qty}")
    
    return qty


def validate_price(price):
    """
    Validate order price.
    
    Args:
        price: Order price
    
    Raises:
        ValidationError: If price is invalid
    """
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValidationError(f"Price must be a valid number, got '{price}'")
    
    if p <= 0:
        raise ValidationError(f"Price must be positive, got {p}")
    
    return p


def validate_stop_price(stop_price):
    """
    Validate stop price for stop-loss orders.
    
    Args:
        stop_price: Stop price
    
    Raises:
        ValidationError: If stop price is invalid
    """
    try:
        p = float(stop_price)
    except (ValueError, TypeError):
        raise ValidationError(f"Stop price must be a valid number, got '{stop_price}'")
    
    if p <= 0:
        raise ValidationError(f"Stop price must be positive, got {p}")
    
    return p


def validate_order_params(symbol, side, order_type, quantity, price=None, stop_price=None):
    """
    Validate all order parameters together.
    
    Args:
        symbol: Trading symbol
        side: Order side (BUY/SELL)
        order_type: Order type (MARKET/LIMIT/etc)
        quantity: Order quantity
        price: Order price (required for LIMIT orders)
        stop_price: Stop price (for stop-loss orders)
    
    Returns:
        dict: Validated parameters
    
    Raises:
        ValidationError: If any parameter is invalid
    """
    validated = {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
    }
    
    # Price validation depends on order type
    if order_type.upper() in ["LIMIT", "STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"]:
        if price is None:
            raise ValidationError(f"Price is required for {order_type} orders")
        validated["price"] = validate_price(price)
    
    # Stop price validation for stop orders
    if order_type.upper() in ["STOP_LOSS", "STOP_LOSS_LIMIT", "TAKE_PROFIT", "TAKE_PROFIT_LIMIT"]:
        if stop_price is None:
            raise ValidationError(f"Stop price is required for {order_type} orders")
        validated["stopPrice"] = validate_stop_price(stop_price)
    
    return validated
