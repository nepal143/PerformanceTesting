#!/usr/bin/env python3
"""
🔥 MEXC & KUCOIN SPEED TEST
Focused testing for MEXC and KuCoin exchanges with proper connection methods
Finding their true ultra-fast speeds
"""

import asyncio
import time
import json
import websockets
import aiohttp
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
    print("⚠️ Install orjson for 30% speed boost: pip install orjson")

class MexcKucoinSpeedTester:
    def __init__(self):
        self.results = []
        
    async def test_mexc_ultra_v2(self, duration=25):
        """🥉 MEXC - Ultra-optimized v2 test with multiple connection methods"""
        print(f"🥉 Testing MEXC ULTRA-OPTIMIZED V2 for {duration}s...")
        print("   🌍 Location: Asia/Global")
        print("   📡 Method: Multiple WebSocket endpoints + fallback")
        
        # Try multiple MEXC endpoints
        endpoints = [
            {
                'url': 'wss://wbs.mexc.com/ws',
                'subscribe': {
                    "method": "SUBSCRIPTION", 
                    "params": ["spot@public.bookTicker.v3.api@BTCUSDT"]
                },
                'name': 'MEXC Main WebSocket'
            },
            {
                'url': 'wss://wbs.mexc.com/raw/ws',
                'subscribe': {
                    "method": "SUBSCRIPTION",
                    "params": ["spot@public.deals.v3.api@BTCUSDT"]
                },
                'name': 'MEXC Raw WebSocket'
            },
            {
                'url': 'wss://contract.mexc.com/ws',
                'subscribe': {
                    "method": "sub.ticker",
                    "param": {"symbol": "BTC_USDT"}
                },
                'name': 'MEXC Contract WebSocket'
            }
        ]
        
        latencies = []
        message_count = 0
        successful_endpoint = None
        
        for endpoint in endpoints:
            print(f"   🔗 Trying: {endpoint['name']}")
            try:
                async with websockets.connect(
                    endpoint['url'],
                    ping_interval=None,
                    ping_timeout=None,
                    compression=None,
                    max_size=1024,
                    close_timeout=0.1
                ) as ws:
                    
                    # Send subscription
                    subscribe_msg = fast_json_dumps(endpoint['subscribe'])
                    await ws.send(subscribe_msg)
                    
                    # Test for 5 seconds to see if we get data
                    test_start = time.perf_counter()
                    test_messages = 0
                    
                    while time.perf_counter() - test_start < 5:
                        try:
                            msg_start = time.perf_counter()
                            msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                            recv_time = time.perf_counter()
                            
                            data = fast_json_loads(msg)
                            
                            # Try different MEXC data structures
                            bid, ask = None, None
                            
                            # Method 1: bookTicker format
                            if 'd' in data and isinstance(data['d'], dict):
                                ticker_data = data['d']
                                if 'b' in ticker_data and 'a' in ticker_data:
                                    bid = float(ticker_data['b'])
                                    ask = float(ticker_data['a'])
                            
                            # Method 2: deals format  
                            elif 'data' in data and isinstance(data['data'], dict):
                                if 'p' in data['data']:  # price field
                                    price = float(data['data']['p'])
                                    bid = price * 0.9999  # Simulate bid
                                    ask = price * 1.0001  # Simulate ask
                            
                            # Method 3: ticker format
                            elif 'tick' in data:
                                tick_data = data['tick']
                                if 'bid' in tick_data and 'ask' in tick_data:
                                    bid = float(tick_data['bid'])
                                    ask = float(tick_data['ask'])
                            
                            # Method 4: Simple price format
                            elif 'symbol' in data and 'price' in data:
                                price = float(data['price'])
                                bid = price * 0.9999
                                ask = price * 1.0001
                            
                            if bid and ask:
                                latency = (recv_time - msg_start) * 1000
                                test_messages += 1
                                print(f"   ✅ {endpoint['name']}: {bid:.2f}/{ask:.2f} | Latency: {latency:.3f}ms")
                                
                                if test_messages >= 3:  # Got enough test data
                                    successful_endpoint = endpoint
                                    break
                        
                        except asyncio.TimeoutError:
                            continue
                        except Exception as e:
                            print(f"   ⚠️ Parse error: {e}")
                            continue
                    
                    if successful_endpoint:
                        print(f"   🎯 SUCCESS with {endpoint['name']}!")
                        break
                    else:
                        print(f"   ❌ No valid data from {endpoint['name']}")
                        
            except Exception as e:
                print(f"   ❌ Connection failed for {endpoint['name']}: {e}")
                continue
        
        if not successful_endpoint:
            print("❌ All MEXC endpoints failed")
            return None
            
        # Now run the full test with the successful endpoint
        print(f"\n🚀 Running full test with {successful_endpoint['name']}...")
        
        try:
            async with websockets.connect(
                successful_endpoint['url'],
                ping_interval=None,
                ping_timeout=None,
                compression=None,
                max_size=512,
                close_timeout=0.1
            ) as ws:
                
                subscribe_msg = fast_json_dumps(successful_endpoint['subscribe'])
                await ws.send(subscribe_msg)
                
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.1)
                        recv_time = time.perf_counter()
                        
                        data = fast_json_loads(msg)
                        
                        # Use the same parsing logic that worked
                        bid, ask = None, None
                        
                        if 'd' in data and isinstance(data['d'], dict):
                            ticker_data = data['d']
                            if 'b' in ticker_data and 'a' in ticker_data:
                                bid = float(ticker_data['b'])
                                ask = float(ticker_data['a'])
                        elif 'data' in data and isinstance(data['data'], dict):
                            if 'p' in data['data']:
                                price = float(data['data']['p'])
                                bid = price * 0.9999
                                ask = price * 1.0001
                        elif 'tick' in data:
                            tick_data = data['tick']
                            if 'bid' in tick_data and 'ask' in tick_data:
                                bid = float(tick_data['bid'])
                                ask = float(tick_data['ask'])
                        elif 'symbol' in data and 'price' in data:
                            price = float(data['price'])
                            bid = price * 0.9999
                            ask = price * 1.0001
                        
                        if bid and ask:
                            latency = (recv_time - msg_start) * 1000
                            latencies.append(latency)
                            message_count += 1
                            
                            if message_count % 50 == 0:
                                recent_avg = statistics.mean(latencies[-30:]) if len(latencies) >= 30 else statistics.mean(latencies)
                                print(f"🔥 MEXC: {bid:.2f}/{ask:.2f} | Current: {latency:.3f}ms | Avg: {recent_avg:.3f}ms | Count: {message_count}")
                    
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ MEXC full test error: {e}")
            return None
        
        if latencies:
            return self._calculate_results('MEXC', successful_endpoint['name'], latencies, message_count, duration, '🥉')
        return None

    async def test_kucoin_ultra_v2(self, duration=25):
        """🔥 KUCOIN - Ultra-optimized v2 test with proper token handling"""
        print(f"🔥 Testing KUCOIN ULTRA-OPTIMIZED V2 for {duration}s...")
        print("   🌍 Location: Global")
        print("   📡 Method: Public bullet + Multiple channels")
        
        latencies = []
        message_count = 0
        
        try:
            # Get WebSocket endpoint and token from KuCoin API
            print("   🔑 Getting KuCoin WebSocket token...")
            
            async with aiohttp.ClientSession() as session:
                # Try public bullet endpoint
                try:
                    async with session.post(
                        'https://api.kucoin.com/api/v1/bullet-public',
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as resp:
                        if resp.status == 200:
                            response_data = await resp.json()
                            token = response_data['data']['token']
                            endpoint = response_data['data']['instanceServers'][0]['endpoint']
                            ping_interval = response_data['data']['instanceServers'][0]['pingInterval']
                            
                            print(f"   ✅ Got token: {token[:20]}...")
                            print(f"   🔗 Endpoint: {endpoint}")
                            
                            # Construct WebSocket URL
                            ws_url = f"{endpoint}?token={token}&[connectId=mexc_kucoin_speed_test]"
                            
                            # Try multiple subscription channels
                            channels = [
                                {
                                    'topic': '/market/ticker:BTC-USDT',
                                    'name': 'Ticker Channel'
                                },
                                {
                                    'topic': '/spotMarket/level2Depth5:BTC-USDT',
                                    'name': 'Level2 Depth'
                                },
                                {
                                    'topic': '/market/match:BTC-USDT',
                                    'name': 'Match Execution'
                                }
                            ]
                            
                            successful_channel = None
                            
                            for channel in channels:
                                print(f"   🔗 Trying: {channel['name']}")
                                
                                try:
                                    async with websockets.connect(
                                        ws_url,
                                        ping_interval=None,
                                        ping_timeout=None,
                                        compression=None,
                                        max_size=1024,
                                        close_timeout=0.1
                                    ) as ws:
                                        
                                        # Subscribe to channel
                                        subscribe_msg = fast_json_dumps({
                                            "type": "subscribe",
                                            "topic": channel['topic'],
                                            "id": f"test_{int(time.time())}"
                                        })
                                        await ws.send(subscribe_msg)
                                        
                                        # Test for 5 seconds
                                        test_start = time.perf_counter()
                                        test_messages = 0
                                        
                                        while time.perf_counter() - test_start < 5:
                                            try:
                                                msg_start = time.perf_counter()
                                                msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                                                recv_time = time.perf_counter()
                                                
                                                data = fast_json_loads(msg)
                                                
                                                # Parse different KuCoin message types
                                                bid, ask = None, None
                                                
                                                if data.get('type') == 'message':
                                                    topic = data.get('topic', '')
                                                    data_payload = data.get('data', {})
                                                    
                                                    # Ticker data
                                                    if '/market/ticker' in topic:
                                                        if 'bestBid' in data_payload and 'bestAsk' in data_payload:
                                                            bid = float(data_payload['bestBid'])
                                                            ask = float(data_payload['bestAsk'])
                                                    
                                                    # Level2 depth data
                                                    elif '/level2Depth' in topic:
                                                        if 'bids' in data_payload and 'asks' in data_payload:
                                                            bids = data_payload['bids']
                                                            asks = data_payload['asks']
                                                            if bids and asks:
                                                                bid = float(bids[0][0])
                                                                ask = float(asks[0][0])
                                                    
                                                    # Match execution data
                                                    elif '/market/match' in topic:
                                                        if 'price' in data_payload:
                                                            price = float(data_payload['price'])
                                                            bid = price * 0.9999
                                                            ask = price * 1.0001
                                                
                                                if bid and ask:
                                                    latency = (recv_time - msg_start) * 1000
                                                    test_messages += 1
                                                    print(f"   ✅ {channel['name']}: {bid:.2f}/{ask:.2f} | Latency: {latency:.3f}ms")
                                                    
                                                    if test_messages >= 3:
                                                        successful_channel = channel
                                                        break
                                            
                                            except asyncio.TimeoutError:
                                                continue
                                            except Exception as e:
                                                print(f"   ⚠️ Parse error: {e}")
                                                continue
                                        
                                        if successful_channel:
                                            print(f"   🎯 SUCCESS with {channel['name']}!")
                                            break
                                        else:
                                            print(f"   ❌ No valid data from {channel['name']}")
                                
                                except Exception as e:
                                    print(f"   ❌ Connection failed for {channel['name']}: {e}")
                                    continue
                            
                            if not successful_channel:
                                print("❌ All KuCoin channels failed")
                                return None
                            
                            # Run full test with successful channel
                            print(f"\n🚀 Running full test with {successful_channel['name']}...")
                            
                            async with websockets.connect(
                                ws_url,
                                ping_interval=None,
                                ping_timeout=None,
                                compression=None,
                                max_size=512,
                                close_timeout=0.1
                            ) as ws:
                                
                                subscribe_msg = fast_json_dumps({
                                    "type": "subscribe",
                                    "topic": successful_channel['topic'],
                                    "id": f"full_test_{int(time.time())}"
                                })
                                await ws.send(subscribe_msg)
                                
                                start_time = time.perf_counter()
                                
                                while time.perf_counter() - start_time < duration:
                                    try:
                                        msg_start = time.perf_counter()
                                        msg = await asyncio.wait_for(ws.recv(), timeout=0.1)
                                        recv_time = time.perf_counter()
                                        
                                        data = fast_json_loads(msg)
                                        
                                        # Use same parsing logic that worked
                                        bid, ask = None, None
                                        
                                        if data.get('type') == 'message':
                                            topic = data.get('topic', '')
                                            data_payload = data.get('data', {})
                                            
                                            if '/market/ticker' in topic:
                                                if 'bestBid' in data_payload and 'bestAsk' in data_payload:
                                                    bid = float(data_payload['bestBid'])
                                                    ask = float(data_payload['bestAsk'])
                                            elif '/level2Depth' in topic:
                                                if 'bids' in data_payload and 'asks' in data_payload:
                                                    bids = data_payload['bids']
                                                    asks = data_payload['asks']
                                                    if bids and asks:
                                                        bid = float(bids[0][0])
                                                        ask = float(asks[0][0])
                                            elif '/market/match' in topic:
                                                if 'price' in data_payload:
                                                    price = float(data_payload['price'])
                                                    bid = price * 0.9999
                                                    ask = price * 1.0001
                                        
                                        if bid and ask:
                                            latency = (recv_time - msg_start) * 1000
                                            latencies.append(latency)
                                            message_count += 1
                                            
                                            if message_count % 30 == 0:
                                                recent_avg = statistics.mean(latencies[-20:]) if len(latencies) >= 20 else statistics.mean(latencies)
                                                print(f"🔥 KuCoin: {bid:.2f}/{ask:.2f} | Current: {latency:.3f}ms | Avg: {recent_avg:.3f}ms | Count: {message_count}")
                                    
                                    except asyncio.TimeoutError:
                                        continue
                                    except Exception:
                                        continue
                        
                        else:
                            print(f"❌ Failed to get KuCoin token: HTTP {resp.status}")
                            return None
                            
                except Exception as e:
                    print(f"❌ KuCoin API request failed: {e}")
                    return None
                        
        except Exception as e:
            print(f"❌ KuCoin connection error: {e}")
            return None
        
        if latencies:
            return self._calculate_results('KuCoin', successful_channel['name'], latencies, message_count, duration, '🔥')
        return None

    def _calculate_results(self, exchange, method, latencies, message_count, duration, emoji):
        """Calculate comprehensive results"""
        avg_latency = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        median_latency = statistics.median(latencies)
        
        # Calculate percentiles safely
        if len(latencies) >= 20:
            p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th percentile
        else:
            p95_latency = max_latency
            
        if len(latencies) >= 100:
            p99_latency = statistics.quantiles(latencies, n=100)[98]  # 99th percentile
        else:
            p99_latency = max_latency
            
        msg_per_sec = message_count / duration
        
        # Calculate grade
        if avg_latency < 1:
            grade = 'EXCEPTIONAL'
        elif avg_latency < 5:
            grade = 'EXCELLENT'
        elif avg_latency < 15:
            grade = 'VERY GOOD'
        elif avg_latency < 30:
            grade = 'GOOD'
        elif avg_latency < 100:
            grade = 'FAIR'
        else:
            grade = 'POOR'
        
        print(f"✅ {exchange.upper()} RESULTS:")
        print(f"   📈 Speed: {msg_per_sec:.1f} msg/s")
        print(f"   ⚡ Avg Latency: {avg_latency:.3f}ms")
        print(f"   🚀 Min Latency: {min_latency:.3f}ms")
        print(f"   📊 Median: {median_latency:.3f}ms")
        print(f"   📈 95th %ile: {p95_latency:.3f}ms")
        print(f"   📉 99th %ile: {p99_latency:.3f}ms")
        print(f"   📈 Max: {max_latency:.3f}ms")
        print(f"   🎯 Grade: {grade}")
        
        return {
            'exchange': exchange,
            'emoji': emoji,
            'method': method,
            'avg_latency': avg_latency,
            'min_latency': min_latency,
            'max_latency': max_latency,
            'median_latency': median_latency,
            'p95_latency': p95_latency,
            'p99_latency': p99_latency,
            'msg_per_sec': msg_per_sec,
            'total_messages': message_count,
            'grade': grade
        }

async def main():
    """Test MEXC and KuCoin with proper connection methods"""
    tester = MexcKucoinSpeedTester()
    
    print("🔥 MEXC & KUCOIN FOCUSED SPEED TEST")
    print("=" * 60)
    print("🎯 Objective: Get MEXC and KuCoin working with true speeds")
    print("💰 Method: FREE ultra-optimized connections with proper endpoints")
    print("📊 Exchanges: MEXC, KuCoin")
    print("⏱️ Duration: 25 seconds per exchange")
    
    test_duration = 25
    results = []
    
    # Test both exchanges
    tests = [
        ("MEXC Ultra V2", tester.test_mexc_ultra_v2),
        ("KuCoin Ultra V2", tester.test_kucoin_ultra_v2),
    ]
    
    print(f"\n🧪 RUNNING TESTS ({test_duration}s each)...")
    print("=" * 40)
    
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
        await asyncio.sleep(3)
    
    # Print comprehensive results
    print("\n" + "🏆" * 60)
    print("MEXC & KUCOIN SPEED TEST - FINAL RESULTS")
    print("🏆" * 60)
    
    if results:
        # Sort by average latency (fastest first)
        results.sort(key=lambda x: x['avg_latency'])
        
        print(f"\n🏅 FINAL RANKINGS (by Average Latency):")
        medals = ["🥇", "🥈"]
        
        for i, result in enumerate(results):
            medal = medals[i] if i < len(medals) else "📊"
            grade_emoji = "🔥" if result['grade'] == 'EXCEPTIONAL' else "✅" if result['grade'] == 'EXCELLENT' else "📊"
            
            print(f"\n{medal} #{i+1} {result['exchange'].upper()}")
            print(f"   📡 Method: {result['method']}")
            print(f"   ⚡ Avg Latency: {result['avg_latency']:.3f}ms")
            print(f"   🚀 Min Latency: {result['min_latency']:.3f}ms")
            print(f"   📊 Median: {result['median_latency']:.3f}ms")
            print(f"   📈 95th %ile: {result['p95_latency']:.3f}ms")
            print(f"   📉 99th %ile: {result['p99_latency']:.3f}ms")
            print(f"   📈 Speed: {result['msg_per_sec']:.1f} msg/s")
            print(f"   🎯 Grade: {grade_emoji} {result['grade']}")
        
        # The winner between these two
        if results:
            winner = results[0]
            print(f"\n🏆 WINNER BETWEEN MEXC & KUCOIN: {winner['exchange'].upper()}")
            print(f"   🔥 FASTEST AVERAGE: {winner['avg_latency']:.3f}ms")
            print(f"   ⚡ FASTEST PEAK: {winner['min_latency']:.3f}ms")
            print(f"   📈 THROUGHPUT: {winner['msg_per_sec']:.1f} messages/second")
            print(f"   🎯 GRADE: {winner['grade']}")
        
        # Performance comparison
        print(f"\n📊 PERFORMANCE COMPARISON:")
        for result in results:
            if results:
                speed_vs_winner = (results[0]['avg_latency'] / result['avg_latency']) * 100
                print(f"   {result['emoji']} {result['exchange']:>8}: {result['avg_latency']:>7.3f}ms ({speed_vs_winner:>5.1f}% of winner speed)")
        
        # Speed assessment
        print(f"\n⚡ SPEED ASSESSMENT:")
        for result in results:
            if result['avg_latency'] < 1:
                print(f"   🔥 {result['exchange']}: EXCEPTIONAL (<1ms) - Perfect for HFT")
            elif result['avg_latency'] < 5:
                print(f"   ✅ {result['exchange']}: EXCELLENT (1-5ms) - Great for arbitrage")
            elif result['avg_latency'] < 15:
                print(f"   📊 {result['exchange']}: VERY GOOD (5-15ms) - Good for swing trading")
            elif result['avg_latency'] < 30:
                print(f"   ⚠️ {result['exchange']}: GOOD (15-30ms) - Acceptable for most strategies")
            elif result['avg_latency'] < 100:
                print(f"   🐌 {result['exchange']}: FAIR (30-100ms) - Slow for time-sensitive trading")
            else:
                print(f"   ❌ {result['exchange']}: POOR (>100ms) - Not recommended for active trading")
        
        print(f"\n💡 RECOMMENDATIONS:")
        if results:
            print(f"   • Use {results[0]['exchange']} as primary among these two")
            if len(results) > 1:
                print(f"   • Use {results[1]['exchange']} as backup/secondary")
            print(f"   • Compare with Binance (0.038ms) and Coinbase (0.085ms)")
            print(f"   • Consider VPS optimization for even better latency")
        
    else:
        print("❌ No successful tests completed")
        print("💡 Both MEXC and KuCoin may have connection issues")
        print("🔧 Possible solutions:")
        print("   • Check firewall settings")
        print("   • Try different network connection")
        print("   • Verify exchange API availability in your region")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 MEXC & KuCoin testing completed!")
