#!/usr/bin/env python3
"""
Quick Ultra-Optimized Exchange Speed Test
Tests only the fastest, working methods from each exchange
"""

import asyncio
import time
import statistics
import json
import websockets
import aiohttp
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import orjson
    HAS_ORJSON = True
    logger.info("Using orjson (fastest)")
except ImportError:
    try:
        import ujson
        HAS_ORJSON = False
        HAS_UJSON = True
        logger.info("Using ujson (fast)")
    except ImportError:
        HAS_ORJSON = False
        HAS_UJSON = False
        logger.info("Using standard json")

class QuickSpeedTester:
    def __init__(self):
        # Set up fastest JSON parser
        if HAS_ORJSON:
            self.fast_json_loads = orjson.loads
            self.json_lib = "orjson"
        elif 'HAS_UJSON' in globals() and HAS_UJSON:
            import ujson
            self.fast_json_loads = ujson.loads
            self.json_lib = "ujson"
        else:
            self.fast_json_loads = json.loads
            self.json_lib = "json"
    
    async def test_binance_bookticker_optimized(self, duration=5):
        """Ultra-optimized Binance BookTicker"""
        logger.info(f"🚀 Testing Binance BookTicker (Ultra-Optimized) for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        try:
            async with websockets.connect(
                url,
                ping_interval=None,
                max_size=2**10,
                compression=None
            ) as ws:
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await ws.recv()
                        recv_time = time.perf_counter()
                        
                        # Fast parsing
                        data = self.fast_json_loads(msg)
                        if 'b' in data and 'a' in data:
                            bid = float(data['b'])
                            ask = float(data['a'])
                            latency = (recv_time - msg_start) * 1000
                            latencies.append(latency)
                            message_count += 1
                            
                            if message_count % 50 == 0:  # Log every 50 messages
                                print(f"📊 BTC/USDT: Bid={bid:.2f}, Ask={ask:.2f}, Latency={latency:.2f}ms")
                        
                    except Exception as e:
                        continue
                        
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return None
        
        if latencies:
            avg_latency = statistics.mean(latencies)
            msg_per_sec = message_count / duration
            logger.info(f"✅ Binance BookTicker: {msg_per_sec:.1f} msg/s, {avg_latency:.2f}ms avg latency")
            return {
                'exchange': 'Binance',
                'method': 'BookTicker Ultra',
                'msg_per_sec': msg_per_sec,
                'avg_latency': avg_latency,
                'total_messages': message_count
            }
        return None
    
    async def test_bybit_orderbook_optimized(self, duration=5):
        """Ultra-optimized Bybit OrderBook"""
        logger.info(f"🚀 Testing Bybit OrderBook (Ultra-Optimized) for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://stream.bybit.com/v5/public/spot"
        subscribe_msg = {"op": "subscribe", "args": ["orderbook.1.BTCUSDT"]}
        
        try:
            async with websockets.connect(url, ping_interval=None, max_size=2**11) as ws:
                # Subscribe
                await ws.send(json.dumps(subscribe_msg))
                
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                        recv_time = time.perf_counter()
                        
                        data = self.fast_json_loads(msg)
                        
                        # Check if it's a data message
                        if (isinstance(data, dict) and 
                            data.get('topic', '').startswith('orderbook') and 
                            'data' in data):
                            
                            book_data = data['data']
                            bids = book_data.get('b', [])
                            asks = book_data.get('a', [])
                            
                            if bids and asks:
                                bid = float(bids[0][0])
                                ask = float(asks[0][0])
                                latency = (recv_time - msg_start) * 1000
                                latencies.append(latency)
                                message_count += 1
                                
                                if message_count % 20 == 0:
                                    print(f"📊 BTC/USDT: Bid={bid:.2f}, Ask={ask:.2f}, Latency={latency:.2f}ms")
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return None
        
        if latencies:
            avg_latency = statistics.mean(latencies)
            msg_per_sec = message_count / duration
            logger.info(f"✅ Bybit OrderBook: {msg_per_sec:.1f} msg/s, {avg_latency:.2f}ms avg latency")
            return {
                'exchange': 'Bybit',
                'method': 'OrderBook Ultra',
                'msg_per_sec': msg_per_sec,
                'avg_latency': avg_latency,
                'total_messages': message_count
            }
        return None
    
    async def test_okx_books5_optimized(self, duration=5):
        """Ultra-optimized OKX Books5"""
        logger.info(f"🚀 Testing OKX Books5 (Ultra-Optimized) for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://ws.okx.com:8443/ws/v5/public"
        subscribe_msg = {"op": "subscribe", "args": [{"channel": "books5", "instId": "BTC-USDT"}]}
        
        try:
            async with websockets.connect(url, ping_interval=None, max_size=2**11) as ws:
                # Subscribe
                await ws.send(json.dumps(subscribe_msg))
                
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                        recv_time = time.perf_counter()
                        
                        data = self.fast_json_loads(msg)
                        
                        # Check for books5 data
                        if (isinstance(data, dict) and 
                            'data' in data and 
                            data.get('arg', {}).get('channel') == 'books5'):
                            
                            book_data = data['data'][0] if data['data'] else {}
                            bids = book_data.get('bids', [])
                            asks = book_data.get('asks', [])
                            
                            if bids and asks:
                                bid = float(bids[0][0])
                                ask = float(asks[0][0])
                                latency = (recv_time - msg_start) * 1000
                                latencies.append(latency)
                                message_count += 1
                                
                                if message_count % 10 == 0:
                                    print(f"📊 BTC-USDT: Bid={bid:.2f}, Ask={ask:.2f}, Latency={latency:.2f}ms")
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return None
        
        if latencies:
            avg_latency = statistics.mean(latencies)
            msg_per_sec = message_count / duration
            logger.info(f"✅ OKX Books5: {msg_per_sec:.1f} msg/s, {avg_latency:.2f}ms avg latency")
            return {
                'exchange': 'OKX',
                'method': 'Books5 Ultra',
                'msg_per_sec': msg_per_sec,
                'avg_latency': avg_latency,
                'total_messages': message_count
            }
        return None

async def main():
    """Run quick ultra-optimized tests"""
    tester = QuickSpeedTester()
    
    print("🚀 Quick Ultra-Optimized Exchange Speed Test")
    print("=" * 60)
    
    test_duration = 10  # 10 seconds per test
    results = []
    
    # Test the fastest working methods
    tests = [
        ("Binance BookTicker", tester.test_binance_bookticker_optimized),
        ("Bybit OrderBook", tester.test_bybit_orderbook_optimized),
        ("OKX Books5", tester.test_okx_books5_optimized),
    ]
    
    for test_name, test_func in tests:
        print(f"\n📊 Running {test_name}...")
        try:
            result = await test_func(test_duration)
            if result:
                results.append(result)
        except Exception as e:
            logger.error(f"Test {test_name} failed: {e}")
    
    # Print results
    print("\n" + "=" * 60)
    print("🏆 ULTRA-OPTIMIZED SPEED TEST RESULTS")
    print("=" * 60)
    
    if results:
        # Sort by messages per second
        results.sort(key=lambda x: x['msg_per_sec'], reverse=True)
        
        for i, result in enumerate(results, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📊"
            print(f"{emoji} {i}. {result['exchange']} {result['method']}")
            print(f"   📈 Speed: {result['msg_per_sec']:.1f} messages/second")
            print(f"   ⚡ Latency: {result['avg_latency']:.2f}ms average")
            print(f"   📊 Total: {result['total_messages']} messages")
            print()
        
        fastest = results[0]
        print(f"🏆 WINNER: {fastest['exchange']} {fastest['method']}")
        print(f"   {fastest['msg_per_sec']:.1f} msg/s with {fastest['avg_latency']:.2f}ms latency")
    else:
        print("❌ No successful tests")

if __name__ == "__main__":
    asyncio.run(main())
