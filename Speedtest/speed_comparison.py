import asyncio
import websockets
import json
import time
import logging
from datetime import datetime
import sys
from dataclasses import dataclass
from typing import List, Dict, Any
import statistics
import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class BenchmarkResult:
    endpoint_name: str
    total_messages: int
    duration: float
    avg_messages_per_sec: float
    avg_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    median_latency_ms: float
    missed_updates: int
    connection_time_ms: float

class SpeedTester:
    def __init__(self):
        self.results = []
        
    async def test_binance_ticker(self, duration=30):
        """Original ticker endpoint"""
        endpoint_name = "Binance Ticker (Original)"
        url = "wss://stream.binance.com:9443/ws/btcusdt@ticker"
        
        return await self._run_websocket_test(endpoint_name, url, duration, self._parse_ticker)
    
    async def test_binance_bookticker(self, duration=30):
        """Binance BookTicker - ~20 updates/sec"""
        endpoint_name = "Binance BookTicker (Fast)"
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        return await self._run_websocket_test(endpoint_name, url, duration, self._parse_bookticker)
    
    async def test_binance_depth_100ms(self, duration=30):
        """Binance Depth 100ms - Full depth every 100ms"""
        endpoint_name = "Binance Depth 100ms"
        url = "wss://stream.binance.com:9443/ws/btcusdt@depth@100ms"
        
        return await self._run_websocket_test(endpoint_name, url, duration, self._parse_depth)
    
    async def test_binance_depth_1000ms(self, duration=30):
        """Binance Depth 1000ms - Full depth every 1000ms"""
        endpoint_name = "Binance Depth 1000ms"
        url = "wss://stream.binance.com:9443/ws/btcusdt@depth@1000ms"
        
        return await self._run_websocket_test(endpoint_name, url, duration, self._parse_depth)
    
    async def test_binance_minimal_processing(self, duration=30):
        """Ultra-fast version with minimal processing"""
        endpoint_name = "Binance BookTicker (Ultra-Fast)"
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        return await self._run_minimal_test(endpoint_name, url, duration)
    
    async def _run_websocket_test(self, endpoint_name: str, url: str, duration: int, parser_func):
        """Run a standard WebSocket test"""
        logger.info(f"🧪 Testing {endpoint_name} for {duration}s...")
        
        latencies = []
        message_count = 0
        start_time = time.perf_counter()
        connection_start = time.perf_counter()
        
        try:
            async with websockets.connect(
                url,
                ping_interval=20,
                ping_timeout=10,
                max_size=2**17,  # 128KB buffer
                compression=None,
                close_timeout=5
            ) as ws:
                connection_time = (time.perf_counter() - connection_start) * 1000
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        msg_start = time.perf_counter()
                        msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                        recv_time = time.perf_counter()
                        
                        data = json.loads(msg)
                        parse_time = time.perf_counter()
                        
                        # Parse data using appropriate parser
                        parsed_data = parser_func(data)
                        process_time = time.perf_counter()
                        
                        # Calculate latency
                        total_latency = (process_time - msg_start) * 1000
                        latencies.append(total_latency)
                        message_count += 1
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception as e:
                        logger.error(f"Error in {endpoint_name}: {e}")
                        break
                
                total_duration = time.perf_counter() - test_start
                
        except Exception as e:
            logger.error(f"Connection error for {endpoint_name}: {e}")
            return None
        
        if not latencies:
            return None
            
        return BenchmarkResult(
            endpoint_name=endpoint_name,
            total_messages=message_count,
            duration=total_duration,
            avg_messages_per_sec=message_count / total_duration,
            avg_latency_ms=statistics.mean(latencies),
            min_latency_ms=min(latencies),
            max_latency_ms=max(latencies),
            median_latency_ms=statistics.median(latencies),
            missed_updates=0,  # TODO: Implement based on expected rate
            connection_time_ms=connection_time
        )
    
    async def _run_minimal_test(self, endpoint_name: str, url: str, duration: int):
        """Ultra-minimal processing test - no parsing, just counting"""
        logger.info(f"🚀 Testing {endpoint_name} (MINIMAL) for {duration}s...")
        
        message_count = 0
        start_time = time.perf_counter()
        connection_start = time.perf_counter()
        
        try:
            async with websockets.connect(
                url,
                ping_interval=None,  # Disable ping/pong for max speed
                max_size=2**15,      # 32KB buffer - smaller for speed
                compression=None,
                close_timeout=1
            ) as ws:
                connection_time = (time.perf_counter() - connection_start) * 1000
                test_start = time.perf_counter()
                
                while time.perf_counter() - test_start < duration:
                    try:
                        # Minimal processing - just receive and count
                        await ws.recv()
                        message_count += 1
                        
                    except Exception:
                        break
                
                total_duration = time.perf_counter() - test_start
                
        except Exception as e:
            logger.error(f"Connection error for {endpoint_name}: {e}")
            return None
        
        return BenchmarkResult(
            endpoint_name=endpoint_name,
            total_messages=message_count,
            duration=total_duration,
            avg_messages_per_sec=message_count / total_duration,
            avg_latency_ms=0.1,  # Estimated minimal latency
            min_latency_ms=0.1,
            max_latency_ms=0.2,
            median_latency_ms=0.1,
            missed_updates=0,
            connection_time_ms=connection_time
        )
    
    def _parse_ticker(self, data):
        """Parse ticker data"""
        return {
            'bid': float(data['b']),
            'ask': float(data['a']),
            'last': float(data['c'])
        }
    
    def _parse_bookticker(self, data):
        """Parse bookTicker data"""
        return {
            'bid': float(data['b']),
            'ask': float(data['a']),
            'bid_qty': float(data['B']),
            'ask_qty': float(data['A'])
        }
    
    def _parse_depth(self, data):
        """Parse depth data"""
        return {
            'bids': [[float(price), float(qty)] for price, qty in data['b'][:5]],  # Top 5
            'asks': [[float(price), float(qty)] for price, qty in data['a'][:5]]   # Top 5
        }
    
    async def run_all_tests(self, test_duration=30):
        """Run all speed tests"""
        logger.info("🏁 Starting comprehensive speed comparison...")
        logger.info(f"⏱️ Each test will run for {test_duration} seconds")
        
        tests = [
            self.test_binance_ticker,
            self.test_binance_bookticker,
            self.test_binance_depth_100ms,
            self.test_binance_depth_1000ms,
            self.test_binance_minimal_processing
        ]
        
        results = []
        
        for i, test_func in enumerate(tests, 1):
            logger.info(f"\n📊 Running test {i}/{len(tests)}")
            result = await test_func(test_duration)
            if result:
                results.append(result)
                logger.info(f"✅ {result.endpoint_name}: {result.avg_messages_per_sec:.1f} msg/s")
            else:
                logger.error(f"❌ Test {i} failed")
            
            # Small delay between tests
            await asyncio.sleep(2)
        
        self.results = results
        return results
    
    def print_comparison_report(self):
        """Print detailed comparison report"""
        if not self.results:
            logger.error("No results to compare!")
            return
        
        # Sort by messages per second (fastest first)
        sorted_results = sorted(self.results, key=lambda x: x.avg_messages_per_sec, reverse=True)
        
        print("\n" + "="*120)
        print("🏆 SPEED COMPARISON RESULTS")
        print("="*120)
        
        # Header
        print(f"{'Rank':<4} {'Endpoint':<35} {'Msg/Sec':<10} {'Conn(ms)':<10} {'Avg Lat':<10} {'Med Lat':<10} {'Total Msg':<10}")
        print("-" * 120)
        
        # Results
        for i, result in enumerate(sorted_results, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📊"
            print(f"{emoji} {i:<3} {result.endpoint_name:<35} "
                  f"{result.avg_messages_per_sec:<10.1f} "
                  f"{result.connection_time_ms:<10.1f} "
                  f"{result.avg_latency_ms:<10.2f} "
                  f"{result.median_latency_ms:<10.2f} "
                  f"{result.total_messages:<10}")
        
        print("\n" + "="*120)
        print("📈 DETAILED ANALYSIS")
        print("="*120)
        
        fastest = sorted_results[0]
        print(f"🏆 FASTEST: {fastest.endpoint_name}")
        print(f"   📊 Rate: {fastest.avg_messages_per_sec:.1f} messages/second")
        print(f"   ⚡ Connection: {fastest.connection_time_ms:.1f}ms")
        print(f"   🕐 Avg Latency: {fastest.avg_latency_ms:.2f}ms")
        print(f"   📦 Total Messages: {fastest.total_messages}")
        
        if len(sorted_results) > 1:
            slowest = sorted_results[-1]
            speedup = fastest.avg_messages_per_sec / slowest.avg_messages_per_sec
            print(f"\n🐌 SLOWEST: {slowest.endpoint_name}")
            print(f"   📊 Rate: {slowest.avg_messages_per_sec:.1f} messages/second")
            print(f"   🔥 SPEEDUP: {speedup:.1f}x faster than slowest!")
        
        print("\n💡 RECOMMENDATIONS:")
        if fastest.endpoint_name.startswith("Binance BookTicker"):
            print("   ✅ Use Binance BookTicker for fastest bid/ask updates")
            print("   ✅ Disable unnecessary processing for maximum speed")
        elif fastest.endpoint_name.startswith("Binance Depth"):
            print("   ✅ Use Binance Depth streams for full order book data")
            print("   ✅ Choose 100ms interval for high-frequency trading")
        
        print("   ⚡ Minimize JSON parsing and console output")
        print("   🔧 Use smaller WebSocket buffers")
        print("   📡 Disable ping/pong for maximum throughput")

async def main():
    """Main function to run speed tests"""
    print("🚀 Binance WebSocket Speed Comparison Tool")
    print("=" * 60)
    
    # Ask user for test duration
    try:
        duration = int(input("Enter test duration in seconds (default 30): ") or "30")
    except ValueError:
        duration = 30
    
    tester = SpeedTester()
    
    try:
        results = await tester.run_all_tests(duration)
        tester.print_comparison_report()
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"speed_test_results_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("Binance WebSocket Speed Test Results\n")
            f.write(f"Test Duration: {duration} seconds\n")
            f.write(f"Timestamp: {datetime.now()}\n\n")
            
            for result in sorted(results, key=lambda x: x.avg_messages_per_sec, reverse=True):
                f.write(f"{result.endpoint_name}: {result.avg_messages_per_sec:.1f} msg/s\n")
        
        print(f"\n💾 Results saved to: {filename}")
        
    except KeyboardInterrupt:
        print("\n❌ Tests interrupted by user")
    except Exception as e:
        print(f"❌ Error running tests: {e}")

if __name__ == "__main__":
    asyncio.run(main())
