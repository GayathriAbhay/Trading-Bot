"""CLI interface for the trading bot."""
import os
import sys
import click
from dotenv import load_dotenv

from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.orders import OrderManager
from trading_bot.bot.validators import ValidationError
from trading_bot.bot.client import BinanceAPIError

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()


@click.group()
def cli():
    """Trading Bot CLI - Place orders on Binance Futures Testnet (USDT-M)"""
    pass


def get_api_credentials():
    """
    Get API credentials from environment variables.
    
    Returns:
        tuple: (api_key, api_secret)
    
    Raises:
        click.ClickException: If credentials are missing
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        raise click.ClickException(
            "BINANCE_API_KEY and BINANCE_API_SECRET environment variables not set. "
            "Please set them in .env file or as environment variables."
        )
    
    return api_key, api_secret


@cli.command()
def test():
    """Test connection to Binance Futures Testnet"""
    click.echo("Testing connection to Binance Futures Testnet...")
    
    try:
        api_key, api_secret = get_api_credentials()
        manager = OrderManager(api_key, api_secret)
        manager.verify_connection()
        click.echo(click.style("✓ Connection successful!", fg="green"))
    
    except click.ClickException as e:
        click.echo(click.style(f"✗ Error: {e.format_message()}", fg="red"))
        sys.exit(1)
    
    except (BinanceAPIError, Exception) as e:
        click.echo(click.style(f"✗ Error: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option("--symbol", prompt="Trading symbol (e.g., BTCUSDT)", 
              help="Symbol to trade")
@click.option("--side", type=click.Choice(["BUY", "SELL"]), 
              prompt="Order side (BUY/SELL)",
              help="BUY or SELL")
@click.option("--quantity", prompt="Quantity", 
              help="Order quantity")
def market(symbol, side, quantity):
    """Place a MARKET order"""
    click.echo("\n" + "="*60)
    click.echo("MARKET ORDER REQUEST")
    click.echo("="*60)
    
    try:
        api_key, api_secret = get_api_credentials()
        manager = OrderManager(api_key, api_secret)
        
        click.echo(f"\nSymbol:   {symbol}")
        click.echo(f"Side:     {side}")
        click.echo(f"Type:     MARKET")
        click.echo(f"Quantity: {quantity}")
        
        click.echo("\nPlacing market order...")
        
        response = manager.place_market_order(symbol, side, float(quantity))
        
        click.echo("\n" + "="*60)
        click.echo("ORDER RESPONSE")
        click.echo("="*60)
        click.echo(f"Order ID:      {response.get('orderId')}")
        click.echo(f"Symbol:        {response.get('symbol')}")
        click.echo(f"Side:          {response.get('side')}")
        click.echo(f"Type:          {response.get('type')}")
        click.echo(f"Status:        {response.get('status')}")
        click.echo(f"Quantity:      {response.get('origQty')}")
        click.echo(f"Executed Qty:  {response.get('executedQty')}")
        click.echo(f"Average Price: {response.get('avgPrice', 'N/A')}")
        click.echo(f"Time:          {response.get('time')}")
        
        click.echo("\n" + click.style("✓ Order placed successfully!", fg="green"))
        click.echo("="*60 + "\n")
    
    except ValidationError as e:
        click.echo(click.style(f"✗ Validation Error: {e}", fg="red"))
        sys.exit(1)
    
    except click.ClickException as e:
        click.echo(click.style(f"✗ Error: {e.format_message()}", fg="red"))
        sys.exit(1)
    
    except (BinanceAPIError, Exception) as e:
        click.echo(click.style(f"✗ Error: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option("--symbol", prompt="Trading symbol (e.g., BTCUSDT)", 
              help="Symbol to trade")
@click.option("--side", type=click.Choice(["BUY", "SELL"]), 
              prompt="Order side (BUY/SELL)",
              help="BUY or SELL")
@click.option("--quantity", prompt="Quantity", 
              help="Order quantity")
@click.option("--price", prompt="Limit price", 
              help="Limit price")
def limit(symbol, side, quantity, price):
    """Place a LIMIT order"""
    click.echo("\n" + "="*60)
    click.echo("LIMIT ORDER REQUEST")
    click.echo("="*60)
    
    try:
        api_key, api_secret = get_api_credentials()
        manager = OrderManager(api_key, api_secret)
        
        click.echo(f"\nSymbol:   {symbol}")
        click.echo(f"Side:     {side}")
        click.echo(f"Type:     LIMIT")
        click.echo(f"Quantity: {quantity}")
        click.echo(f"Price:    {price}")
        
        click.echo("\nPlacing limit order...")
        
        response = manager.place_limit_order(symbol, side, float(quantity), float(price))
        
        click.echo("\n" + "="*60)
        click.echo("ORDER RESPONSE")
        click.echo("="*60)
        click.echo(f"Order ID:      {response.get('orderId')}")
        click.echo(f"Symbol:        {response.get('symbol')}")
        click.echo(f"Side:          {response.get('side')}")
        click.echo(f"Type:          {response.get('type')}")
        click.echo(f"Status:        {response.get('status')}")
        click.echo(f"Quantity:      {response.get('origQty')}")
        click.echo(f"Price:         {response.get('price')}")
        click.echo(f"Executed Qty:  {response.get('executedQty')}")
        click.echo(f"Average Price: {response.get('avgPrice', 'N/A')}")
        click.echo(f"Time:          {response.get('time')}")
        
        click.echo("\n" + click.style("✓ Order placed successfully!", fg="green"))
        click.echo("="*60 + "\n")
    
    except ValidationError as e:
        click.echo(click.style(f"✗ Validation Error: {e}", fg="red"))
        sys.exit(1)
    
    except click.ClickException as e:
        click.echo(click.style(f"✗ Error: {e.format_message()}", fg="red"))
        sys.exit(1)
    
    except (BinanceAPIError, Exception) as e:
        click.echo(click.style(f"✗ Error: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option("--symbol", prompt="Trading symbol (e.g., BTCUSDT)", 
              help="Symbol to trade")
@click.option("--side", type=click.Choice(["BUY", "SELL"]), 
              prompt="Order side (BUY/SELL)",
              help="BUY or SELL")
@click.option("--quantity", prompt="Quantity", 
              help="Order quantity")
@click.option("--stop-price", prompt="Stop price", 
              help="Stop trigger price")
def stoploss(symbol, side, quantity, stop_price):
    """Place a STOP_LOSS order"""
    click.echo("\n" + "="*60)
    click.echo("STOP-LOSS ORDER REQUEST")
    click.echo("="*60)
    
    try:
        api_key, api_secret = get_api_credentials()
        manager = OrderManager(api_key, api_secret)
        
        click.echo(f"\nSymbol:     {symbol}")
        click.echo(f"Side:       {side}")
        click.echo(f"Type:       STOP_LOSS")
        click.echo(f"Quantity:   {quantity}")
        click.echo(f"Stop Price: {stop_price}")
        
        click.echo("\nPlacing stop-loss order...")
        
        response = manager.place_stop_loss_order(symbol, side, float(quantity), float(stop_price))
        
        click.echo("\n" + "="*60)
        click.echo("ORDER RESPONSE")
        click.echo("="*60)
        click.echo(f"Order ID:      {response.get('orderId')}")
        click.echo(f"Symbol:        {response.get('symbol')}")
        click.echo(f"Side:          {response.get('side')}")
        click.echo(f"Type:          {response.get('type')}")
        click.echo(f"Status:        {response.get('status')}")
        click.echo(f"Quantity:      {response.get('origQty')}")
        click.echo(f"Stop Price:    {response.get('stopPrice')}")
        click.echo(f"Time:          {response.get('time')}")
        
        click.echo("\n" + click.style("✓ Order placed successfully!", fg="green"))
        click.echo("="*60 + "\n")
    
    except ValidationError as e:
        click.echo(click.style(f"✗ Validation Error: {e}", fg="red"))
        sys.exit(1)
    
    except click.ClickException as e:
        click.echo(click.style(f"✗ Error: {e.format_message()}", fg="red"))
        sys.exit(1)
    
    except (BinanceAPIError, Exception) as e:
        click.echo(click.style(f"✗ Error: {e}", fg="red"))
        sys.exit(1)


if __name__ == "__main__":
    cli()
