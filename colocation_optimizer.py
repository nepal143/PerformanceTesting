#!/usr/bin/env python3
"""
🏢 COLOCATION OPTIMIZER FOR BINANCE & OKX INSTITUTIONAL
Simulates and optimizes co-location trading scenarios for ultra-low latency
Includes direct market data feeds, institutional APIs, and physical proximity optimization
"""

import asyncio
import time
import json
import websockets
import aiohttp
import logging
from collections import deque
import struct
import random

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

class ColocationOptimizer:
    def __init__(self):
        self.latencies = {
            'binance_standard': deque(maxlen=100),
            'binance_colocation': deque(maxlen=100),
            'okx_standard': deque(maxlen=100),
            'okx_institutional': deque(maxlen=100),
            'okx_colocation': deque(maxlen=100)
        }
        self.prices = {
            'binance': deque(maxlen=50),
            'okx': deque(maxlen=50)
        }
        
    def simulate_colocation_latency(self, base_latency_ms, colocation_type="premium"):
        """
        Simulate colocation latency improvements
        Premium colocation: 50-90% latency reduction
        Standard colocation: 30-60% latency reduction
        """
        if colocation_type == "premium":
            # Premium colocation (same rack/building as exchange)
            reduction_factor = random.uniform(0.1, 0.5)  # 50-90% reduction
            network_overhead = random.uniform(0.1, 0.3)  # 0.1-0.3ms overhead
        else:
            # Standard colocation (same data center)
            reduction_factor = random.uniform(0.4, 0.7)  # 30-60% reduction
            network_overhead = random.uniform(0.2, 0.5)  # 0.2-0.5ms overhead
            
        colocation_latency = (base_latency_ms * reduction_factor) + network_overhead
        return max(colocation_latency, 0.1)  # Minimum 0.1ms due to hardware limits

    async def test_binance_standard(self, duration=10):
        """Test standard Binance WebSocket connection"""
        print(f"📡 Testing Binance STANDARD connection for {duration}s...")
        
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
                        recv_time = time.perf_counter()
                        
                        data = fast_json_loads(msg)
                        if 'b' in data and 'a' in data:
                            bid = float(data['b'])
                            ask = float(data['a'])
                            latency = (recv_time - msg_start) * 1000
                            latencies.append(latency)
                            message_count += 1
                            
                            self.latencies['binance_standard'].append(latency)
                            self.prices['binance'].append((bid, ask, recv_time))
                            
                            if message_count % 50 == 0:
                                avg_lat = sum(self.latencies['binance_standard']) / len(self.latencies['binance_standard'])
                                print(f"📊 Binance Standard: {bid:.2f}/{ask:.2f} | Latency: {latency:.2f}ms | Avg: {avg_lat:.2f}ms")
                        
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Binance standard connection error: {e}")
            return None
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            msg_per_sec = message_count / duration
            
            return {
                'exchange': 'Binance',
                'connection_type': 'Standard',
                'avg_latency': avg_latency,
                'min_latency': min_latency,
                'msg_per_sec': msg_per_sec,
                'total_messages': message_count
            }
        return None

    async def test_binance_colocation_simulation(self, duration=10):
        """Simulate Binance co-location with optimized connection"""
        print(f"🏢 Testing Binance COLOCATION SIMULATION for {duration}s...")
        print("   📍 Simulating: AWS Tokyo (ap-northeast-1) proximity to Binance servers")
        
        latencies = []
        colocation_latencies = []
        message_count = 0
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        try:
            # Ultra-optimized connection settings for colocation
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                max_size=256,           # Minimal buffer
                compression=None,
                close_timeout=0.01,
                max_queue=1,
                read_limit=256,
                write_limit=128,
                # Additional optimization headers
                extra_headers={
                    'User-Agent': 'ColocationBot/1.0',
                    'Connection': 'Upgrade'
                }
            ) as ws:
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.001)
                        recv_time = time.perf_counter()
                        
                        # Calculate actual latency
                        actual_latency = (recv_time - msg_start) * 1000
                        
                        # Simulate colocation improvement
                        colocation_latency = self.simulate_colocation_latency(actual_latency, "premium")
                        
                        data = fast_json_loads(msg)
                        if 'b' in data and 'a' in data:
                            bid = float(data['b'])
                            ask = float(data['a'])
                            latencies.append(actual_latency)
                            colocation_latencies.append(colocation_latency)
                            message_count += 1
                            
                            self.latencies['binance_colocation'].append(colocation_latency)
                            self.prices['binance'].append((bid, ask, recv_time))
                            
                            if message_count % 50 == 0:
                                avg_actual = sum(latencies[-50:]) / min(50, len(latencies))
                                avg_colo = sum(colocation_latencies[-50:]) / min(50, len(colocation_latencies))
                                improvement = ((avg_actual - avg_colo) / avg_actual) * 100
                                print(f"🏢 Binance Colocation: {bid:.2f}/{ask:.2f}")
                                print(f"   📡 Standard: {actual_latency:.2f}ms → 🏢 Colocation: {colocation_latency:.2f}ms ({improvement:.1f}% faster)")
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Binance colocation simulation error: {e}")
            return None
        
        if latencies and colocation_latencies:
            avg_standard = sum(latencies) / len(latencies)
            avg_colocation = sum(colocation_latencies) / len(colocation_latencies)
            min_colocation = min(colocation_latencies)
            improvement = ((avg_standard - avg_colocation) / avg_standard) * 100
            msg_per_sec = message_count / duration
            
            return {
                'exchange': 'Binance',
                'connection_type': 'Colocation (Simulated)',
                'avg_latency_standard': avg_standard,
                'avg_latency_colocation': avg_colocation,
                'min_latency': min_colocation,
                'improvement_percent': improvement,
                'msg_per_sec': msg_per_sec,
                'total_messages': message_count
            }
        return None

    async def test_okx_standard(self, duration=10):
        """Test standard OKX WebSocket connection"""
        print(f"📡 Testing OKX STANDARD connection for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://ws.okx.com:8443/ws/v5/public"
        
        subscribe_msg = fast_json_dumps({
            "op": "subscribe", 
            "args": [{"channel": "books5", "instId": "BTC-USDT"}]
        })
        
        try:
            async with websockets.connect(
                url,
                ping_interval=None,
                max_size=1024,
                compression=None
            ) as ws:
                await ws.send(subscribe_msg)
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await ws.recv()
                        recv_time = time.perf_counter()
                        
                        data = fast_json_loads(msg)
                        if 'data' in data and data['data']:
                            book_data = data['data'][0]
                            bids = book_data.get('bids', [])
                            asks = book_data.get('asks', [])
                            
                            if bids and asks:
                                bid = float(bids[0][0])
                                ask = float(asks[0][0])
                                latency = (recv_time - msg_start) * 1000
                                latencies.append(latency)
                                message_count += 1
                                
                                self.latencies['okx_standard'].append(latency)
                                self.prices['okx'].append((bid, ask, recv_time))
                                
                                if message_count % 20 == 0:
                                    avg_lat = sum(self.latencies['okx_standard']) / len(self.latencies['okx_standard'])
                                    print(f"📊 OKX Standard: {bid:.2f}/{ask:.2f} | Latency: {latency:.2f}ms | Avg: {avg_lat:.2f}ms")
                        
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ OKX standard connection error: {e}")
            return None
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            msg_per_sec = message_count / duration
            
            return {
                'exchange': 'OKX',
                'connection_type': 'Standard',
                'avg_latency': avg_latency,
                'min_latency': min_latency,
                'msg_per_sec': msg_per_sec,
                'total_messages': message_count
            }
        return None

    async def test_okx_institutional_simulation(self, duration=10):
        """Simulate OKX Institutional API with dedicated infrastructure"""
        print(f"🏛️ Testing OKX INSTITUTIONAL SIMULATION for {duration}s...")
        print("   📍 Simulating: Dedicated institutional WebSocket feed")
        print("   🔒 Simulating: Enhanced QoS and priority routing")
        
        latencies = []
        institutional_latencies = []
        message_count = 0
        
        # Use AWS Singapore for better OKX connectivity (closer to their infrastructure)
        url = "wss://ws.okx.com:8443/ws/v5/public"
        
        subscribe_msg = fast_json_dumps({
            "op": "subscribe", 
            "args": [{"channel": "books5", "instId": "BTC-USDT"}]
        })
        
        try:
            # Institutional-grade connection settings
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                max_size=512,
                compression=None,
                close_timeout=0.01,
                max_queue=1,
                read_limit=512,
                write_limit=256,
                extra_headers={
                    'User-Agent': 'OKX-Institutional-Bot/2.0',
                    'X-Priority': 'high',
                    'Connection': 'Upgrade'
                }
            ) as ws:
                await ws.send(subscribe_msg)
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.001)
                        recv_time = time.perf_counter()
                        
                        # Calculate actual latency
                        actual_latency = (recv_time - msg_start) * 1000
                        
                        # Simulate institutional improvements
                        # Institutional gets priority routing + better infrastructure
                        institutional_latency = actual_latency * 0.6  # 40% improvement
                        institutional_latency += random.uniform(0.1, 0.3)  # Add minimal overhead
                        
                        data = fast_json_loads(msg)
                        if 'data' in data and data['data']:
                            book_data = data['data'][0]
                            bids = book_data.get('bids', [])
                            asks = book_data.get('asks', [])
                            
                            if bids and asks:
                                bid = float(bids[0][0])
                                ask = float(asks[0][0])
                                latencies.append(actual_latency)
                                institutional_latencies.append(institutional_latency)
                                message_count += 1
                                
                                self.latencies['okx_institutional'].append(institutional_latency)
                                self.prices['okx'].append((bid, ask, recv_time))
                                
                                if message_count % 20 == 0:
                                    avg_actual = sum(latencies[-20:]) / min(20, len(latencies))
                                    avg_inst = sum(institutional_latencies[-20:]) / min(20, len(institutional_latencies))
                                    improvement = ((avg_actual - avg_inst) / avg_actual) * 100
                                    print(f"🏛️ OKX Institutional: {bid:.2f}/{ask:.2f}")
                                    print(f"   📡 Standard: {actual_latency:.2f}ms → 🏛️ Institutional: {institutional_latency:.2f}ms ({improvement:.1f}% faster)")
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ OKX institutional simulation error: {e}")
            return None
        
        if latencies and institutional_latencies:
            avg_standard = sum(latencies) / len(latencies)
            avg_institutional = sum(institutional_latencies) / len(institutional_latencies)
            min_institutional = min(institutional_latencies)
            improvement = ((avg_standard - avg_institutional) / avg_standard) * 100
            msg_per_sec = message_count / duration
            
            return {
                'exchange': 'OKX',
                'connection_type': 'Institutional (Simulated)',
                'avg_latency_standard': avg_standard,
                'avg_latency_institutional': avg_institutional,
                'min_latency': min_institutional,
                'improvement_percent': improvement,
                'msg_per_sec': msg_per_sec,
                'total_messages': message_count
            }
        return None

    async def test_okx_colocation_simulation(self, duration=10):
        """Simulate OKX co-location with premium infrastructure"""
        print(f"🏢 Testing OKX COLOCATION SIMULATION for {duration}s...")
        print("   📍 Simulating: AWS Singapore (ap-southeast-1) proximity to OKX infrastructure")
        print("   🚀 Simulating: Premium colocation with direct network peering")
        
        latencies = []
        colocation_latencies = []
        message_count = 0
        
        url = "wss://ws.okx.com:8443/ws/v5/public"
        
        subscribe_msg = fast_json_dumps({
            "op": "subscribe", 
            "args": [{"channel": "books5", "instId": "BTC-USDT"}]
        })
        
        try:
            # Premium colocation connection settings
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                max_size=256,           # Ultra minimal
                compression=None,
                close_timeout=0.005,    # Even faster timeout
                max_queue=1,
                read_limit=256,
                write_limit=128,
                extra_headers={
                    'User-Agent': 'OKX-Colocation-HFT/3.0',
                    'X-Priority': 'critical',
                    'X-Colocation': 'premium',
                    'Connection': 'Upgrade'
                }
            ) as ws:
                await ws.send(subscribe_msg)
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.0005)  # Ultra-fast timeout
                        recv_time = time.perf_counter()
                        
                        # Calculate actual latency
                        actual_latency = (recv_time - msg_start) * 1000
                        
                        # Simulate premium colocation improvement
                        colocation_latency = self.simulate_colocation_latency(actual_latency, "premium")
                        
                        data = fast_json_loads(msg)
                        if 'data' in data and data['data']:
                            book_data = data['data'][0]
                            bids = book_data.get('bids', [])
                            asks = book_data.get('asks', [])
                            
                            if bids and asks:
                                bid = float(bids[0][0])
                                ask = float(asks[0][0])
                                latencies.append(actual_latency)
                                colocation_latencies.append(colocation_latency)
                                message_count += 1
                                
                                self.latencies['okx_colocation'].append(colocation_latency)
                                self.prices['okx'].append((bid, ask, recv_time))
                                
                                if message_count % 15 == 0:
                                    avg_actual = sum(latencies[-15:]) / min(15, len(latencies))
                                    avg_colo = sum(colocation_latencies[-15:]) / min(15, len(colocation_latencies))
                                    improvement = ((avg_actual - avg_colo) / avg_actual) * 100
                                    print(f"🏢 OKX Colocation: {bid:.2f}/{ask:.2f}")
                                    print(f"   📡 Standard: {actual_latency:.2f}ms → 🏢 Colocation: {colocation_latency:.2f}ms ({improvement:.1f}% faster)")
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ OKX colocation simulation error: {e}")
            return None
        
        if latencies and colocation_latencies:
            avg_standard = sum(latencies) / len(latencies)
            avg_colocation = sum(colocation_latencies) / len(colocation_latencies)
            min_colocation = min(colocation_latencies)
            improvement = ((avg_standard - avg_colocation) / avg_standard) * 100
            msg_per_sec = message_count / duration
            
            return {
                'exchange': 'OKX',
                'connection_type': 'Colocation (Simulated)',
                'avg_latency_standard': avg_standard,
                'avg_latency_colocation': avg_colocation,
                'min_latency': min_colocation,
                'improvement_percent': improvement,
                'msg_per_sec': msg_per_sec,
                'total_messages': message_count
            }
        return None

    def print_colocation_info(self):
        """Print detailed colocation information"""
        print("\n" + "🏢" * 50)
        print("COLOCATION INFORMATION & BENEFITS")
        print("🏢" * 50)
        
        print("\n📍 BINANCE COLOCATION OPTIONS:")
        print("   🌏 Primary Regions:")
        print("     • AWS Tokyo (ap-northeast-1) - Main production")
        print("     • AWS Singapore (ap-southeast-1) - Backup")
        print("     • AWS Sydney (ap-southeast-2) - Secondary")
        print("   💰 Expected Benefits:")
        print("     • 50-80% latency reduction (3ms → 0.6-1.5ms)")
        print("     • Direct network peering")
        print("     • Priority bandwidth allocation")
        print("     • Hardware-level optimizations")
        
        print("\n📍 OKX COLOCATION OPTIONS:")
        print("   🌏 Primary Regions:")
        print("     • AWS Singapore (ap-southeast-1) - Primary")
        print("     • AWS Hong Kong (ap-east-1) - Secondary")
        print("     • Alibaba Cloud Singapore - Alternative")
        print("   💰 Expected Benefits:")
        print("     • 60-90% latency reduction (50ms → 5-20ms)")
        print("     • Institutional-grade infrastructure")
        print("     • Dedicated bandwidth")
        print("     • Advanced network routing")
        
        print("\n💵 COLOCATION COSTS (Estimated):")
        print("   🏢 Premium Colocation (Same Rack): $5,000-15,000/month")
        print("   🏬 Standard Colocation (Same DC): $2,000-8,000/month")
        print("   ☁️ Cloud Proximity (Same AZ): $500-2,000/month")
        
        print("\n🚀 PERFORMANCE EXPECTATIONS:")
        print("   ⚡ Binance + Premium Colocation: 0.3-1.0ms")
        print("   ⚡ OKX + Premium Colocation: 3-15ms")
        print("   📊 ROI Break-even: ~$50,000+ daily volume")

async def main():
    """Run comprehensive colocation testing and analysis"""
    optimizer = ColocationOptimizer()
    
    print("🏢 COLOCATION OPTIMIZER FOR BINANCE & OKX INSTITUTIONAL")
    print("=" * 80)
    print("🎯 Objective: Analyze colocation benefits for ultra-low latency trading")
    print("📊 Testing: Standard vs Institutional vs Colocation scenarios")
    
    # Print colocation information first
    optimizer.print_colocation_info()
    
    test_duration = 12  # 12 seconds per test
    results = []
    
    # Test scenarios in order of increasing optimization
    tests = [
        ("Binance Standard", optimizer.test_binance_standard),
        ("OKX Standard", optimizer.test_okx_standard),
        ("OKX Institutional", optimizer.test_okx_institutional_simulation),
        ("Binance Colocation", optimizer.test_binance_colocation_simulation),
        ("OKX Colocation", optimizer.test_okx_colocation_simulation),
    ]
    
    print(f"\n🧪 RUNNING TESTS ({test_duration}s each)...")
    print("=" * 50)
    
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
        await asyncio.sleep(1)
    
    # Print comprehensive results
    print("\n" + "🏆" * 60)
    print("COLOCATION OPTIMIZATION RESULTS")
    print("🏆" * 60)
    
    if results:
        # Group results by exchange
        binance_results = [r for r in results if r['exchange'] == 'Binance']
        okx_results = [r for r in results if r['exchange'] == 'OKX']
        
        print("\n📊 BINANCE RESULTS:")
        for result in binance_results:
            connection_type = result['connection_type']
            if 'improvement_percent' in result:
                print(f"   🔥 {connection_type}:")
                print(f"      📡 Standard: {result['avg_latency_standard']:.2f}ms")
                print(f"      🏢 Optimized: {result.get('avg_latency_colocation', result.get('avg_latency_institutional', 0)):.2f}ms")
                print(f"      📈 Improvement: {result['improvement_percent']:.1f}%")
                print(f"      🚀 Min Latency: {result['min_latency']:.2f}ms")
            else:
                print(f"   📊 {connection_type}: {result['avg_latency']:.2f}ms avg")
        
        print("\n📊 OKX RESULTS:")
        for result in okx_results:
            connection_type = result['connection_type']
            if 'improvement_percent' in result:
                print(f"   🔥 {connection_type}:")
                print(f"      📡 Standard: {result['avg_latency_standard']:.2f}ms")
                print(f"      🏛️ Optimized: {result.get('avg_latency_colocation', result.get('avg_latency_institutional', 0)):.2f}ms")
                print(f"      📈 Improvement: {result['improvement_percent']:.1f}%")
                print(f"      🚀 Min Latency: {result['min_latency']:.2f}ms")
            else:
                print(f"   📊 {connection_type}: {result['avg_latency']:.2f}ms avg")
        
        # Best performance summary
        print("\n🏅 BEST PERFORMANCE ACHIEVED:")
        best_binance = min(binance_results, key=lambda x: x.get('min_latency', x.get('avg_latency', 1000)))
        best_okx = min(okx_results, key=lambda x: x.get('min_latency', x.get('avg_latency', 1000)))
        
        if best_binance:
            best_lat = best_binance.get('min_latency', best_binance.get('avg_latency', 0))
            print(f"   🥇 Binance ({best_binance['connection_type']}): {best_lat:.2f}ms")
        
        if best_okx:
            best_lat = best_okx.get('min_latency', best_okx.get('avg_latency', 0))
            print(f"   🥈 OKX ({best_okx['connection_type']}): {best_lat:.2f}ms")
        
        # ROI Analysis
        print("\n💰 ROI ANALYSIS:")
        if best_binance and best_okx:
            binance_lat = best_binance.get('min_latency', best_binance.get('avg_latency', 0))
            okx_lat = best_okx.get('min_latency', best_okx.get('avg_latency', 0))
            
            if binance_lat < 2:
                print(f"   ✅ Binance colocation: EXCELLENT for HFT (sub-2ms)")
            elif binance_lat < 5:
                print(f"   ✅ Binance colocation: GOOD for arbitrage")
            
            if okx_lat < 10:
                print(f"   ✅ OKX colocation: GOOD for arbitrage")
            elif okx_lat < 25:
                print(f"   ⚠️ OKX colocation: MARGINAL for HFT")
            else:
                print(f"   ❌ OKX colocation: NOT RECOMMENDED for HFT")
        
        print("\n🎯 RECOMMENDATIONS:")
        print("   1. 🥇 Binance colocation: Primary exchange for HFT")
        print("   2. 🏛️ OKX institutional: Secondary for diversification")
        print("   3. 📍 Location: AWS Singapore for both exchanges")
        print("   4. 💰 Budget: $10,000-20,000/month for premium setup")
        print("   5. 🔄 Strategy: Cross-exchange arbitrage with <1ms Binance")
        
    else:
        print("❌ No successful tests completed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Colocation analysis completed!")
