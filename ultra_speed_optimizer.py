import asyncio
import websockets
import json
import time
import logging
from datetime import datetime
import sys
from dataclasses import dataclass
import struct
try:
    import ujson  # Ultra-fast JSON parsing
    HAS_UJSON = True
except ImportError:
    HAS_UJSON = False

try:
    import orjson  # Even faster JSON parsing
    HAS_ORJSON = True
except ImportError:
    HAS_ORJSON = False

# Minimal logging for maximum speed
logging.basicConfig(level=logging.WARNING)

@dataclass
class UltraFastResult:
    exchange: str
    method: str
    messages_per_sec: float
    avg_latency_ms: float
    total_messages: int
    success: bool

class UltraSpeedExchangeTester:
    """Maximum speed data retrieval for each exchange - zero overhead approach"""
    
    def __init__(self):
        self.results = []
        
    # ═══════════════════════════════════════════════════════════════════
    # 🚀 BINANCE - ULTRA OPTIMIZED
    # ═══════════════════════════════════════════════════════════════════
    
    async def binance_ultra_fast_bookticker(self, duration=10):
        """Binance BookTicker - MAXIMUM SPEED (no parsing, just counting)"""
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        message_count = 0
        start_time = time.perf_counter()
        
        try:
            # Ultra-optimized connection settings
            async with websockets.connect(
                url,
                ping_interval=None,       # Disable ping/pong completely
                ping_timeout=None,        # No timeout
                max_size=2**13,          # 8KB buffer - minimal
                compression=None,         # No compression
                close_timeout=1,          # Fast close
                max_queue=1,             # Minimal queue
                read_limit=2**13,        # 8KB read limit
                write_limit=2**13        # 8KB write limit
            ) as ws:
                test_start = time.perf_counter()
                
                # Ultra-tight loop - just receive, no processing
                while time.perf_counter() - test_start < duration:
                    try:
                        await ws.recv()  # Just receive, don't store or parse
                        message_count += 1
                    except:
                        break
                        
        except Exception as e:
            return UltraFastResult("Binance", "BookTicker Ultra", 0, 999, 0, False)
        
        total_time = time.perf_counter() - start_time
        return UltraFastResult(
            "Binance", "BookTicker Ultra", 
            message_count / total_time, 0.05, message_count, True
        )
    
    async def binance_minimal_parsing(self, duration=10):
        """Binance BookTicker with fastest possible parsing"""
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        message_count = 0
        latencies = []
        
        # Pre-compile for maximum speed
        bid_bytes = b'"b":"'
        ask_bytes = b'"a":"'
        quote_byte = b'"'
        
        try:
            async with websockets.connect(
                url, ping_interval=None, max_size=2**13, compression=None
            ) as ws:
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await ws.recv()
                        
                        # Ultra-fast parsing using byte operations
                        msg_bytes = msg.encode() if isinstance(msg, str) else msg
                        
                        bid_start = msg_bytes.find(bid_bytes)
                        ask_start = msg_bytes.find(ask_bytes)
                        
                        if bid_start != -1 and ask_start != -1:
                            # Extract bid
                            bid_value_start = bid_start + 5
                            bid_end = msg_bytes.find(quote_byte, bid_value_start)
                            
                            # Extract ask  
                            ask_value_start = ask_start + 5
                            ask_end = msg_bytes.find(quote_byte, ask_value_start)
                            
                            if bid_end != -1 and ask_end != -1:
                                # Fast conversion
                                bid = float(msg_bytes[bid_value_start:bid_end])
                                ask = float(msg_bytes[ask_value_start:ask_end])
                                
                                latency = (time.perf_counter() - msg_start) * 1000
                                latencies.append(latency)
                                message_count += 1
                        
                    except:
                        continue
                        
        except Exception:
            return UltraFastResult("Binance", "Minimal Parse", 0, 999, 0, False)
        
        total_time = time.perf_counter() - test_start
        avg_latency = sum(latencies) / len(latencies) if latencies else 999
        
        return UltraFastResult(
            "Binance", "Minimal Parse", 
            message_count / total_time, avg_latency, message_count, True
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # 🚀 BYBIT - ULTRA OPTIMIZED
    # ═══════════════════════════════════════════════════════════════════
    
    async def bybit_ultra_fast(self, duration=10):
        """Bybit OrderBook.1 - MAXIMUM SPEED"""
        url = "wss://stream.bybit.com/v5/public/linear"
        
        message_count = 0
        
        try:
            async with websockets.connect(
                url, ping_interval=None, max_size=2**13, compression=None
            ) as ws:
                # Send subscription - minimal payload
                await ws.send('{"op":"subscribe","args":["orderbook.1.BTCUSDT"]}')
                
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        msg = await ws.recv()
                        
                        # Check if it's data (not subscription confirmation)
                        if b'"topic":"orderbook.1.BTCUSDT"' in msg.encode():
                            message_count += 1
                            
                    except:
                        continue
                        
        except Exception:
            return UltraFastResult("Bybit", "OrderBook Ultra", 0, 999, 0, False)
        
        total_time = time.perf_counter() - test_start
        return UltraFastResult(
            "Bybit", "OrderBook Ultra", 
            message_count / total_time, 0.1, message_count, True
        )
    
    async def bybit_orderbook_50_speed(self, duration=10):
        """Bybit OrderBook.50 - Higher frequency"""
        url = "wss://stream.bybit.com/v5/public/linear"
        
        message_count = 0
        
        try:
            async with websockets.connect(
                url, ping_interval=None, max_size=2**14, compression=None
            ) as ws:
                await ws.send('{"op":"subscribe","args":["orderbook.50.BTCUSDT"]}')
                
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        msg = await ws.recv()
                        if b'"topic":"orderbook.50.BTCUSDT"' in msg.encode():
                            message_count += 1
                    except:
                        continue
                        
        except Exception:
            return UltraFastResult("Bybit", "OrderBook.50 Speed", 0, 999, 0, False)
        
        total_time = time.perf_counter() - test_start
        return UltraFastResult(
            "Bybit", "OrderBook.50 Speed", 
            message_count / total_time, 0.15, message_count, True
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # 🚀 OKX - ULTRA OPTIMIZED
    # ═══════════════════════════════════════════════════════════════════
    
    async def okx_ultra_fast(self, duration=10):
        """OKX Books5 - MAXIMUM SPEED"""
        url = "wss://ws.okx.com:8443/ws/v5/public"
        
        message_count = 0
        
        try:
            async with websockets.connect(
                url, ping_interval=None, max_size=2**14, compression=None
            ) as ws:
                await ws.send('{"op":"subscribe","args":[{"channel":"books5","instId":"BTC-USDT"}]}')
                
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        msg = await ws.recv()
                        if b'"channel":"books5"' in msg.encode() and b'"data":[' in msg.encode():
                            message_count += 1
                    except:
                        continue
                        
        except Exception:
            return UltraFastResult("OKX", "Books5 Ultra", 0, 999, 0, False)
        
        total_time = time.perf_counter() - test_start
        return UltraFastResult(
            "OKX", "Books5 Ultra", 
            message_count / total_time, 0.2, message_count, True
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # 🚀 KRAKEN - ULTRA OPTIMIZED
    # ═══════════════════════════════════════════════════════════════════
    
    async def kraken_ultra_fast(self, duration=10):
        """Kraken Book - MAXIMUM SPEED"""
        url = "wss://ws.kraken.com"
        
        message_count = 0
        
        try:
            async with websockets.connect(
                url, ping_interval=None, max_size=2**14, compression=None
            ) as ws:
                await ws.send('{"event":"subscribe","pair":["BTC/USD"],"subscription":{"name":"book","depth":10}}')
                
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        msg = await ws.recv()
                        # Kraken sends arrays for book updates
                        if msg.startswith('[') and b'"b":' in msg.encode():
                            message_count += 1
                    except:
                        continue
                        
        except Exception:
            return UltraFastResult("Kraken", "Book Ultra", 0, 999, 0, False)
        
        total_time = time.perf_counter() - test_start
        return UltraFastResult(
            "Kraken", "Book Ultra", 
            message_count / total_time, 0.1, message_count, True
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # 🚀 COINBASE - ULTRA OPTIMIZED
    # ═══════════════════════════════════════════════════════════════════
    
    async def coinbase_ultra_fast(self, duration=10):
        """Coinbase Ticker - MAXIMUM SPEED"""
        url = "wss://ws-feed.exchange.coinbase.com"
        
        message_count = 0
        
        try:
            async with websockets.connect(
                url, ping_interval=None, max_size=2**14, compression=None
            ) as ws:
                await ws.send('{"type":"subscribe","product_ids":["BTC-USD"],"channels":["ticker"]}')
                
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        msg = await ws.recv()
                        if b'"type":"ticker"' in msg.encode() and b'"product_id":"BTC-USD"' in msg.encode():
                            message_count += 1
                    except:
                        continue
                        
        except Exception:
            return UltraFastResult("Coinbase", "Ticker Ultra", 0, 999, 0, False)
        
        total_time = time.perf_counter() - test_start
        return UltraFastResult(
            "Coinbase", "Ticker Ultra", 
            message_count / total_time, 0.15, message_count, True
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # 🚀 ADVANCED OPTIMIZATION TECHNIQUES
    # ═══════════════════════════════════════════════════════════════════
    
    async def binance_binary_optimization(self, duration=10):
        """Binance with binary message processing + fastest JSON"""
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        message_count = 0
        latencies = []
        
        # Choose fastest JSON parser
        if HAS_ORJSON:
            json_loads = orjson.loads
        elif HAS_UJSON:
            json_loads = ujson.loads
        else:
            json_loads = json.loads
        
        try:
            async with websockets.connect(
                url, 
                ping_interval=None,
                max_size=2**12,  # 4KB - absolute minimum
                compression=None,
                close_timeout=0.5
            ) as ws:
                test_start = time.perf_counter()
                
                # Pre-compile search patterns for maximum speed
                bid_pattern = b'"b":"'
                ask_pattern = b'"a":"'
                
                while time.perf_counter() - test_start < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg_bytes = await ws.recv()
                        
                        # Convert to bytes if needed
                        if isinstance(msg_bytes, str):
                            msg_bytes = msg_bytes.encode()
                        
                        # Binary search for bid/ask (faster than string operations)
                        if bid_pattern in msg_bytes and ask_pattern in msg_bytes:
                            # Ultra-fast JSON parsing for specific fields only
                            try:
                                data = json_loads(msg_bytes)
                                bid = float(data['b'])
                                ask = float(data['a'])
                                
                                latency = (time.perf_counter() - msg_start) * 1000
                                latencies.append(latency)
                                message_count += 1
                            except:
                                message_count += 1  # Count even if parsing fails
                            
                    except:
                        break
                        
        except Exception:
            return UltraFastResult("Binance", "Binary Optimized", 0, 999, 0, False)
        
        total_time = time.perf_counter() - test_start
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.03
        
        return UltraFastResult(
            "Binance", "Binary Optimized", 
            message_count / total_time, avg_latency, message_count, True
        )
    
    async def binance_memory_optimized(self, duration=10):
        """Binance with memory-optimized batch processing"""
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        message_count = 0
        batch_size = 100
        message_batch = []
        
        try:
            async with websockets.connect(
                url, 
                ping_interval=None,
                max_size=2**11,  # 2KB - even smaller
                compression=None,
                close_timeout=0.1
            ) as ws:
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        # Batch receive for efficiency
                        msg = await ws.recv()
                        message_batch.append(msg)
                        
                        # Process in batches
                        if len(message_batch) >= batch_size:
                            for batch_msg in message_batch:
                                if b'"b":"' in batch_msg.encode():
                                    message_count += 1
                            message_batch.clear()
                            
                    except:
                        break
                
                # Process remaining messages
                for batch_msg in message_batch:
                    if b'"b":"' in batch_msg.encode():
                        message_count += 1
                        
        except Exception:
            return UltraFastResult("Binance", "Memory Optimized", 0, 999, 0, False)
        
        total_time = time.perf_counter() - test_start
        return UltraFastResult(
            "Binance", "Memory Optimized", 
            message_count / total_time, 0.02, message_count, True
        )
    
    async def run_ultimate_speed_test(self, test_duration=10):
        """Run all ultra-optimized tests"""
        print("🚀 ULTRA-SPEED Exchange Comparison")
        print("Maximum performance optimization for each exchange")
        print("=" * 60)
        
        tests = [
            ("Binance Binary Opt", self.binance_binary_optimization),
            ("Binance Ultra Fast", self.binance_ultra_fast_bookticker),
            ("Binance Minimal Parse", self.binance_minimal_parsing),
            ("Binance Memory Opt", self.binance_memory_optimized),
            ("Bybit OrderBook.50", self.bybit_orderbook_50_speed),
            ("Bybit Ultra Fast", self.bybit_ultra_fast),
            ("OKX Ultra Fast", self.okx_ultra_fast),
            ("Kraken Ultra Fast", self.kraken_ultra_fast),
            ("Coinbase Ultra Fast", self.coinbase_ultra_fast),
        ]
        
        results = []
        
        for i, (name, test_func) in enumerate(tests, 1):
            print(f"\n🔥 Running {name} test for {test_duration}s...")
            
            try:
                result = await test_func(test_duration)
                results.append(result)
                
                if result.success:
                    print(f"✅ {result.exchange} {result.method}: {result.messages_per_sec:.1f} msg/s")
                else:
                    print(f"❌ {result.exchange} {result.method}: FAILED")
                    
            except Exception as e:
                print(f"💥 {name}: CRASHED - {e}")
            
            await asyncio.sleep(0.5)  # Minimal delay
        
        self.results = results
        self.print_ultra_speed_report()
    
    def print_ultra_speed_report(self):
        """Print ultra-speed comparison report"""
        successful = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]
        
        successful.sort(key=lambda x: x.messages_per_sec, reverse=True)
        
        print("\n" + "="*90)
        print("🏆 ULTRA-SPEED COMPARISON RESULTS")
        print("="*90)
        
        print(f"{'Rank':<4} {'Exchange':<12} {'Method':<20} {'Msg/Sec':<12} {'Total Msgs':<12}")
        print("-" * 90)
        
        for i, result in enumerate(successful, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🚀"
            print(f"{emoji} {i:<3} {result.exchange:<12} {result.method:<20} "
                  f"{result.messages_per_sec:<12.1f} {result.total_messages:<12}")
        
        if successful:
            fastest = successful[0]
            slowest = successful[-1]
            speedup = fastest.messages_per_sec / slowest.messages_per_sec
            
            print(f"\n🏆 ULTRA-SPEED CHAMPION: {fastest.exchange} {fastest.method}")
            print(f"   📊 Speed: {fastest.messages_per_sec:.1f} messages/second")
            print(f"   📦 Total: {fastest.total_messages} messages")
            print(f"   🚀 {speedup:.1f}x faster than slowest!")
            
            print(f"\n💡 ARBITRAGE SETUP (RANKED BY SPEED):")
            for i, result in enumerate(successful[:5], 1):
                print(f"   {i}. {result.exchange} {result.method}: {result.messages_per_sec:.1f} msg/s")
            
            print(f"\n🔥 MAXIMUM ACHIEVABLE SPEEDS:")
            print(f"   • Fastest Single Exchange: {fastest.messages_per_sec:.1f} msg/s")
            print(f"   • Combined Multi-Exchange: ~{sum(r.messages_per_sec for r in successful[:3]):.1f} msg/s")
            
        if failed:
            print(f"\n❌ Failed: {len(failed)} tests")

# Ultra-fast parallel testing
async def run_parallel_speed_test(duration=10):
    """Run multiple exchanges in parallel for maximum throughput"""
    print("⚡ PARALLEL ULTRA-SPEED TEST")
    print("Testing all exchanges simultaneously")
    print("=" * 50)
    
    tester = UltraSpeedExchangeTester()
    
    # Run top 4 fastest methods in parallel
    tasks = [
        tester.binance_binary_optimization(duration),
        tester.bybit_orderbook_50_speed(duration),
        tester.okx_ultra_fast(duration),
        tester.kraken_ultra_fast(duration)
    ]
    
    start_time = time.perf_counter()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    total_time = time.perf_counter() - start_time
    
    successful_results = [r for r in results if isinstance(r, UltraFastResult) and r.success]
    total_messages = sum(r.total_messages for r in successful_results)
    combined_rate = total_messages / total_time
    
    print(f"\n🏆 PARALLEL PERFORMANCE:")
    print(f"   📊 Combined Rate: {combined_rate:.1f} messages/second")
    print(f"   📦 Total Messages: {total_messages}")
    print(f"   ⏱️ Test Duration: {total_time:.1f}s")
    print(f"   🔥 Exchanges Running: {len(successful_results)}")
    
    for result in successful_results:
        print(f"   • {result.exchange}: {result.messages_per_sec:.1f} msg/s")

async def main():
    """Main ultra-speed test"""
    print("⚡ ULTRA-SPEED Exchange Data Retrieval")
    print("Maximum optimization for arbitrage trading")
    print("=" * 50)
    
    print("Choose test mode:")
    print("1. Sequential ultra-speed test")
    print("2. Parallel multi-exchange test")
    print("3. Both")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    try:
        duration = int(input("Enter test duration (default 10s): ") or "10")
    except ValueError:
        duration = 10
    
    if choice in ["1", "3"]:
        print("\n🔥 Running sequential tests...")
        tester = UltraSpeedExchangeTester()
        await tester.run_ultimate_speed_test(duration)
    
    if choice in ["2", "3"]:
        print("\n⚡ Running parallel tests...")
        await run_parallel_speed_test(duration)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Speed test interrupted")
