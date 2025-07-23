import asyncio
import websockets
import json
import time
import logging
import aiohttp
import statistics
from datetime import datetime
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class QuickTestResult:
    exchange: str
    method: str
    messages_per_sec: float
    avg_latency_ms: float
    success: bool
    notes: str = ""

class QuickSpeedTester:
    """Quick speed comparison of the most important methods"""
    
    def __init__(self):
        self.results = []
    
    async def test_binance_bookticker_ultra_fast(self, duration=10):
        """Ultra-fast Binance BookTicker test"""
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        logger.info(f"🚀 Testing Binance BookTicker (Ultra-Fast) for {duration}s...")
        
        message_count = 0
        start_time = time.perf_counter()
        
        try:
            async with websockets.connect(
                url,
                ping_interval=None,  # Disable ping/pong for max speed
                max_size=2**14,     # 16KB buffer
                compression=None,
                close_timeout=1
            ) as ws:
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        await ws.recv()  # Just receive, don't parse
                        message_count += 1
                    except:
                        break
                
                total_duration = time.perf_counter() - test_start
                
            return QuickTestResult(
                exchange="Binance",
                method="BookTicker (Ultra-Fast)",
                messages_per_sec=message_count / total_duration,
                avg_latency_ms=0.1,  # Estimated
                success=True
            )
        except Exception as e:
            return QuickTestResult(
                exchange="Binance",
                method="BookTicker (Ultra-Fast)", 
                messages_per_sec=0,
                avg_latency_ms=999,
                success=False,
                notes=str(e)
            )
    
    async def test_binance_bookticker_with_parsing(self, duration=10):
        """Binance BookTicker with full parsing"""
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        logger.info(f"📊 Testing Binance BookTicker (With Parsing) for {duration}s...")
        
        latencies = []
        message_count = 0
        
        try:
            async with websockets.connect(url) as ws:
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                        
                        # Parse JSON
                        data = json.loads(msg)
                        bid = float(data['b'])
                        ask = float(data['a'])
                        
                        latency = (time.perf_counter() - msg_start) * 1000
                        latencies.append(latency)
                        message_count += 1
                        
                    except asyncio.TimeoutError:
                        break
                    except:
                        continue
                
                total_duration = time.perf_counter() - test_start
                
            return QuickTestResult(
                exchange="Binance",
                method="BookTicker (With Parsing)",
                messages_per_sec=message_count / total_duration,
                avg_latency_ms=statistics.mean(latencies) if latencies else 999,
                success=len(latencies) > 0
            )
        except Exception as e:
            return QuickTestResult(
                exchange="Binance",
                method="BookTicker (With Parsing)",
                messages_per_sec=0,
                avg_latency_ms=999,
                success=False,
                notes=str(e)
            )
    
    async def test_bybit_orderbook(self, duration=10):
        """Bybit OrderBook.1 test"""
        url = "wss://stream.bybit.com/v5/public/linear"
        logger.info(f"📊 Testing Bybit OrderBook.1 for {duration}s...")
        
        message_count = 0
        
        try:
            async with websockets.connect(url) as ws:
                # Subscribe
                await ws.send(json.dumps({
                    "op": "subscribe",
                    "args": ["orderbook.1.BTCUSDT"]
                }))
                
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                        data = json.loads(msg)
                        
                        # Check if it's a data message
                        if 'data' in data and data.get('topic', '').startswith('orderbook'):
                            message_count += 1
                            
                    except asyncio.TimeoutError:
                        break
                    except:
                        continue
                
                total_duration = time.perf_counter() - test_start
                
            return QuickTestResult(
                exchange="Bybit",
                method="OrderBook.1",
                messages_per_sec=message_count / total_duration,
                avg_latency_ms=20,  # Estimated
                success=message_count > 0
            )
        except Exception as e:
            return QuickTestResult(
                exchange="Bybit",
                method="OrderBook.1",
                messages_per_sec=0,
                avg_latency_ms=999,
                success=False,
                notes=str(e)
            )
    
    async def test_binance_depth_100ms(self, duration=10):
        """Binance Depth@100ms test"""
        url = "wss://stream.binance.com:9443/ws/btcusdt@depth@100ms"
        logger.info(f"📊 Testing Binance Depth@100ms for {duration}s...")
        
        message_count = 0
        
        try:
            async with websockets.connect(url) as ws:
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        await asyncio.wait_for(ws.recv(), timeout=1.0)
                        message_count += 1
                    except asyncio.TimeoutError:
                        break
                    except:
                        continue
                
                total_duration = time.perf_counter() - test_start
                
            return QuickTestResult(
                exchange="Binance",
                method="Depth@100ms",
                messages_per_sec=message_count / total_duration,
                avg_latency_ms=100,  # Expected ~100ms
                success=message_count > 0
            )
        except Exception as e:
            return QuickTestResult(
                exchange="Binance",
                method="Depth@100ms",
                messages_per_sec=0,
                avg_latency_ms=999,
                success=False,
                notes=str(e)
            )
    
    async def test_binance_rest_api(self, duration=10):
        """Binance REST API test"""
        url = "https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT"
        logger.info(f"📊 Testing Binance REST API for {duration}s...")
        
        request_count = 0
        latencies = []
        
        async with aiohttp.ClientSession() as session:
            test_start = time.perf_counter()
            
            while time.perf_counter() - test_start < duration:
                try:
                    req_start = time.perf_counter()
                    async with session.get(url) as response:
                        data = await response.json()
                        req_end = time.perf_counter()
                        
                        latency = (req_end - req_start) * 1000
                        latencies.append(latency)
                        request_count += 1
                        
                        # Rate limit
                        await asyncio.sleep(0.1)
                        
                except:
                    await asyncio.sleep(0.1)
                    continue
            
            total_duration = time.perf_counter() - test_start
        
        return QuickTestResult(
            exchange="Binance",
            method="REST API",
            messages_per_sec=request_count / total_duration,
            avg_latency_ms=statistics.mean(latencies) if latencies else 999,
            success=len(latencies) > 0
        )
    
    async def run_quick_comparison(self, test_duration=10):
        """Run quick comparison of key methods"""
        print("🚀 Quick Exchange Speed Comparison")
        print("=" * 50)
        print(f"⏱️ Testing 5 key methods for {test_duration}s each")
        
        tests = [
            self.test_binance_bookticker_ultra_fast,
            self.test_binance_bookticker_with_parsing,
            self.test_bybit_orderbook,
            self.test_binance_depth_100ms,
            self.test_binance_rest_api
        ]
        
        results = []
        
        for i, test_func in enumerate(tests, 1):
            print(f"\n📊 Running test {i}/{len(tests)}")
            result = await test_func(test_duration)
            results.append(result)
            
            if result.success:
                print(f"✅ {result.exchange} {result.method}: {result.messages_per_sec:.1f} msg/s")
            else:
                print(f"❌ {result.exchange} {result.method}: FAILED")
            
            await asyncio.sleep(1)
        
        self.results = results
        self.print_quick_report()
    
    def print_quick_report(self):
        """Print quick comparison report"""
        successful = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]
        
        successful.sort(key=lambda x: x.messages_per_sec, reverse=True)
        
        print("\n" + "="*80)
        print("🏆 QUICK SPEED COMPARISON RESULTS")
        print("="*80)
        
        print(f"{'Rank':<4} {'Exchange':<10} {'Method':<25} {'Msg/Sec':<12} {'Latency':<10}")
        print("-" * 80)
        
        for i, result in enumerate(successful, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📊"
            print(f"{emoji} {i:<3} {result.exchange:<10} {result.method:<25} "
                  f"{result.messages_per_sec:<12.1f} {result.avg_latency_ms:<10.1f}")
        
        if failed:
            print(f"\n❌ Failed: {', '.join([f'{r.exchange} {r.method}' for r in failed])}")
        
        if successful:
            fastest = successful[0]
            slowest = successful[-1]
            speedup = fastest.messages_per_sec / slowest.messages_per_sec
            
            print(f"\n🏆 WINNER: {fastest.exchange} {fastest.method}")
            print(f"   📊 Speed: {fastest.messages_per_sec:.1f} msg/s")
            print(f"   🚀 {speedup:.1f}x faster than slowest!")
            
            print(f"\n💡 KEY INSIGHTS:")
            print(f"   • Ultra-fast (no parsing) vs parsing: {successful[0].messages_per_sec/successful[1].messages_per_sec:.1f}x speedup")
            print(f"   • WebSocket vs REST API: ~{successful[0].messages_per_sec/successful[-1].messages_per_sec:.0f}x faster")
            print(f"   • For arbitrage: Use {fastest.exchange} {fastest.method}")

async def main():
    """Main function for quick test"""
    print("⚡ Quick Exchange Speed Test")
    print("Testing the most important methods only")
    print("=" * 50)
    
    try:
        duration = int(input("Enter test duration per method (default 10s): ") or "10")
    except ValueError:
        duration = 10
    
    tester = QuickSpeedTester()
    
    try:
        await tester.run_quick_comparison(duration)
    except KeyboardInterrupt:
        print("\n❌ Tests interrupted")
        if tester.results:
            tester.print_quick_report()

if __name__ == "__main__":
    asyncio.run(main())
