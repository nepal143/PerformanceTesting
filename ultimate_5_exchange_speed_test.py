#!/usr/bin/env python3
"""
🚀 ULTIMATE 5-EXCHANGE SPEED COMPARISON
Testing Bybit, MEXC, KuCoin, Binance, and Coinbase for ultimate speed
Finding the absolute fastest exchange with optimal methods
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
    print("⚠️ Install orjson for 30% speed boost: pip install orjson")

class UltimateExchangeSpeedTester:
    def __init__(self):
        self.results = []
        
    async def test_binance_ultra(self, duration=20):
        """🥇 BINANCE - Global leader test"""
        print(f"🥇 Testing BINANCE ULTRA-OPTIMIZED for {duration}s...")
        print("   🌍 Location: Global CDN")
        print("   📡 Method: Direct bookTicker WebSocket")
        
        latencies = []
        message_count = 0
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        try:
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                compression=None,
                max_size=256,
                close_timeout=0.1
            ) as ws:
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.01)
                        recv_time = time.perf_counter()
                        
                        data = fast_json_loads(msg)
                        if 'b' in data and 'a' in data:
                            bid = float(data['b'])
                            ask = float(data['a'])
                            latency = (recv_time - msg_start) * 1000
                            latencies.append(latency)
                            message_count += 1
                            
                            if message_count % 200 == 0:
                                recent_avg = statistics.mean(latencies[-100:]) if len(latencies) >= 100 else statistics.mean(latencies)
                                print(f"🔥 Binance: {bid:.2f}/{ask:.2f} | Current: {latency:.3f}ms | Avg: {recent_avg:.3f}ms | Count: {message_count}")
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Binance connection error: {e}")
            return None
        
        if latencies:
            return self._calculate_results('Binance', 'Direct bookTicker WebSocket', latencies, message_count, duration, '🥇')
        return None

    async def test_bybit_ultra(self, duration=20):
        """🥈 BYBIT - Singapore powerhouse test"""
        print(f"🥈 Testing BYBIT ULTRA-OPTIMIZED for {duration}s...")
        print("   🌍 Location: Singapore/Global")
        print("   📡 Method: Orderbook WebSocket + Binary optimization")
        
        latencies = []
        message_count = 0
        url = "wss://stream.bybit.com/v5/public/spot"
        
        subscribe_msg = fast_json_dumps({"op": "subscribe", "args": ["orderbook.1.BTCUSDT"]})
        
        try:
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                compression=None,
                max_size=512,
                close_timeout=0.1
            ) as ws:
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
                                    
                                    if message_count % 100 == 0:
                                        recent_avg = statistics.mean(latencies[-50:]) if len(latencies) >= 50 else statistics.mean(latencies)
                                        print(f"🔥 Bybit: {bid:.2f}/{ask:.2f} | Current: {latency:.3f}ms | Avg: {recent_avg:.3f}ms | Count: {message_count}")
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Bybit connection error: {e}")
            return None
        
        if latencies:
            return self._calculate_results('Bybit', 'Orderbook WebSocket + Binary optimization', latencies, message_count, duration, '🥈')
        return None

    async def test_mexc_ultra(self, duration=20):
        """🥉 MEXC - Asian challenger test"""
        print(f"🥉 Testing MEXC ULTRA-OPTIMIZED for {duration}s...")
        print("   🌍 Location: Asia/Global")
        print("   📡 Method: Spot ticker WebSocket")
        
        latencies = []
        message_count = 0
        url = "wss://wbs.mexc.com/ws"
        
        subscribe_msg = fast_json_dumps({
            "method": "SUBSCRIPTION",
            "params": ["spot@public.bookTicker.v3.api@BTCUSDT"]
        })
        
        try:
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                compression=None,
                max_size=512,
                close_timeout=0.1
            ) as ws:
                await ws.send(subscribe_msg)
                
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.01)
                        recv_time = time.perf_counter()
                        
                        data = fast_json_loads(msg)
                        
                        # MEXC uses different structure
                        if 'd' in data and data.get('c') == 'spot@public.bookTicker.v3.api@BTCUSDT':
                            ticker_data = data['d']
                            if 'b' in ticker_data and 'a' in ticker_data:
                                bid = float(ticker_data['b'])
                                ask = float(ticker_data['a'])
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
            print(f"❌ MEXC connection error: {e}")
            return None
        
        if latencies:
            return self._calculate_results('MEXC', 'Spot ticker WebSocket', latencies, message_count, duration, '🥉')
        return None

    async def test_kucoin_ultra(self, duration=20):
        """🔥 KUCOIN - Innovation test"""
        print(f"🔥 Testing KUCOIN ULTRA-OPTIMIZED for {duration}s...")
        print("   🌍 Location: Global")
        print("   📡 Method: Level2 Market Data + Token auth")
        
        latencies = []
        message_count = 0
        
        try:
            # First get WebSocket endpoint and token from KuCoin API
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.kucoin.com/api/v1/bullet-public') as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        token = data['data']['token']
                        endpoint = data['data']['instanceServers'][0]['endpoint']
                        
                        ws_url = f"{endpoint}?token={token}&[connectId=ultra_speed_test]"
                        
                        subscribe_msg = fast_json_dumps({
                            "type": "subscribe",
                            "topic": "/market/ticker:BTC-USDT",
                            "id": "ultra_speed_test"
                        })
                        
                        async with websockets.connect(
                            ws_url,
                            ping_interval=None,
                            ping_timeout=None,
                            compression=None,
                            max_size=512,
                            close_timeout=0.1
                        ) as ws:
                            await ws.send(subscribe_msg)
                            
                            start_time = time.perf_counter()
                            
                            while time.perf_counter() - start_time < duration:
                                try:
                                    msg_start = time.perf_counter()
                                    msg = await asyncio.wait_for(ws.recv(), timeout=0.01)
                                    recv_time = time.perf_counter()
                                    
                                    data = fast_json_loads(msg)
                                    
                                    if data.get('type') == 'message' and data.get('topic') == '/market/ticker:BTC-USDT':
                                        ticker_data = data.get('data', {})
                                        if 'bestBid' in ticker_data and 'bestAsk' in ticker_data:
                                            bid = float(ticker_data['bestBid'])
                                            ask = float(ticker_data['bestAsk'])
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
                        print("❌ Failed to get KuCoin WebSocket token")
                        return None
                        
        except Exception as e:
            print(f"❌ KuCoin connection error: {e}")
            return None
        
        if latencies:
            return self._calculate_results('KuCoin', 'Level2 Market Data + Token auth', latencies, message_count, duration, '🔥')
        return None

    async def test_coinbase_ultra(self, duration=20):
        """💎 COINBASE PRO - Enterprise test"""
        print(f"💎 Testing COINBASE PRO ULTRA-OPTIMIZED for {duration}s...")
        print("   🌍 Location: US/Global")
        print("   📡 Method: Ticker channel WebSocket")
        
        latencies = []
        message_count = 0
        url = "wss://ws-feed.exchange.coinbase.com"
        
        subscribe_msg = fast_json_dumps({
            "type": "subscribe",
            "product_ids": ["BTC-USD"],
            "channels": ["ticker"]
        })
        
        try:
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                compression=None,
                max_size=512,
                close_timeout=0.1
            ) as ws:
                await ws.send(subscribe_msg)
                
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.01)
                        recv_time = time.perf_counter()
                        
                        data = fast_json_loads(msg)
                        
                        if data.get('type') == 'ticker' and 'best_bid' in data and 'best_ask' in data:
                            bid = float(data['best_bid'])
                            ask = float(data['best_ask'])
                            latency = (recv_time - msg_start) * 1000
                            latencies.append(latency)
                            message_count += 1
                            
                            if message_count % 40 == 0:
                                recent_avg = statistics.mean(latencies[-25:]) if len(latencies) >= 25 else statistics.mean(latencies)
                                print(f"🔥 Coinbase: {bid:.2f}/{ask:.2f} | Current: {latency:.3f}ms | Avg: {recent_avg:.3f}ms | Count: {message_count}")
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Coinbase connection error: {e}")
            return None
        
        if latencies:
            return self._calculate_results('Coinbase Pro', 'Ticker channel WebSocket', latencies, message_count, duration, '💎')
        return None

    def _calculate_results(self, exchange, method, latencies, message_count, duration, emoji):
        """Calculate comprehensive results"""
        avg_latency = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        median_latency = statistics.median(latencies)
        p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th percentile
        p99_latency = statistics.quantiles(latencies, n=100)[98]  # 99th percentile
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
        else:
            grade = 'FAIR'
        
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
    """Test all 5 exchanges and find the absolute fastest"""
    tester = UltimateExchangeSpeedTester()
    
    print("🚀 ULTIMATE 5-EXCHANGE SPEED COMPARISON")
    print("=" * 80)
    print("🎯 Objective: Find the ABSOLUTE FASTEST exchange")
    print("💰 Method: FREE ultra-optimized connections")
    print("📊 Exchanges: Binance, Bybit, MEXC, KuCoin, Coinbase Pro")
    print("⏱️ Duration: 20 seconds per exchange")
    
    test_duration = 20
    results = []
    
    # Test all exchanges
    tests = [
        ("Binance Ultra", tester.test_binance_ultra),
        ("Bybit Ultra", tester.test_bybit_ultra),
        ("MEXC Ultra", tester.test_mexc_ultra),
        ("KuCoin Ultra", tester.test_kucoin_ultra),
        ("Coinbase Pro Ultra", tester.test_coinbase_ultra),
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
    
    # Print comprehensive results
    print("\n" + "🏆" * 80)
    print("ULTIMATE 5-EXCHANGE SPEED COMPARISON - FINAL RESULTS")
    print("🏆" * 80)
    
    if results:
        # Sort by average latency (fastest first)
        results.sort(key=lambda x: x['avg_latency'])
        
        print(f"\n🏅 FINAL RANKINGS (by Average Latency):")
        medals = ["🥇", "🥈", "🥉", "🏅", "📊"]
        
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
        
        # The absolute winner
        winner = results[0]
        print(f"\n🏆 ABSOLUTE WINNER: {winner['exchange'].upper()}")
        print(f"   🔥 FASTEST AVERAGE: {winner['avg_latency']:.3f}ms")
        print(f"   ⚡ FASTEST PEAK: {winner['min_latency']:.3f}ms")
        print(f"   📈 THROUGHPUT: {winner['msg_per_sec']:.1f} messages/second")
        print(f"   🎯 GRADE: {winner['grade']}")
        
        # Performance comparison
        print(f"\n📊 PERFORMANCE COMPARISON:")
        for result in results:
            speed_vs_winner = (winner['avg_latency'] / result['avg_latency']) * 100
            print(f"   {result['emoji']} {result['exchange']:>12}: {result['avg_latency']:>7.3f}ms ({speed_vs_winner:>5.1f}% of winner speed)")
        
        # Recommendations
        print(f"\n🎯 RECOMMENDATIONS:")
        print(f"   1. 🥇 PRIMARY: Use {winner['exchange']} for main trading")
        print(f"   2. 🥈 BACKUP: Use {results[1]['exchange'] if len(results) > 1 else 'second fastest'} for redundancy")
        print(f"   3. 🚀 STRATEGY: Focus on {winner['exchange']} for arbitrage")
        print(f"   4. 📊 MONITORING: Track latency continuously")
        
        # Speed tiers
        print(f"\n⚡ SPEED TIERS:")
        exceptional = [r for r in results if r['avg_latency'] < 1]
        excellent = [r for r in results if 1 <= r['avg_latency'] < 5]
        very_good = [r for r in results if 5 <= r['avg_latency'] < 15]
        good = [r for r in results if 15 <= r['avg_latency'] < 30]
        
        if exceptional:
            print(f"   🔥 EXCEPTIONAL (<1ms): {', '.join([r['exchange'] for r in exceptional])}")
        if excellent:
            print(f"   ✅ EXCELLENT (1-5ms): {', '.join([r['exchange'] for r in excellent])}")
        if very_good:
            print(f"   📊 VERY GOOD (5-15ms): {', '.join([r['exchange'] for r in very_good])}")
        if good:
            print(f"   ⚠️ GOOD (15-30ms): {', '.join([r['exchange'] for r in good])}")
        
        # Next steps
        print(f"\n💡 NEXT STEPS:")
        print(f"   • Implement {winner['exchange']} as primary data source")
        print(f"   • Set up multi-exchange arbitrage monitoring")
        print(f"   • Consider VPS near fastest exchange servers")
        print(f"   • Monitor latency patterns during different market hours")
        
    else:
        print("❌ No successful tests completed")
        print("💡 Check your internet connection and try again")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Testing completed!")
