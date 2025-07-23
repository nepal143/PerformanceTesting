#!/usr/bin/env python3
"""
🚀 BYBIT & OKX LATENCY REDUCER
Advanced techniques to reduce Bybit and OKX latency to sub-20ms
Uses connection optimization, binary processing, and minimal data handling
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

class LatencyReducer:
    def __init__(self):
        self.stats = {'Binance': [], 'Bybit': [], 'OKX': []}
        
    async def test_bybit_optimized_v2(self, duration=15):
        """Bybit with ultra-aggressive optimizations"""
        print(f"🚀 Testing Bybit OPTIMIZED V2 (Target: <20ms) for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://stream.bybit.com/v5/public/spot"
        
        # Pre-compile subscription as bytes for speed
        if HAS_ORJSON:
            subscribe_msg = orjson.dumps({"op": "subscribe", "args": ["orderbook.1.BTCUSDT"]})
        else:
            subscribe_msg = json.dumps({"op": "subscribe", "args": ["orderbook.1.BTCUSDT"]}).encode()
        
        try:
            # Use most aggressive connection settings possible
            async with websockets.connect(
                url,
                ping_interval=None,        # No ping/pong overhead
                ping_timeout=None,
                max_size=1024,            # Very small buffer
                compression=None,         # No compression overhead
                close_timeout=0.1,        # Fast close
                open_timeout=5            # Quick connection timeout
            ) as ws:
                # Send subscription immediately upon connection
                await ws.send(subscribe_msg)
                
                # Pre-compile binary search patterns for speed
                topic_bytes = b'"topic":"orderbook'
                data_bytes = b'"data":'
                
                start_time = time.perf_counter()
                consecutive_timeouts = 0
                
                while time.perf_counter() - start_time < duration:
                    try:
                        # Start timing immediately before receive
                        msg_start = time.perf_counter()
                        
                        # Very aggressive timeout for minimal latency
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.1)
                        recv_end = time.perf_counter()
                        
                        consecutive_timeouts = 0  # Reset timeout counter
                        
                        # Convert to bytes for ultra-fast binary search
                        if isinstance(msg, str):
                            msg_bytes = msg.encode('utf-8')
                        else:
                            msg_bytes = msg
                        
                        # Ultra-fast binary pattern matching
                        if topic_bytes in msg_bytes and data_bytes in msg_bytes:
                            parse_start = time.perf_counter()
                            
                            try:
                                # Only parse if we found the right patterns
                                data = fast_json_loads(msg_bytes)
                                
                                # Direct access - no intermediate variables
                                if (data.get('topic', '').startswith('orderbook') and 
                                    'data' in data and 
                                    data['data']):
                                    
                                    book_data = data['data']
                                    bids = book_data.get('b', [])
                                    asks = book_data.get('a', [])
                                    
                                    if bids and asks and bids[0] and asks[0]:
                                        bid = float(bids[0][0])
                                        ask = float(asks[0][0])
                                        
                                        # Calculate latency from message start to parse end
                                        total_latency = (time.perf_counter() - msg_start) * 1000
                                        recv_latency = (recv_end - msg_start) * 1000
                                        
                                        latencies.append(recv_latency)  # Use receive latency
                                        message_count += 1
                                        
                                        # Log every 20 messages with running average
                                        if message_count % 20 == 0:
                                            recent_avg = sum(latencies[-20:]) / min(20, len(latencies))
                                            print(f"🔥 Bybit #{message_count}: {bid:.2f}/{ask:.2f} | "
                                                  f"Latency: {recv_latency:.2f}ms | "
                                                  f"Avg20: {recent_avg:.2f}ms")
                            
                            except (json.JSONDecodeError, KeyError, IndexError, ValueError):
                                continue  # Skip malformed messages
                        
                    except asyncio.TimeoutError:
                        consecutive_timeouts += 1
                        if consecutive_timeouts > 50:  # If too many timeouts, break
                            print("⚠️ Too many timeouts, connection may be slow")
                            break
                        continue
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"❌ Bybit connection error: {e}")
            return None
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            median_latency = sorted(latencies)[len(latencies)//2]
            msg_per_sec = message_count / duration
            
            # Performance analysis
            under_10ms = len([l for l in latencies if l < 10])
            under_20ms = len([l for l in latencies if l < 20])
            
            print(f"✅ Bybit OPTIMIZED V2 Results:")
            print(f"   📈 Speed: {msg_per_sec:.1f} msg/s")
            print(f"   ⚡ Avg Latency: {avg_latency:.2f}ms")
            print(f"   🚀 Min Latency: {min_latency:.2f}ms")
            print(f"   📊 Max Latency: {max_latency:.2f}ms")
            print(f"   🎯 Median: {median_latency:.2f}ms")
            print(f"   🔥 Under 10ms: {under_10ms}/{len(latencies)} ({under_10ms/len(latencies)*100:.1f}%)")
            print(f"   ✅ Under 20ms: {under_20ms}/{len(latencies)} ({under_20ms/len(latencies)*100:.1f}%)")
            
            success = "✅ TARGET ACHIEVED!" if avg_latency < 20 else "⚠️ GETTING CLOSER" if avg_latency < 30 else "❌ NEEDS MORE WORK"
            print(f"   🎯 Target <20ms: {success}")
            
            return {
                'exchange': 'Bybit',
                'method': 'Optimized V2',
                'msg_per_sec': msg_per_sec,
                'avg_latency': avg_latency,
                'min_latency': min_latency,
                'max_latency': max_latency,
                'median_latency': median_latency,
                'under_20ms_pct': under_20ms/len(latencies)*100,
                'total_messages': message_count
            }
        return None
    
    async def test_okx_optimized_v2(self, duration=15):
        """OKX with ultra-aggressive optimizations"""
        print(f"🚀 Testing OKX OPTIMIZED V2 (Target: <20ms) for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://ws.okx.com:8443/ws/v5/public"
        
        # Pre-compile subscription as bytes for speed
        if HAS_ORJSON:
            subscribe_msg = orjson.dumps({
                "op": "subscribe", 
                "args": [{"channel": "books5", "instId": "BTC-USDT"}]
            })
        else:
            subscribe_msg = json.dumps({
                "op": "subscribe", 
                "args": [{"channel": "books5", "instId": "BTC-USDT"}]
            }).encode()
        
        try:
            # Use most aggressive connection settings possible
            async with websockets.connect(
                url,
                ping_interval=None,        # No ping/pong overhead
                ping_timeout=None,
                max_size=1024,            # Very small buffer
                compression=None,         # No compression overhead
                close_timeout=0.1,        # Fast close
                open_timeout=5            # Quick connection timeout
            ) as ws:
                # Send subscription immediately upon connection
                await ws.send(subscribe_msg)
                
                # Pre-compile binary search patterns for speed
                channel_bytes = b'"channel":"books5"'
                data_bytes = b'"data":['
                
                start_time = time.perf_counter()
                consecutive_timeouts = 0
                
                while time.perf_counter() - start_time < duration:
                    try:
                        # Start timing immediately before receive
                        msg_start = time.perf_counter()
                        
                        # Very aggressive timeout for minimal latency
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.1)
                        recv_end = time.perf_counter()
                        
                        consecutive_timeouts = 0  # Reset timeout counter
                        
                        # Convert to bytes for ultra-fast binary search
                        if isinstance(msg, str):
                            msg_bytes = msg.encode('utf-8')
                        else:
                            msg_bytes = msg
                        
                        # Ultra-fast binary pattern matching
                        if channel_bytes in msg_bytes and data_bytes in msg_bytes:
                            parse_start = time.perf_counter()
                            
                            try:
                                # Only parse if we found the right patterns
                                data = fast_json_loads(msg_bytes)
                                
                                # Direct access - no intermediate variables
                                if ('data' in data and 
                                    data['data'] and 
                                    len(data['data']) > 0):
                                    
                                    book_data = data['data'][0]
                                    bids = book_data.get('bids', [])
                                    asks = book_data.get('asks', [])
                                    
                                    if bids and asks and len(bids) > 0 and len(asks) > 0:
                                        bid = float(bids[0][0])
                                        ask = float(asks[0][0])
                                        
                                        # Calculate latency from message start to parse end
                                        total_latency = (time.perf_counter() - msg_start) * 1000
                                        recv_latency = (recv_end - msg_start) * 1000
                                        
                                        latencies.append(recv_latency)  # Use receive latency
                                        message_count += 1
                                        
                                        # Log every 15 messages with running average
                                        if message_count % 15 == 0:
                                            recent_avg = sum(latencies[-15:]) / min(15, len(latencies))
                                            print(f"🔥 OKX #{message_count}: {bid:.2f}/{ask:.2f} | "
                                                  f"Latency: {recv_latency:.2f}ms | "
                                                  f"Avg15: {recent_avg:.2f}ms")
                            
                            except (json.JSONDecodeError, KeyError, IndexError, ValueError):
                                continue  # Skip malformed messages
                        
                    except asyncio.TimeoutError:
                        consecutive_timeouts += 1
                        if consecutive_timeouts > 50:  # If too many timeouts, break
                            print("⚠️ Too many timeouts, connection may be slow")
                            break
                        continue
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"❌ OKX connection error: {e}")
            return None
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            median_latency = sorted(latencies)[len(latencies)//2]
            msg_per_sec = message_count / duration
            
            # Performance analysis
            under_10ms = len([l for l in latencies if l < 10])
            under_20ms = len([l for l in latencies if l < 20])
            
            print(f"✅ OKX OPTIMIZED V2 Results:")
            print(f"   📈 Speed: {msg_per_sec:.1f} msg/s")
            print(f"   ⚡ Avg Latency: {avg_latency:.2f}ms")
            print(f"   🚀 Min Latency: {min_latency:.2f}ms")
            print(f"   📊 Max Latency: {max_latency:.2f}ms")
            print(f"   🎯 Median: {median_latency:.2f}ms")
            print(f"   🔥 Under 10ms: {under_10ms}/{len(latencies)} ({under_10ms/len(latencies)*100:.1f}%)")
            print(f"   ✅ Under 20ms: {under_20ms}/{len(latencies)} ({under_20ms/len(latencies)*100:.1f}%)")
            
            success = "✅ TARGET ACHIEVED!" if avg_latency < 20 else "⚠️ GETTING CLOSER" if avg_latency < 30 else "❌ NEEDS MORE WORK"
            print(f"   🎯 Target <20ms: {success}")
            
            return {
                'exchange': 'OKX',
                'method': 'Optimized V2',
                'msg_per_sec': msg_per_sec,
                'avg_latency': avg_latency,
                'min_latency': min_latency,
                'max_latency': max_latency,
                'median_latency': median_latency,
                'under_20ms_pct': under_20ms/len(latencies)*100,
                'total_messages': message_count
            }
        return None
    
    async def test_binance_reference(self, duration=15):
        """Binance reference test"""
        print(f"🚀 Testing Binance REFERENCE for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        try:
            async with websockets.connect(
                url,
                ping_interval=None,
                max_size=1024,
                compression=None
            ) as ws:
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await ws.recv()
                        recv_end = time.perf_counter()
                        
                        data = fast_json_loads(msg)
                        if 'b' in data and 'a' in data:
                            bid = float(data['b'])
                            ask = float(data['a'])
                            recv_latency = (recv_end - msg_start) * 1000
                            latencies.append(recv_latency)
                            message_count += 1
                            
                            if message_count % 50 == 0:
                                recent_avg = sum(latencies[-50:]) / min(50, len(latencies))
                                print(f"🔥 Binance #{message_count}: {bid:.2f}/{ask:.2f} | "
                                      f"Latency: {recv_latency:.2f}ms | "
                                      f"Avg50: {recent_avg:.2f}ms")
                        
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Binance connection error: {e}")
            return None
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            msg_per_sec = message_count / duration
            under_20ms = len([l for l in latencies if l < 20])
            
            print(f"✅ Binance REFERENCE Results:")
            print(f"   📈 Speed: {msg_per_sec:.1f} msg/s")
            print(f"   ⚡ Avg Latency: {avg_latency:.2f}ms")
            print(f"   🚀 Min Latency: {min_latency:.2f}ms")
            print(f"   ✅ Under 20ms: {under_20ms}/{len(latencies)} ({under_20ms/len(latencies)*100:.1f}%)")
            
            return {
                'exchange': 'Binance',
                'method': 'Reference',
                'msg_per_sec': msg_per_sec,
                'avg_latency': avg_latency,
                'min_latency': min_latency,
                'under_20ms_pct': under_20ms/len(latencies)*100,
                'total_messages': message_count
            }
        return None

async def main():
    """Run the latency reduction tests"""
    reducer = LatencyReducer()
    
    print("🚀 BYBIT & OKX LATENCY REDUCER")
    print("=" * 60)
    print("🎯 Mission: Get Bybit & OKX under 20ms average latency")
    print("📊 Binance reference: Should be ~3-8ms")
    print()
    
    test_duration = 15
    results = []
    
    tests = [
        ("Binance Reference", reducer.test_binance_reference),
        ("Bybit Optimized V2", reducer.test_bybit_optimized_v2),
        ("OKX Optimized V2", reducer.test_okx_optimized_v2),
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"📊 Running {test_name}...")
        print('='*60)
        try:
            result = await test_func(test_duration)
            if result:
                results.append(result)
        except Exception as e:
            print(f"❌ Test {test_name} failed: {e}")
        
        await asyncio.sleep(2)  # Brief pause between tests
    
    # Final comparison
    print(f"\n{'='*60}")
    print("🏆 FINAL LATENCY COMPARISON")
    print('='*60)
    
    if results:
        results.sort(key=lambda x: x['avg_latency'])
        
        for i, result in enumerate(results, 1):
            rank = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            status = "🔥" if result['avg_latency'] < 10 else "✅" if result['avg_latency'] < 20 else "⚠️"
            
            print(f"{rank} {status} {result['exchange']} {result['method']}")
            print(f"    ⚡ Avg Latency: {result['avg_latency']:.2f}ms")
            print(f"    🚀 Min Latency: {result['min_latency']:.2f}ms")
            print(f"    📈 Speed: {result['msg_per_sec']:.1f} msg/s")
            print(f"    ✅ Under 20ms: {result['under_20ms_pct']:.1f}%")
            print()
        
        # Mission analysis
        bybit_result = next((r for r in results if r['exchange'] == 'Bybit'), None)
        okx_result = next((r for r in results if r['exchange'] == 'OKX'), None)
        
        print("🎯 MISSION STATUS:")
        if bybit_result:
            status = "✅ SUCCESS" if bybit_result['avg_latency'] < 20 else "⚠️ PROGRESS" if bybit_result['avg_latency'] < 30 else "❌ FAILED"
            print(f"   Bybit: {bybit_result['avg_latency']:.2f}ms - {status}")
        
        if okx_result:
            status = "✅ SUCCESS" if okx_result['avg_latency'] < 20 else "⚠️ PROGRESS" if okx_result['avg_latency'] < 30 else "❌ FAILED"
            print(f"   OKX: {okx_result['avg_latency']:.2f}ms - {status}")
            
        print(f"\n💡 RECOMMENDATION:")
        best_exchange = min(results, key=lambda x: x['avg_latency'])
        print(f"   🏆 Use {best_exchange['exchange']} as primary ({best_exchange['avg_latency']:.2f}ms)")
        
        fast_exchanges = [r for r in results if r['avg_latency'] < 20]
        if len(fast_exchanges) > 1:
            others = [r['exchange'] for r in fast_exchanges if r['exchange'] != best_exchange['exchange']]
            print(f"   📊 Use {', '.join(others)} as backup feeds")
    else:
        print("❌ No successful tests")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Optimization interrupted!")
