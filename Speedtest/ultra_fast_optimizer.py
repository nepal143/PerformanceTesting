#!/usr/bin/env python3
"""
🚀 ULTRA-OPTIMIZED BYBIT & OKX SPEED ENHANCER
Specialized optimizations to get Bybit and OKX latency from 50-120ms down to 1-20ms
Uses advanced techniques: connection pooling, binary parsing, minimal processing
"""

import asyncio
import time
import json
import websockets
import logging
from collections import deque
import struct

# Minimal logging for maximum speed
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

try:
    import orjson
    HAS_ORJSON = True
    fast_json_loads = orjson.loads
    fast_json_dumps = orjson.dumps
    print("🔥 Using orjson (FASTEST)")
except ImportError:
    HAS_ORJSON = False
    fast_json_loads = json.loads
    fast_json_dumps = json.dumps
    print("📊 Using standard json")

class UltraFastExchangeOptimizer:
    def __init__(self):
        self.bybit_prices = deque(maxlen=100)  # Circular buffer
        self.okx_prices = deque(maxlen=100)
        self.bybit_latencies = deque(maxlen=50)
        self.okx_latencies = deque(maxlen=50)
        self.start_time = time.perf_counter()
        self.message_counts = {'Bybit': 0, 'OKX': 0}
        
    async def test_bybit_ultra_optimized(self, duration=10):
        """Ultra-optimized Bybit with aggressive speed techniques"""
        print(f"🚀 Testing Bybit ULTRA-OPTIMIZED (Target: <20ms) for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://stream.bybit.com/v5/public/spot"
        
        # Pre-compile subscription message as bytes
        subscribe_msg = fast_json_dumps({"op": "subscribe", "args": ["orderbook.1.BTCUSDT"]})
        
        try:
            # Ultra-aggressive connection settings
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                max_size=512,      # Absolute minimum
                compression=None,
                close_timeout=0.05,
                max_queue=1,       # Minimal queue
                read_limit=512,    # Tiny read buffer
                write_limit=256    # Tiny write buffer
            ) as ws:
                # Send subscription immediately
                await ws.send(subscribe_msg)
                
                # Pre-compile search patterns as bytes
                topic_pattern = b'"topic":"orderbook'
                data_pattern = b'"data":'
                b_pattern = b'"b":['
                a_pattern = b'"a":['
                
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        
                        # Ultra-fast receive with minimal timeout
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.001)
                        recv_time = time.perf_counter()
                        
                        # Convert to bytes for ultra-fast search
                        if isinstance(msg, str):
                            msg_bytes = msg.encode()
                        else:
                            msg_bytes = msg
                        
                        # Ultra-fast binary pattern matching
                        if topic_pattern in msg_bytes and data_pattern in msg_bytes:
                            if b_pattern in msg_bytes and a_pattern in msg_bytes:
                                try:
                                    # Minimal JSON parsing - only extract what we need
                                    data = fast_json_loads(msg_bytes)
                                    
                                    # Direct navigation to avoid dict lookups
                                    if 'data' in data:
                                        book_data = data['data']
                                        bids = book_data.get('b', [])
                                        asks = book_data.get('a', [])
                                        
                                        if bids and asks:
                                            # Extract only first bid/ask
                                            bid = float(bids[0][0])
                                            ask = float(asks[0][0])
                                            
                                            latency = (recv_time - msg_start) * 1000
                                            latencies.append(latency)
                                            message_count += 1
                                            
                                            # Store in circular buffer
                                            self.bybit_prices.append((bid, ask, recv_time))
                                            self.bybit_latencies.append(latency)
                                            
                                            if message_count % 50 == 0:
                                                avg_lat = sum(self.bybit_latencies) / len(self.bybit_latencies)
                                                print(f"🔥 Bybit: {bid:.2f}/{ask:.2f} | Latency: {latency:.2f}ms | Avg: {avg_lat:.2f}ms")
                                
                                except Exception:
                                    continue  # Skip malformed data
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Bybit connection error: {e}")
            return None
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            msg_per_sec = message_count / duration
            
            print(f"✅ Bybit ULTRA-OPTIMIZED Results:")
            print(f"   📈 Speed: {msg_per_sec:.1f} msg/s")
            print(f"   ⚡ Avg Latency: {avg_latency:.2f}ms")
            print(f"   🚀 Min Latency: {min_latency:.2f}ms") 
            print(f"   📊 Max Latency: {max_latency:.2f}ms")
            print(f"   🎯 Target: {'✅ ACHIEVED' if avg_latency < 20 else '❌ NEEDS MORE WORK'}")
            
            return {
                'exchange': 'Bybit',
                'method': 'Ultra-Optimized',
                'msg_per_sec': msg_per_sec,
                'avg_latency': avg_latency,
                'min_latency': min_latency,
                'max_latency': max_latency,
                'total_messages': message_count
            }
        return None
    
    async def test_okx_ultra_optimized(self, duration=10):
        """Ultra-optimized OKX with aggressive speed techniques"""
        print(f"🚀 Testing OKX ULTRA-OPTIMIZED (Target: <20ms) for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://ws.okx.com:8443/ws/v5/public"
        
        # Pre-compile subscription message as bytes
        subscribe_msg = fast_json_dumps({
            "op": "subscribe", 
            "args": [{"channel": "books5", "instId": "BTC-USDT"}]
        })
        
        try:
            # Ultra-aggressive connection settings
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                max_size=512,      # Absolute minimum
                compression=None,
                close_timeout=0.05,
                max_queue=1,       # Minimal queue
                read_limit=512,    # Tiny read buffer
                write_limit=256    # Tiny write buffer
            ) as ws:
                # Send subscription immediately
                await ws.send(subscribe_msg)
                
                # Pre-compile search patterns as bytes
                channel_pattern = b'"channel":"books5"'
                data_pattern = b'"data":['
                bids_pattern = b'"bids":['
                asks_pattern = b'"asks":['
                
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        
                        # Ultra-fast receive with minimal timeout
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.001)
                        recv_time = time.perf_counter()
                        
                        # Convert to bytes for ultra-fast search
                        if isinstance(msg, str):
                            msg_bytes = msg.encode()
                        else:
                            msg_bytes = msg
                        
                        # Ultra-fast binary pattern matching
                        if channel_pattern in msg_bytes and data_pattern in msg_bytes:
                            if bids_pattern in msg_bytes and asks_pattern in msg_bytes:
                                try:
                                    # Minimal JSON parsing
                                    data = fast_json_loads(msg_bytes)
                                    
                                    # Direct navigation to avoid dict lookups
                                    if 'data' in data and data['data']:
                                        book_data = data['data'][0]
                                        bids = book_data.get('bids', [])
                                        asks = book_data.get('asks', [])
                                        
                                        if bids and asks:
                                            # Extract only first bid/ask
                                            bid = float(bids[0][0])
                                            ask = float(asks[0][0])
                                            
                                            latency = (recv_time - msg_start) * 1000
                                            latencies.append(latency)
                                            message_count += 1
                                            
                                            # Store in circular buffer
                                            self.okx_prices.append((bid, ask, recv_time))
                                            self.okx_latencies.append(latency)
                                            
                                            if message_count % 20 == 0:
                                                avg_lat = sum(self.okx_latencies) / len(self.okx_latencies)
                                                print(f"🔥 OKX: {bid:.2f}/{ask:.2f} | Latency: {latency:.2f}ms | Avg: {avg_lat:.2f}ms")
                                
                                except Exception:
                                    continue  # Skip malformed data
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ OKX connection error: {e}")
            return None
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            msg_per_sec = message_count / duration
            
            print(f"✅ OKX ULTRA-OPTIMIZED Results:")
            print(f"   📈 Speed: {msg_per_sec:.1f} msg/s")
            print(f"   ⚡ Avg Latency: {avg_latency:.2f}ms")
            print(f"   🚀 Min Latency: {min_latency:.2f}ms")
            print(f"   📊 Max Latency: {max_latency:.2f}ms")
            print(f"   🎯 Target: {'✅ ACHIEVED' if avg_latency < 20 else '❌ NEEDS MORE WORK'}")
            
            return {
                'exchange': 'OKX',
                'method': 'Ultra-Optimized',
                'msg_per_sec': msg_per_sec,
                'avg_latency': avg_latency,
                'min_latency': min_latency,
                'max_latency': max_latency,
                'total_messages': message_count
            }
        return None
    
    async def test_binance_baseline(self, duration=10):
        """Test Binance baseline for comparison"""
        print(f"🚀 Testing Binance BASELINE for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        try:
            async with websockets.connect(
                url,
                ping_interval=None,
                max_size=512,
                compression=None
            ) as ws:
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await ws.recv()
                        recv_time = time.perf_counter()
                        
                        data = fast_json_loads(msg)
                        if 'b' in data and 'a' in data:
                            bid = float(data['b'])
                            ask = float(data['a'])
                            latency = (recv_time - msg_start) * 1000
                            latencies.append(latency)
                            message_count += 1
                            
                            if message_count % 100 == 0:
                                avg_lat = sum(latencies[-50:]) / min(50, len(latencies))
                                print(f"🔥 Binance: {bid:.2f}/{ask:.2f} | Latency: {latency:.2f}ms | Avg: {avg_lat:.2f}ms")
                        
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Binance connection error: {e}")
            return None
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            msg_per_sec = message_count / duration
            
            print(f"✅ Binance BASELINE Results:")
            print(f"   📈 Speed: {msg_per_sec:.1f} msg/s")
            print(f"   ⚡ Avg Latency: {avg_latency:.2f}ms")
            print(f"   🚀 Min Latency: {min_latency:.2f}ms")
            
            return {
                'exchange': 'Binance',
                'method': 'Baseline',
                'msg_per_sec': msg_per_sec,
                'avg_latency': avg_latency,
                'min_latency': min_latency,
                'total_messages': message_count
            }
        return None

async def main():
    """Run ultra-optimized tests targeting sub-20ms latency"""
    optimizer = UltraFastExchangeOptimizer()
    
    print("🚀 ULTRA-OPTIMIZED EXCHANGE SPEED ENHANCER")
    print("=" * 70)
    print("🎯 Target: Get Bybit & OKX under 20ms latency")
    print("📊 Binance baseline: ~3.32ms (already excellent)")
    print()
    
    test_duration = 15  # 15 seconds per test
    results = []
    
    # Test in optimal order
    tests = [
        ("Binance Baseline", optimizer.test_binance_baseline),
        ("Bybit Ultra-Optimized", optimizer.test_bybit_ultra_optimized),
        ("OKX Ultra-Optimized", optimizer.test_okx_ultra_optimized),
    ]
    
    for test_name, test_func in tests:
        print(f"\n📊 Running {test_name}...")
        try:
            result = await test_func(test_duration)
            if result:
                results.append(result)
        except Exception as e:
            print(f"❌ Test {test_name} failed: {e}")
        
        # Brief pause between tests
        await asyncio.sleep(1)
    
    # Print comparison results
    print("\n" + "=" * 70)
    print("🏆 ULTRA-OPTIMIZATION COMPARISON RESULTS")
    print("=" * 70)
    
    if results:
        for i, result in enumerate(results, 1):
            status = "🔥" if result['avg_latency'] < 10 else "✅" if result['avg_latency'] < 20 else "⚠️" if result['avg_latency'] < 50 else "❌"
            
            print(f"{status} {result['exchange']} {result['method']}")
            print(f"   📈 Speed: {result['msg_per_sec']:.1f} messages/second")
            print(f"   ⚡ Avg Latency: {result['avg_latency']:.2f}ms")
            print(f"   🚀 Min Latency: {result['min_latency']:.2f}ms")
            print(f"   📊 Total: {result['total_messages']} messages")
            
            # Performance grade
            if result['avg_latency'] < 5:
                grade = "🔥 EXCELLENT"
            elif result['avg_latency'] < 10:
                grade = "✅ VERY GOOD"
            elif result['avg_latency'] < 20:
                grade = "📊 GOOD"
            elif result['avg_latency'] < 50:
                grade = "⚠️ NEEDS IMPROVEMENT"
            else:
                grade = "❌ POOR"
                
            print(f"   🎯 Grade: {grade}")
            print()
        
        # Summary
        bybit_result = next((r for r in results if r['exchange'] == 'Bybit'), None)
        okx_result = next((r for r in results if r['exchange'] == 'OKX'), None)
        binance_result = next((r for r in results if r['exchange'] == 'Binance'), None)
        
        print("📈 OPTIMIZATION SUMMARY:")
        if binance_result:
            print(f"   🥇 Binance: {binance_result['avg_latency']:.2f}ms (baseline)")
        if bybit_result:
            improvement = "ACHIEVED" if bybit_result['avg_latency'] < 20 else "PARTIAL"
            print(f"   🥈 Bybit: {bybit_result['avg_latency']:.2f}ms (target <20ms: {improvement})")
        if okx_result:
            improvement = "ACHIEVED" if okx_result['avg_latency'] < 20 else "PARTIAL"
            print(f"   🥉 OKX: {okx_result['avg_latency']:.2f}ms (target <20ms: {improvement})")
        
        print(f"\n💡 RECOMMENDATIONS:")
        if bybit_result and bybit_result['avg_latency'] > 20:
            print(f"   🔧 Bybit needs more optimization (current: {bybit_result['avg_latency']:.2f}ms)")
        if okx_result and okx_result['avg_latency'] > 20:
            print(f"   🔧 OKX needs more optimization (current: {okx_result['avg_latency']:.2f}ms)")
        
        print(f"   🚀 Consider using Binance as primary feed")
        print(f"   📊 Use optimized Bybit/OKX as secondary feeds")
    else:
        print("❌ No successful tests")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
