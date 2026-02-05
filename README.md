# Trading Bot - Binance Futures Testnet

A Python application for placing orders on Binance Futures Testnet (USDT-M). This bot provides a clean CLI interface with proper logging, validation, and error handling.

## Features

- **Market Orders**: Place market orders with immediate execution
- **Limit Orders**: Place limit orders with specified price levels
- **Stop-Loss Orders**: Implement risk management with stop-loss orders
- **Comprehensive Logging**: All API requests and responses logged to file
- **Input Validation**: Robust validation of all user inputs
- **Error Handling**: Graceful handling of API errors and network failures
- **Clean Architecture**: Separated concerns (client, orders, validators, logging)

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance Futures API client wrapper
│   ├── orders.py          # Order placement logic and OrderManager
│   ├── validators.py      # Input validation functions
│   └── logging_config.py  # Logging configuration
├── cli.py                 # CLI entry point with Click commands
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Prerequisites

- Python 3.8+
- A Binance Futures Testnet account
- API credentials (API Key and Secret) from testnet

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd trading_bot
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Credentials

Create a `.env` file in the project root:

```bash
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**Important**: 
- Use your **Binance Futures Testnet** API credentials
- Sign up at: https://testnet.binancefuture.com
- Never commit the `.env` file to version control

### 5. Test Connection

```bash
python -m trading_bot.cli test
```

You should see: `✓ Connection successful!`

## Usage

### Available Commands

#### 1. Test Connection
```bash
python -m trading_bot.cli test
```
Verifies your API credentials and connection to testnet.

#### 2. Place Market Order
```bash
python -m trading_bot.cli market
```
Interactive prompts for:
- Symbol (e.g., BTCUSDT)
- Side (BUY/SELL)
- Quantity

Example:
```bash
python -m trading_bot.cli market --symbol BTCUSDT --side BUY --quantity 0.1
```

#### 3. Place Limit Order
```bash
python -m trading_bot.cli limit
```
Interactive prompts for:
- Symbol
- Side
- Quantity
- Limit Price

Example:
```bash
python -m trading_bot.cli limit --symbol ETHUSDT --side SELL --quantity 1.0 --price 2500
```

#### 4. Place Stop-Loss Order
```bash
python -m trading_bot.cli stoploss
```
Interactive prompts for:
- Symbol
- Side
- Quantity
- Stop Price

Example:
```bash
python -m trading_bot.cli stoploss --symbol BTCUSDT --side SELL --quantity 0.05 --stop-price 35000
```

## Examples

### Example 1: Market Order

```bash
$ python -m trading_bot.cli market
Trading symbol (e.g., BTCUSDT): BTCUSDT
Order side (BUY/SELL): BUY
Quantity: 0.1

============================================================
MARKET ORDER REQUEST
============================================================

Symbol:   BTCUSDT
Side:     BUY
Type:     MARKET
Quantity: 0.1

Placing market order...

============================================================
ORDER RESPONSE
============================================================
Order ID:      1234567890
Symbol:        BTCUSDT
Side:          BUY
Type:          MARKET
Status:        FILLED
Quantity:      0.1
Executed Qty:  0.1
Average Price: 43250.50
Time:          1643650800000

✓ Order placed successfully!
============================================================
```

### Example 2: Limit Order

```bash
$ python -m trading_bot.cli limit
Trading symbol (e.g., BTCUSDT): ETHUSDT
Order side (BUY/SELL): BUY
Quantity: 1.0
Limit price: 2400

============================================================
LIMIT ORDER REQUEST
============================================================

Symbol:   ETHUSDT
Side:     BUY
Type:     LIMIT
Quantity: 1.0
Price:    2400

Placing limit order...

============================================================
ORDER RESPONSE
============================================================
Order ID:      1234567891
Symbol:        ETHUSDT
Side:          BUY
Type:          LIMIT
Status:        NEW
Quantity:      1.0
Price:         2400
Executed Qty:  0
Average Price: N/A
Time:          1643650900000

✓ Order placed successfully!
============================================================
```

## Log Files

All activities are logged to `logs/` directory with timestamps:

```
logs/
└── trading_bot_20240205_143022.log
```

### Sample Log Output

```
2024-02-05 14:30:22 - trading_bot - INFO - Logging initialized. Log file: logs/trading_bot_20240205_143022.log
2024-02-05 14:30:23 - trading_bot - INFO - Initialized BinanceFuturesClient (testnet=True)
2024-02-05 14:30:23 - trading_bot - DEBUG - GET /fapi/v1/ping - params: {'timestamp': 1707138623000, 'signature': 'abc123...'}
2024-02-05 14:30:24 - trading_bot - DEBUG - Response: {}
2024-02-05 14:30:24 - trading_bot - INFO - Connection verified successfully
2024-02-05 14:30:25 - trading_bot - INFO - Placing MARKET BUY order: BTCUSDT x0.1
2024-02-05 14:30:25 - trading_bot - DEBUG - POST /fapi/v1/order - params: {...}
2024-02-05 14:30:26 - trading_bot - DEBUG - Response: {'orderId': 1234567890, ...}
2024-02-05 14:30:26 - trading_bot - INFO - Market order placed successfully: {...}
```

## Validation & Error Handling

### Input Validation

The bot validates:
- **Symbol**: Must be alphanumeric, typically ends with USDT/BUSD/USDC
- **Side**: Must be BUY or SELL
- **Order Type**: Must be MARKET, LIMIT, STOP_LOSS, etc.
- **Quantity**: Must be a positive number
- **Price**: Must be a positive number (required for LIMIT orders)
- **Stop Price**: Must be a positive number (required for STOP_LOSS orders)

### Error Handling

- **Validation Errors**: Clear messages on invalid inputs
- **API Errors**: Graceful handling with error codes and messages
- **Network Errors**: Connection timeout and retry logic through logs
- **Missing Credentials**: Helpful error messages with setup instructions

Example:
```bash
$ python -m trading_bot.cli limit --symbol BTCUSDT --side BUY --quantity -1 --price 40000
✗ Validation Error: Quantity must be positive, got -1
```

## Code Architecture

### `client.py`
- `BinanceFuturesClient`: Main API wrapper
- `_generate_signature()`: HMAC SHA256 signing for authenticated endpoints
- `_request()`: Generic HTTP request handler with error management
- Methods: `ping()`, `get_account()`, `place_order()`, `cancel_order()`, `get_order()`

### `orders.py`
- `OrderManager`: High-level order management
- Methods: `place_market_order()`, `place_limit_order()`, `place_stop_loss_order()`
- Integrates validation and logging

### `validators.py`
- Input validation functions
- `ValidationError` exception class
- Validators: `validate_symbol()`, `validate_side()`, `validate_order_type()`, etc.

### `logging_config.py`
- `setup_logging()`: Configure file and console logging
- Creates timestamped log files
- DEBUG level for files, INFO level for console

### `cli.py`
- Click-based CLI interface
- Commands: `test`, `market`, `limit`, `stoploss`
- Credential management from environment variables

## API Reference

### Binance Futures Testnet

Base URL: `https://testnet.binancefuture.com`

**Key Endpoints Used:**
- `GET /fapi/v1/ping` - Test connectivity
- `GET /fapi/v2/account` - Get account information
- `POST /fapi/v1/order` - Place order
- `DELETE /fapi/v1/order` - Cancel order
- `GET /fapi/v1/order` - Query order

All requests require API Key header and HMAC SHA256 signature for authenticated endpoints.

## Assumptions & Limitations

1. **Testnet Only**: This bot is configured for Binance Futures Testnet. For production, change `BASE_URL` in `client.py`
2. **USDT-M Futures**: Configured for USDT-Margined Futures
3. **Default Time in Force**: LIMIT orders use GTC (Good Till Cancel)
4. **No Position Management**: This bot doesn't track open positions across sessions
5. **No Advanced Features**: No grid trading, DCA, or algorithmic strategies
6. **Single Order Tracking**: Only tracks the last placed order in memory

## Troubleshooting

### Issue: "BINANCE_API_KEY and BINANCE_API_SECRET not set"

**Solution**: Ensure your `.env` file is in the project root:
```bash
echo "BINANCE_API_KEY=your_key" > .env
echo "BINANCE_API_SECRET=your_secret" >> .env
```

### Issue: Connection fails with "Invalid API key"

**Solution**: 
- Verify you're using Testnet credentials
- Check credentials in `.env` are correct
- Ensure API key has trading permissions enabled

### Issue: Order validation fails

**Solution**: Check the error message:
- Symbol must be valid (e.g., BTCUSDT, not BTC)
- Quantity must be positive and within trading limits
- Price must be positive (for LIMIT orders)

### Issue: "Symbol not found"

**Solution**: Verify the symbol is available on Binance Futures:
- Check: https://testnet.binancefuture.com (after login)
- Use correct format: TOKENUSDT

## Requirements

```
python-binance==1.0.19
requests==2.31.0
click==8.1.7
python-dotenv==1.0.0
```

## License

MIT License

## Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Review the Error Handling section above
3. Verify API credentials and testnet access

## Author

Gayathri A Menon

---

**Last Updated**: February 2024
**Status**: Production Ready for Testnet
