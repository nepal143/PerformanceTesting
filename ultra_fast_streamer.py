import asyncio
import websockets
import json
import time
from datetime import datetime
import logging

# Minimal logging
logging.basicConfig(level=logging.WARNING)

class UltraFastBinanceStreamer:
    """Ultra-optimized Binance streamer for maximum speed"""
    
    def __init__(self, symbol="btcusdt"):
        self.symbol = symbol.lower()
        self.message_count = 0
        self.start_time = None
        
        # BookTicker endpoint - fastest for bid/ask
        self.bookticker_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@bookTicker"
        
        # Depth endpoint - 100ms updates
        self.depth_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@depth@100ms"
    
    async def stream_bookticker_ultra_fast(self):
        """Ultra-fast BookTicker stream with minimal processing"""
        print(f"🚀 Starting ULTRA-FAST BookTicker stream for {self.symbol.upper()}")
        print("📊 Optimizations: No logging, minimal parsing, no console output in loop")
        
        self.start_time = time.perf_counter()
        
        async with websockets.connect(
            self.bookticker_url,
            ping_interval=None,    # Disable ping/pong
            max_size=2**14,       # 16KB buffer - smallest possible
            compression=None,      # No compression
            close_timeout=1        # Fast close
        ) as ws:
            print("📡 Connected to BookTicker stream")
            
            # Variables for periodic stats (avoid division in hot loop)
            last_stats_time = self.start_time
            stats_interval = 5  # Print stats every 5 seconds
            
            while True:
                try:
                    # Hot loop - minimal operations
                    msg = await ws.recv()
                    self.message_count += 1
                    
                    # Only parse and print stats periodically
                    current_time = time.perf_counter()
                    if current_time - last_stats_time >= stats_interval:
                        # Parse only for stats
                        data = json.loads(msg)
                        bid = float(data['b'])
                        ask = float(data['a'])
                        
                        elapsed = current_time - self.start_time
                        rate = self.message_count / elapsed
                        
                        print(f"📈 Bid: {bid:>10.2f} | Ask: {ask:>10.2f} | "
                              f"Rate: {rate:.1f} msg/s | Total: {self.message_count}")
                        
                        last_stats_time = current_time
                
                except Exception as e:
                    print(f"❌ Error: {e}")
                    break
    
    async def stream_depth_fast(self):
        """Fast depth stream with optimized processing"""
        print(f"🚀 Starting FAST Depth stream for {self.symbol.upper()}")
        print("📊 100ms updates with top 5 levels only")
        
        self.start_time = time.perf_counter()
        
        async with websockets.connect(
            self.depth_url,
            ping_interval=30,     # Longer ping interval
            max_size=2**16,      # 64KB for depth data
            compression=None,
            close_timeout=2
        ) as ws:
            print("📡 Connected to Depth stream")
            
            last_stats_time = self.start_time
            stats_interval = 5
            
            while True:
                try:
                    msg = await ws.recv()
                    self.message_count += 1
                    
                    current_time = time.perf_counter()
                    if current_time - last_stats_time >= stats_interval:
                        # Parse depth data
                        data = json.loads(msg)
                        
                        # Get top 3 bids and asks only
                        top_bids = [[float(p), float(q)] for p, q in data['b'][:3]]
                        top_asks = [[float(p), float(q)] for p, q in data['a'][:3]]
                        
                        elapsed = current_time - self.start_time
                        rate = self.message_count / elapsed
                        
                        print(f"📊 Best Bid: {top_bids[0][0]:.2f} | Best Ask: {top_asks[0][0]:.2f} | "
                              f"Rate: {rate:.1f} msg/s | Total: {self.message_count}")
                        
                        last_stats_time = current_time
                
                except Exception as e:
                    print(f"❌ Error: {e}")
                    break
    
    async def stream_comparison(self, duration=60):
        """Run both streams in parallel for comparison"""
        print("🏁 Running parallel comparison test...")
        
        tasks = [
            asyncio.create_task(self._timed_stream(self.stream_bookticker_ultra_fast, "BookTicker", duration)),
            asyncio.create_task(self._timed_stream(self.stream_depth_fast, "Depth", duration))
        ]
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _timed_stream(self, stream_func, name, duration):
        """Run a stream for a specific duration"""
        start_time = time.perf_counter()
        
        try:
            # Create a timeout task
            await asyncio.wait_for(stream_func(), timeout=duration)
        except asyncio.TimeoutError:
            elapsed = time.perf_counter() - start_time
            rate = self.message_count / elapsed
            print(f"⏰ {name} test completed: {self.message_count} messages in {elapsed:.1f}s ({rate:.1f} msg/s)")

async def benchmark_single_stream():
    """Benchmark a single ultra-fast stream"""
    print("🧪 Single Stream Benchmark")
    print("=" * 50)
    
    streamer = UltraFastBinanceStreamer()
    
    print("Choose stream type:")
    print("1. BookTicker (Ultra-Fast)")
    print("2. Depth 100ms")
    
    choice = input("Enter choice (1 or 2): ").strip()
    duration = int(input("Enter test duration (seconds): ") or "30")
    
    start_time = time.perf_counter()
    
    try:
        if choice == "1":
            await asyncio.wait_for(streamer.stream_bookticker_ultra_fast(), timeout=duration)
        else:
            await asyncio.wait_for(streamer.stream_depth_fast(), timeout=duration)
    except asyncio.TimeoutError:
        pass
    
    elapsed = time.perf_counter() - start_time
    rate = streamer.message_count / elapsed
    
    print("\n" + "="*50)
    print("📊 FINAL BENCHMARK RESULTS")
    print("="*50)
    print(f"Total Messages: {streamer.message_count}")
    print(f"Duration: {elapsed:.1f}s")
    print(f"Average Rate: {rate:.1f} messages/second")
    print(f"Time per message: {1000/rate:.2f}ms")
    
    if rate > 50:
        print("🏆 EXCELLENT! High-frequency ready")
    elif rate > 20:
        print("✅ GOOD! Suitable for most trading")
    else:
        print("⚠️ SLOW! Needs optimization")

async def main():
    """Main menu"""
    print("🚀 Ultra-Fast Binance WebSocket Tester")
    print("=" * 60)
    print("1. Single stream benchmark")
    print("2. Comparison with original streamer")
    print("3. Exit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        await benchmark_single_stream()
    elif choice == "2":
        print("Starting comparison mode...")
        streamer = UltraFastBinanceStreamer()
        await streamer.stream_comparison(30)
    else:
        print("Goodbye! 👋")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
