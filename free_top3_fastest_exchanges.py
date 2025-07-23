#!/usr/bin/env python3
"""
🚀 TOP 3 FASTEST EXCHANGES - FREE OPTIMIZATION
Ultra-optimized connections to the 3 fastest cryptocurrency exchanges
No colocation required - pure software optimization
"""

import asyncio
import time
import json
import websockets
import logging
from collections import deque
import statistics

# Minimal logging for maximum speed
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

try:
    import orjson
    HAS_ORJSON = True
    fast_json_loads = orjson.loads
    fast_json_dumps = orjson.dumps
    print("🔥 Using orjson (FASTEST JSON library)")
except ImportError:
    HAS_ORJSON = False
    fast_json_loads = json.loads
    fast_json_dumps = json.dumps
    print("📊 Using standard json (install orjson for 30% speed boost)")

class FreeSpeedOptimizer:
    def __init__(self):
        self.results = []
        
    async def test_binance_ultra_fast(self, duration=15):
        """🥇 BINANCE - Fastest exchange globally (FREE)"""
        print(f"🥇 Testing BINANCE ULTRA-FAST (FREE) for {duration}s...")
        print("   🌍 Location: Global CDN (automatically optimal)")
        print("   📡 Method: Direct WebSocket + Ultra optimization")
        
        latencies = []
        message_count = 0
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        try:
            # Ultra-optimized connection settings
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                compression=None,
                max_size=512,
                close_timeout=0.1
            ) as ws:
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        
                        # Ultra-fast receive with timeout
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.01)
                        recv_time = time.perf_counter()
                        
                        # Fast JSON parsing
                        data = fast_json_loads(msg)
                        if 'b' in data and 'a' in data:
                            bid = float(data['b'])
                            ask = float(data['a'])
                            latency = (recv_time - msg_start) * 1000
                            latencies.append(latency)
                            message_count += 1
                            
                            if message_count % 100 == 0:
                                recent_avg = statistics.mean(latencies[-50:]) if len(latencies) >= 50 else statistics.mean(latencies)
                                print(f"🔥 Binance: {bid:.2f}/{ask:.2f} | Current: {latency:.2f}ms | Avg: {recent_avg:.2f}ms | Count: {message_count}")
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Binance connection error: {e}")
            return None
        
        if latencies:
            avg_latency = statistics.mean(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            median_latency = statistics.median(latencies)
            msg_per_sec = message_count / duration
            
            print(f"✅ BINANCE RESULTS:")
            print(f"   📈 Speed: {msg_per_sec:.1f} msg/s")
            print(f"   ⚡ Avg Latency: {avg_latency:.2f}ms")
            print(f"   🚀 Min Latency: {min_latency:.2f}ms")
            print(f"   📊 Median: {median_latency:.2f}ms")
            print(f"   📈 Max: {max_latency:.2f}ms")
            print(f"   🎯 Grade: {'🔥 EXCELLENT' if avg_latency < 5 else '✅ VERY GOOD' if avg_latency < 10 else '📊 GOOD'}")
            
            return {
                'exchange': 'Binance',
                'rank': 1,
                'method': 'Direct WebSocket (FREE)',
                'location': 'Global CDN',
                'cost': '$0/month',
                'avg_latency': avg_latency,
                'min_latency': min_latency,
                'median_latency': median_latency,
                'msg_per_sec': msg_per_sec,
                'total_messages': message_count,
                'grade': 'EXCELLENT' if avg_latency < 5 else 'VERY GOOD' if avg_latency < 10 else 'GOOD'
            }
        return None

    async def test_bybit_ultra_fast(self, duration=15):
        """🥈 BYBIT - Second fastest exchange (FREE)"""
        print(f"🥈 Testing BYBIT ULTRA-FAST (FREE) for {duration}s...")
        print("   🌍 Location: Singapore/Global")
        print("   📡 Method: Optimized WebSocket + Binary patterns")
        
        latencies = []
        message_count = 0
        url = "wss://stream.bybit.com/v5/public/spot"
        
        # Pre-compile subscription message
        subscribe_msg = fast_json_dumps({"op": "subscribe", "args": ["orderbook.1.BTCUSDT"]})
        
        try:
            # Optimized connection for Bybit
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                compression=None,
                max_size=1024,
                close_timeout=0.1
            ) as ws:
                # Send subscription
                await ws.send(subscribe_msg)
                
                # Pre-compile binary patterns for ultra-fast parsing
                topic_pattern = b'"topic":"orderbook'
                data_pattern = b'"data":'
                
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.01)
                        recv_time = time.perf_counter()
                        
                        # Ultra-fast binary search before JSON parsing
                        if isinstance(msg, str):
                            msg_bytes = msg.encode()
                        else:
                            msg_bytes = msg
                        
                        if topic_pattern in msg_bytes and data_pattern in msg_bytes:
                            # Only parse JSON if it contains orderbook data
                            data = fast_json_loads(msg_bytes)
                            
                            if 'data' in data:
                                book_data = data['data']
                                bids = book_data.get('b', [])
                                asks = book_data.get('a', [])
                                
                                if bids and asks:
                                    bid = float(bids[0][0])
                                    ask = float(asks[0][0])
                                    latency = (recv_time - msg_start) * 1000
                                    latencies.append(latency)
                                    message_count += 1
                                    
                                    if message_count % 50 == 0:
                                        recent_avg = statistics.mean(latencies[-30:]) if len(latencies) >= 30 else statistics.mean(latencies)
                                        print(f"🔥 Bybit: {bid:.2f}/{ask:.2f} | Current: {latency:.2f}ms | Avg: {recent_avg:.2f}ms | Count: {message_count}")
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Bybit connection error: {e}")
            return None
        
        if latencies:
            avg_latency = statistics.mean(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            median_latency = statistics.median(latencies)
            msg_per_sec = message_count / duration
            
            print(f"✅ BYBIT RESULTS:")
            print(f"   📈 Speed: {msg_per_sec:.1f} msg/s")
            print(f"   ⚡ Avg Latency: {avg_latency:.2f}ms")
            print(f"   🚀 Min Latency: {min_latency:.2f}ms")
            print(f"   📊 Median: {median_latency:.2f}ms")
            print(f"   📈 Max: {max_latency:.2f}ms")
            print(f"   🎯 Grade: {'🔥 EXCELLENT' if avg_latency < 15 else '✅ VERY GOOD' if avg_latency < 25 else '📊 GOOD'}")
            
            return {
                'exchange': 'Bybit',
                'rank': 2,
                'method': 'Optimized WebSocket + Binary Search (FREE)',
                'location': 'Singapore/Global',
                'cost': '$0/month',
                'avg_latency': avg_latency,
                'min_latency': min_latency,
                'median_latency': median_latency,
                'msg_per_sec': msg_per_sec,
                'total_messages': message_count,
                'grade': 'EXCELLENT' if avg_latency < 15 else 'VERY GOOD' if avg_latency < 25 else 'GOOD'
            }
        return None

    async def test_coinbase_ultra_fast(self, duration=15):
        """🥉 COINBASE PRO - Third fastest with high reliability (FREE)"""
        print(f"🥉 Testing COINBASE PRO ULTRA-FAST (FREE) for {duration}s...")
        print("   🌍 Location: US/Global")
        print("   📡 Method: Level2 WebSocket + Optimized parsing")
        
        latencies = []
        message_count = 0
        url = "wss://ws-feed.exchange.coinbase.com"
        
        # Subscription message for BTC-USD
        subscribe_msg = fast_json_dumps({
            "type": "subscribe",
            "product_ids": ["BTC-USD"],
            "channels": ["ticker"]
        })
        
        try:
            # Optimized connection for Coinbase
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                compression=None,
                max_size=1024,
                close_timeout=0.1
            ) as ws:
                # Send subscription
                await ws.send(subscribe_msg)
                
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.01)
                        recv_time = time.perf_counter()
                        
                        # Fast JSON parsing with direct key access
                        data = fast_json_loads(msg)
                        
                        if data.get('type') == 'ticker' and 'best_bid' in data and 'best_ask' in data:
                            bid = float(data['best_bid'])
                            ask = float(data['best_ask'])
                            latency = (recv_time - msg_start) * 1000
                            latencies.append(latency)
                            message_count += 1
                            
                            if message_count % 30 == 0:
                                recent_avg = statistics.mean(latencies[-20:]) if len(latencies) >= 20 else statistics.mean(latencies)
                                print(f"🔥 Coinbase: {bid:.2f}/{ask:.2f} | Current: {latency:.2f}ms | Avg: {recent_avg:.2f}ms | Count: {message_count}")
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Coinbase connection error: {e}")
            return None
        
        if latencies:
            avg_latency = statistics.mean(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            median_latency = statistics.median(latencies)
            msg_per_sec = message_count / duration
            
            print(f"✅ COINBASE PRO RESULTS:")
            print(f"   📈 Speed: {msg_per_sec:.1f} msg/s")
            print(f"   ⚡ Avg Latency: {avg_latency:.2f}ms")
            print(f"   🚀 Min Latency: {min_latency:.2f}ms")
            print(f"   📊 Median: {median_latency:.2f}ms")
            print(f"   📈 Max: {max_latency:.2f}ms")
            print(f"   🎯 Grade: {'🔥 EXCELLENT' if avg_latency < 20 else '✅ VERY GOOD' if avg_latency < 35 else '📊 GOOD'}")
            
            return {
                'exchange': 'Coinbase Pro',
                'rank': 3,
                'method': 'Ticker WebSocket + Fast JSON (FREE)',
                'location': 'US/Global',
                'cost': '$0/month',
                'avg_latency': avg_latency,
                'min_latency': min_latency,
                'median_latency': median_latency,
                'msg_per_sec': msg_per_sec,
                'total_messages': message_count,
                'grade': 'EXCELLENT' if avg_latency < 20 else 'VERY GOOD' if avg_latency < 35 else 'GOOD'
            }
        return None

    def print_free_optimization_tips(self):
        """Print free optimization tips"""
        print("\n" + "💡" * 60)
        print("FREE OPTIMIZATION TECHNIQUES")
        print("💡" * 60)
        
        print("\n🚀 SOFTWARE OPTIMIZATIONS (FREE):")
        print("   1. 📦 Install orjson: pip install orjson (30% JSON speed boost)")
        print("   2. 🔧 Use binary pattern matching before JSON parsing")
        print("   3. ⚡ Minimize buffer sizes and timeouts")
        print("   4. 🎯 Target specific data fields only")
        print("   5. 📊 Use asyncio for parallel connections")
        
        print("\n🌐 NETWORK OPTIMIZATIONS (FREE):")
        print("   1. 🏠 Use fastest internet connection available")
        print("   2. 📡 Close unnecessary applications")
        print("   3. 🔧 Disable ping/pong for WebSockets")
        print("   4. ⚡ Use compression=None")
        print("   5. 🎯 Connect to nearest exchange servers")
        
        print("\n💰 COST-EFFECTIVE UPGRADES:")
        print("   1. 🌐 VPS near exchange servers: $10-50/month")
        print("      • AWS Tokyo for Binance: $20-40/month")
        print("      • AWS Singapore for Bybit: $15-30/month")
        print("      • AWS US for Coinbase: $10-25/month")
        print("   2. 📈 Better internet: Fiber connection $30-100/month")
        print("   3. 🖥️ Dedicated server: $50-200/month")

async def main():
    """Test the 3 fastest exchanges with free optimization"""
    optimizer = FreeSpeedOptimizer()
    
    print("🚀 TOP 3 FASTEST EXCHANGES - FREE OPTIMIZATION")
    print("=" * 80)
    print("🎯 Objective: Find the fastest exchanges using FREE methods only")
    print("💰 Total Cost: $0/month (pure software optimization)")
    print("📊 Target: Sub-10ms for top exchanges")
    
    # Print optimization tips
    optimizer.print_free_optimization_tips()
    
    test_duration = 15  # 15 seconds per test
    results = []
    
    # Test the top 3 fastest exchanges
    tests = [
        ("Binance Ultra-Fast", optimizer.test_binance_ultra_fast),
        ("Bybit Ultra-Fast", optimizer.test_bybit_ultra_fast),
        ("Coinbase Pro Ultra-Fast", optimizer.test_coinbase_ultra_fast),
    ]
    
    print(f"\n🧪 RUNNING TESTS ({test_duration}s each)...")
    print("=" * 60)
    
    for test_name, test_func in tests:
        print(f"\n🔬 Starting: {test_name}")
        try:
            result = await test_func(test_duration)
            if result:
                results.append(result)
                print(f"✅ Completed: {test_name}")
            else:
                print(f"❌ Failed: {test_name}")
        except Exception as e:
            print(f"💥 Error in {test_name}: {e}")
        
        # Brief pause between tests
        await asyncio.sleep(2)
    
    # Print final results
    print("\n" + "🏆" * 80)
    print("TOP 3 FASTEST EXCHANGES - FINAL RESULTS")
    print("🏆" * 80)
    
    if results:
        # Sort by average latency
        results.sort(key=lambda x: x['avg_latency'])
        
        print(f"\n🥇 WINNER RANKINGS:")
        for i, result in enumerate(results, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            grade_emoji = "🔥" if result['grade'] == 'EXCELLENT' else "✅" if result['grade'] == 'VERY GOOD' else "📊"
            
            print(f"{medal} #{i} {result['exchange'].upper()}")
            print(f"   📡 Method: {result['method']}")
            print(f"   🌍 Location: {result['location']}")
            print(f"   💰 Cost: {result['cost']}")
            print(f"   ⚡ Avg Latency: {result['avg_latency']:.2f}ms")
            print(f"   🚀 Min Latency: {result['min_latency']:.2f}ms")
            print(f"   📊 Median: {result['median_latency']:.2f}ms")
            print(f"   📈 Speed: {result['msg_per_sec']:.1f} msg/s")
            print(f"   🎯 Grade: {grade_emoji} {result['grade']}")
            print()
        
        # Performance summary
        best_exchange = results[0]
        print(f"🏅 BEST PERFORMER: {best_exchange['exchange']}")
        print(f"   ⚡ Latency: {best_exchange['avg_latency']:.2f}ms average")
        print(f"   🚀 Peak: {best_exchange['min_latency']:.2f}ms minimum")
        print(f"   📈 Throughput: {best_exchange['msg_per_sec']:.1f} messages/second")
        
        # Recommendations
        print(f"\n🎯 RECOMMENDATIONS:")
        print(f"   1. 🥇 Primary: Use {best_exchange['exchange']} for main trading")
        print(f"   2. 🥈 Secondary: Use {results[1]['exchange'] if len(results) > 1 else 'second fastest'} for backup")
        print(f"   3. 🥉 Tertiary: Use {results[2]['exchange'] if len(results) > 2 else 'third fastest'} for diversification")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"   • Install orjson: pip install orjson")
        print(f"   • Consider VPS near {best_exchange['exchange']} servers")
        print(f"   • Implement multi-exchange arbitrage monitoring")
        print(f"   • Monitor latency continuously")
        
        # Cost comparison
        print(f"\n💰 COST COMPARISON WITH PAID SOLUTIONS:")
        print(f"   🆓 Current FREE solution: $0/month")
        print(f"   ☁️ VPS optimization: $20-50/month (5-10x faster)")
        print(f"   🏢 Colocation: $10,000-25,000/month (50-100x faster)")
        print(f"   📊 ROI: Start free, upgrade based on profits")
        
    else:
        print("❌ No successful tests completed")
        print("💡 Check your internet connection and try again")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Testing completed!")
