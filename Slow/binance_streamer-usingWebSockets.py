import asyncio
import websockets
import json
import time
import logging
from datetime import datetime
import sys
import signal

# Configure logging for performance monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

TICKER = "btcusdt"
URL = f"wss://stream.binance.com:9443/ws/{TICKER}@ticker"

# Performance tracking variables
message_count = 0
start_time = None
last_message_time = None

async def stream_price():
    global message_count, start_time, last_message_time
    
    connection_start = time.perf_counter()
    logger.info(f"🔄 Attempting to connect to Binance WebSocket for {TICKER.upper()}")
    
    try:
        # Optimized connection with faster ping/pong and smaller buffer
        async with websockets.connect(
            URL,
            ping_interval=20,  # Send ping every 20 seconds
            ping_timeout=10,   # Wait 10 seconds for pong
            max_size=2**16,    # 64KB buffer (smaller = faster)
            compression=None,  # Disable compression for speed
            close_timeout=5    # Faster connection close
        ) as ws:
            connection_time = time.perf_counter() - connection_start
            logger.info(f"📡 Connected in {connection_time:.3f}s to Binance WebSocket for {TICKER.upper()}")
            
            start_time = time.perf_counter()
            last_message_time = start_time
            
            while True:
                try:
                    # High precision timing for message processing
                    msg_start = time.perf_counter()
                    
                    # Receive message
                    msg = await ws.recv()
                    recv_time = time.perf_counter()
                    
                    # Parse JSON
                    data = json.loads(msg)
                    parse_time = time.perf_counter()

                    # Extract key info with minimal processing
                    ask = float(data['a'])  # best ask
                    bid = float(data['b'])  # best bid
                    last = float(data['c']) # last price
                    
                    # Calculate timing metrics
                    current_time = time.perf_counter()
                    message_count += 1
                    
                    recv_latency = (recv_time - msg_start) * 1000  # ms
                    parse_latency = (parse_time - recv_time) * 1000  # ms
                    total_latency = (current_time - msg_start) * 1000  # ms
                    
                    if last_message_time:
                        message_interval = (current_time - last_message_time) * 1000  # ms
                    else:
                        message_interval = 0
                    
                    last_message_time = current_time
                    
                    # Calculate messages per second
                    elapsed = current_time - start_time
                    msgs_per_sec = message_count / elapsed if elapsed > 0 else 0
                    
                    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Include milliseconds
                    
                    # Optimized output with performance metrics
                    print(f"[{timestamp}] Bid: {bid:>10.2f} | Ask: {ask:>10.2f} | Last: {last:>10.2f} | "
                          f"Recv: {recv_latency:.1f}ms | Parse: {parse_latency:.1f}ms | "
                          f"Total: {total_latency:.1f}ms | Interval: {message_interval:.1f}ms | "
                          f"Rate: {msgs_per_sec:.1f}/s | Msg#{message_count}")
                    
                    # Log performance stats every 100 messages
                    if message_count % 100 == 0:
                        avg_rate = message_count / elapsed
                        logger.info(f"📊 Performance: {message_count} messages in {elapsed:.1f}s "
                                  f"(avg: {avg_rate:.1f} msg/s)")

                except websockets.exceptions.ConnectionClosed:
                    logger.warning("🔌 WebSocket connection closed by server")
                    break
                except json.JSONDecodeError as e:
                    logger.error(f"❌ JSON decode error: {e}")
                    continue
                except Exception as e:
                    logger.error(f"⚠️ Unexpected error: {e}")
                    break
                    
    except Exception as e:
        logger.error(f"❌ Connection error: {e}")
        
def signal_handler(signum, frame):
    """Handle graceful shutdown"""
    global message_count, start_time
    if start_time and message_count > 0:
        elapsed = time.perf_counter() - start_time
        avg_rate = message_count / elapsed
        logger.info(f"📋 Final stats: {message_count} messages in {elapsed:.1f}s "
                   f"(avg: {avg_rate:.1f} msg/s)")
    logger.info("🛑 Shutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("🚀 Starting Binance WebSocket Streamer with Performance Monitoring")
    logger.info(f"📈 Ticker: {TICKER.upper()}")
    logger.info("Press Ctrl+C to stop and see final statistics")
    
    try:
        asyncio.run(stream_price())
    except KeyboardInterrupt:
        signal_handler(None, None)
