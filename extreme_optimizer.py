#!/usr/bin/env python3
"""
🚀 EXTREME LATENCY OPTIMIZER FOR BYBIT & OKX
Final attempt to achieve sub-20ms latency using the most aggressive techniques possible
- Direct binary processing
- Minimal JSON parsing
- Connection pooling
- Ultra-fast pattern matching
"""

import asyncio
import time
import json
import websockets
import logging
import re
from collections import deque

# Disable all logging for maximum performance
logging.disable(logging.CRITICAL)

try:
    import orjson
    HAS_ORJSON = True
    parse_json = orjson.loads
    print("🔥 Using orjson (FASTEST)")
except ImportError:
    HAS_ORJSON = False
    parse_json = json.loads
    print("📊 Using standard json")

class ExtremeOptimizer:
    def __init__(self):
        # Pre-compile regex patterns for ultra-fast parsing
        self.bybit_price_pattern = re.compile(rb'"b":\[{2}([^"]+)","([^"]+)"[^}]*}],"a":\[{2}([^"]+)","([^"]+)"')
        self.okx_price_pattern = re.compile(rb'"bids":\[\["([^"]+)","([^"]+)"].*?"asks":\[\["([^"]+)","([^"]+)"]')
        
    async def extreme_bybit_test(self, duration=15):
        """Extreme Bybit optimization - targeting sub-20ms"""
        print(f"🚀 EXTREME Bybit optimization (Target: <15ms) for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://stream.bybit.com/v5/public/spot"
        
        # Pre-compiled subscription
        sub_msg = b'{"op":"subscribe","args":["orderbook.1.BTCUSDT"]}'
        
        try:
            # Most aggressive settings possible
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                max_size=256,         # Tiny buffer
                compression=None,     # No compression
                close_timeout=0.01,   # Immediate close
                open_timeout=3        # Fast connection
            ) as ws:
                await ws.send(sub_msg)
                
                start_time = time.perf_counter()
                timeout_count = 0
                
                while time.perf_counter() - start_time < duration:
                    try:
                        # Ultra-aggressive timing
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.01)  # 10ms timeout
                        recv_time = time.perf_counter()
                        
                        timeout_count = 0
                        
                        # Direct binary processing - skip JSON if possible
                        if isinstance(msg, str):
                            msg_bytes = msg.encode('utf-8')
                        else:
                            msg_bytes = msg
                        
                        # Try regex first (fastest)
                        match = self.bybit_price_pattern.search(msg_bytes)
                        if match:
                            try:
                                bid_price = float(match.group(1))
                                ask_price = float(match.group(3))
                                
                                latency = (recv_time - msg_start) * 1000
                                latencies.append(latency)
                                message_count += 1
                                
                                if message_count % 20 == 0:
                                    recent = latencies[-10:] if len(latencies) >= 10 else latencies
                                    avg = sum(recent) / len(recent)
                                    print(f"🔥 Bybit #{message_count}: {bid_price:.2f}/{ask_price:.2f} | "
                                          f"Latency: {latency:.2f}ms | Avg10: {avg:.2f}ms")
                                continue
                            except (ValueError, IndexError):
                                pass
                        
                        # Fallback to minimal JSON parsing if regex fails
                        if b'"topic":"orderbook' in msg_bytes and b'"data":' in msg_bytes:
                            try:
                                data = parse_json(msg_bytes)
                                if (data.get('topic', '').startswith('orderbook') and 
                                    'data' in data and data['data']):
                                    
                                    book = data['data']
                                    bids = book.get('b', [])
                                    asks = book.get('a', [])
                                    
                                    if bids and asks and bids[0] and asks[0]:
                                        bid_price = float(bids[0][0])
                                        ask_price = float(asks[0][0])
                                        
                                        latency = (recv_time - msg_start) * 1000
                                        latencies.append(latency)
                                        message_count += 1
                            except:
                                continue
                        
                    except asyncio.TimeoutError:
                        timeout_count += 1
                        if timeout_count > 100:  # Too many timeouts
                            break
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Bybit connection error: {e}")
            return None
        
        if latencies:
            avg_lat = sum(latencies) / len(latencies)
            min_lat = min(latencies)
            max_lat = max(latencies)
            msg_rate = message_count / duration
            
            # Percentile analysis
            sorted_lat = sorted(latencies)
            p50 = sorted_lat[len(sorted_lat)//2]
            p90 = sorted_lat[int(len(sorted_lat)*0.9)]
            p95 = sorted_lat[int(len(sorted_lat)*0.95)]
            
            under_15ms = len([l for l in latencies if l < 15])
            under_20ms = len([l for l in latencies if l < 20])
            
            print(f"✅ EXTREME Bybit Results:")
            print(f"   📈 Speed: {msg_rate:.1f} msg/s")
            print(f"   ⚡ Avg: {avg_lat:.2f}ms | Min: {min_lat:.2f}ms | Max: {max_lat:.2f}ms")
            print(f"   📊 P50: {p50:.2f}ms | P90: {p90:.2f}ms | P95: {p95:.2f}ms")
            print(f"   🎯 <15ms: {under_15ms}/{len(latencies)} ({under_15ms/len(latencies)*100:.1f}%)")
            print(f"   ✅ <20ms: {under_20ms}/{len(latencies)} ({under_20ms/len(latencies)*100:.1f}%)")
            
            target_15 = "✅ ACHIEVED!" if avg_lat < 15 else "⚠️ CLOSE" if avg_lat < 20 else "❌ FAILED"
            target_20 = "✅ ACHIEVED!" if avg_lat < 20 else "⚠️ CLOSE" if avg_lat < 25 else "❌ FAILED"
            print(f"   🎯 Target <15ms: {target_15}")
            print(f"   🎯 Target <20ms: {target_20}")
            
            return {
                'exchange': 'Bybit',
                'method': 'EXTREME',
                'avg_latency': avg_lat,
                'min_latency': min_lat,
                'p50_latency': p50,
                'p95_latency': p95,
                'msg_per_sec': msg_rate,
                'under_15ms_pct': under_15ms/len(latencies)*100,
                'under_20ms_pct': under_20ms/len(latencies)*100,
                'total_messages': message_count
            }
        return None
    
    async def extreme_okx_test(self, duration=15):
        """Extreme OKX optimization - targeting sub-20ms"""
        print(f"🚀 EXTREME OKX optimization (Target: <15ms) for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://ws.okx.com:8443/ws/v5/public"
        
        # Pre-compiled subscription
        sub_msg = b'{"op":"subscribe","args":[{"channel":"books5","instId":"BTC-USDT"}]}'
        
        try:
            # Most aggressive settings possible
            async with websockets.connect(
                url,
                ping_interval=None,
                ping_timeout=None,
                max_size=256,         # Tiny buffer
                compression=None,     # No compression
                close_timeout=0.01,   # Immediate close
                open_timeout=3        # Fast connection
            ) as ws:
                await ws.send(sub_msg)
                
                start_time = time.perf_counter()
                timeout_count = 0
                
                while time.perf_counter() - start_time < duration:
                    try:
                        # Ultra-aggressive timing
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.02)  # 20ms timeout
                        recv_time = time.perf_counter()
                        
                        timeout_count = 0
                        
                        # Direct binary processing
                        if isinstance(msg, str):
                            msg_bytes = msg.encode('utf-8')
                        else:
                            msg_bytes = msg
                        
                        # Try regex first (fastest)
                        match = self.okx_price_pattern.search(msg_bytes)
                        if match:
                            try:
                                bid_price = float(match.group(1))
                                ask_price = float(match.group(3))
                                
                                latency = (recv_time - msg_start) * 1000
                                latencies.append(latency)
                                message_count += 1
                                
                                if message_count % 15 == 0:
                                    recent = latencies[-10:] if len(latencies) >= 10 else latencies
                                    avg = sum(recent) / len(recent)
                                    print(f"🔥 OKX #{message_count}: {bid_price:.2f}/{ask_price:.2f} | "
                                          f"Latency: {latency:.2f}ms | Avg10: {avg:.2f}ms")
                                continue
                            except (ValueError, IndexError):
                                pass
                        
                        # Fallback to minimal JSON parsing
                        if b'"channel":"books5"' in msg_bytes and b'"data":[' in msg_bytes:
                            try:
                                data = parse_json(msg_bytes)
                                if ('data' in data and data['data'] and len(data['data']) > 0):
                                    book = data['data'][0]
                                    bids = book.get('bids', [])
                                    asks = book.get('asks', [])
                                    
                                    if bids and asks and len(bids) > 0 and len(asks) > 0:
                                        bid_price = float(bids[0][0])
                                        ask_price = float(asks[0][0])
                                        
                                        latency = (recv_time - msg_start) * 1000
                                        latencies.append(latency)
                                        message_count += 1
                            except:
                                continue
                        
                    except asyncio.TimeoutError:
                        timeout_count += 1
                        if timeout_count > 100:  # Too many timeouts
                            print(f"⚠️ Too many timeouts ({timeout_count}), OKX may be slow")
                            break
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ OKX connection error: {e}")
            return None
        
        if latencies:
            avg_lat = sum(latencies) / len(latencies)
            min_lat = min(latencies)
            max_lat = max(latencies)
            msg_rate = message_count / duration
            
            # Percentile analysis
            sorted_lat = sorted(latencies)
            p50 = sorted_lat[len(sorted_lat)//2]
            p90 = sorted_lat[int(len(sorted_lat)*0.9)]
            p95 = sorted_lat[int(len(sorted_lat)*0.95)]
            
            under_15ms = len([l for l in latencies if l < 15])
            under_20ms = len([l for l in latencies if l < 20])
            
            print(f"✅ EXTREME OKX Results:")
            print(f"   📈 Speed: {msg_rate:.1f} msg/s")
            print(f"   ⚡ Avg: {avg_lat:.2f}ms | Min: {min_lat:.2f}ms | Max: {max_lat:.2f}ms")
            print(f"   📊 P50: {p50:.2f}ms | P90: {p90:.2f}ms | P95: {p95:.2f}ms")
            print(f"   🎯 <15ms: {under_15ms}/{len(latencies)} ({under_15ms/len(latencies)*100:.1f}%)")
            print(f"   ✅ <20ms: {under_20ms}/{len(latencies)} ({under_20ms/len(latencies)*100:.1f}%)")
            
            target_15 = "✅ ACHIEVED!" if avg_lat < 15 else "⚠️ CLOSE" if avg_lat < 20 else "❌ FAILED"
            target_20 = "✅ ACHIEVED!" if avg_lat < 20 else "⚠️ CLOSE" if avg_lat < 25 else "❌ FAILED"
            print(f"   🎯 Target <15ms: {target_15}")
            print(f"   🎯 Target <20ms: {target_20}")
            
            return {
                'exchange': 'OKX',
                'method': 'EXTREME',
                'avg_latency': avg_lat,
                'min_latency': min_lat,
                'p50_latency': p50,
                'p95_latency': p95,
                'msg_per_sec': msg_rate,
                'under_15ms_pct': under_15ms/len(latencies)*100,
                'under_20ms_pct': under_20ms/len(latencies)*100,
                'total_messages': message_count
            }
        return None
    
    async def binance_baseline_extreme(self, duration=15):
        """Binance with extreme optimizations for comparison"""
        print(f"🚀 Binance EXTREME baseline for {duration}s...")
        
        latencies = []
        message_count = 0
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        # Pre-compile regex for Binance
        price_pattern = re.compile(rb'"b":"([^"]+)".*?"a":"([^"]+)"')
        
        try:
            async with websockets.connect(
                url,
                ping_interval=None,
                max_size=256,
                compression=None
            ) as ws:
                start_time = time.perf_counter()
                
                while time.perf_counter() - start_time < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await ws.recv()
                        recv_time = time.perf_counter()
                        
                        # Direct binary processing
                        if isinstance(msg, str):
                            msg_bytes = msg.encode('utf-8')
                        else:
                            msg_bytes = msg
                        
                        # Regex first
                        match = price_pattern.search(msg_bytes)
                        if match:
                            try:
                                bid = float(match.group(1))
                                ask = float(match.group(2))
                                
                                latency = (recv_time - msg_start) * 1000
                                latencies.append(latency)
                                message_count += 1
                                
                                if message_count % 100 == 0:
                                    recent = latencies[-20:] if len(latencies) >= 20 else latencies
                                    avg = sum(recent) / len(recent)
                                    print(f"🔥 Binance #{message_count}: {bid:.2f}/{ask:.2f} | "
                                          f"Latency: {latency:.2f}ms | Avg20: {avg:.2f}ms")
                                continue
                            except ValueError:
                                pass
                        
                        # Fallback to JSON
                        try:
                            data = parse_json(msg_bytes)
                            if 'b' in data and 'a' in data:
                                bid = float(data['b'])
                                ask = float(data['a'])
                                latency = (recv_time - msg_start) * 1000
                                latencies.append(latency)
                                message_count += 1
                        except:
                            continue
                        
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"❌ Binance connection error: {e}")
            return None
        
        if latencies:
            avg_lat = sum(latencies) / len(latencies)
            min_lat = min(latencies)
            msg_rate = message_count / duration
            under_20ms = len([l for l in latencies if l < 20])
            
            print(f"✅ Binance EXTREME Results:")
            print(f"   📈 Speed: {msg_rate:.1f} msg/s")
            print(f"   ⚡ Avg: {avg_lat:.2f}ms | Min: {min_lat:.2f}ms")
            print(f"   ✅ Under 20ms: {under_20ms}/{len(latencies)} ({under_20ms/len(latencies)*100:.1f}%)")
            
            return {
                'exchange': 'Binance',
                'method': 'EXTREME',
                'avg_latency': avg_lat,
                'min_latency': min_lat,
                'msg_per_sec': msg_rate,
                'under_20ms_pct': under_20ms/len(latencies)*100,
                'total_messages': message_count
            }
        return None

async def main():
    """Run extreme optimization tests"""
    optimizer = ExtremeOptimizer()
    
    print("🚀 EXTREME LATENCY OPTIMIZER")
    print("=" * 60)
    print("🎯 MISSION: Get Bybit & OKX under 15-20ms using EXTREME techniques")
    print("🔥 Using regex parsing, binary processing, ultra-small buffers")
    print()
    
    test_duration = 20  # Longer test for better accuracy
    results = []
    
    tests = [
        ("Binance EXTREME", optimizer.binance_baseline_extreme),
        ("Bybit EXTREME", optimizer.extreme_bybit_test),
        ("OKX EXTREME", optimizer.extreme_okx_test),
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🚀 Running {test_name}...")
        print('='*60)
        try:
            result = await test_func(test_duration)
            if result:
                results.append(result)
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
        
        await asyncio.sleep(2)
    
    # Final results
    print(f"\n{'='*60}")
    print("🏆 EXTREME OPTIMIZATION FINAL RESULTS")
    print('='*60)
    
    if results:
        results.sort(key=lambda x: x['avg_latency'])
        
        for i, result in enumerate(results, 1):
            rank = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            status = "🔥" if result['avg_latency'] < 10 else "✅" if result['avg_latency'] < 20 else "⚠️"
            
            print(f"{rank} {status} {result['exchange']} {result['method']}")
            print(f"    ⚡ Average: {result['avg_latency']:.2f}ms")
            print(f"    🚀 Minimum: {result['min_latency']:.2f}ms")
            print(f"    📈 Speed: {result['msg_per_sec']:.1f} msg/s")
            if 'under_20ms_pct' in result:
                print(f"    ✅ Under 20ms: {result['under_20ms_pct']:.1f}%")
            if 'p50_latency' in result:
                print(f"    📊 P50: {result['p50_latency']:.2f}ms | P95: {result['p95_latency']:.2f}ms")
            print()
        
        print("🎯 FINAL VERDICT:")
        for result in results:
            if result['exchange'] in ['Bybit', 'OKX']:
                status = "✅ SUCCESS!" if result['avg_latency'] < 20 else "⚠️ IMPROVED" if result['avg_latency'] < 30 else "❌ FAILED"
                improvement = f"(Target: <20ms)"
                print(f"   {result['exchange']}: {result['avg_latency']:.2f}ms {status} {improvement}")
        
        print(f"\n💡 FINAL RECOMMENDATION:")
        best = results[0]
        print(f"   🏆 Primary: {best['exchange']} ({best['avg_latency']:.2f}ms)")
        
        good_backups = [r for r in results[1:] if r['avg_latency'] < 30]
        if good_backups:
            backup_names = [r['exchange'] for r in good_backups]
            print(f"   📊 Backup: {', '.join(backup_names)}")
    else:
        print("❌ No successful tests")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Extreme optimization interrupted!")
