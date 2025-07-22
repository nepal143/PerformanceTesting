#!/usr/bin/env python3
"""
🚀 ULTIMATE ARBITRAGE SPEED MONITOR
Real-time ultra-fast cryptocurrency data feeds from multiple exchanges
Optimized for maximum speed and minimum latency for arbitrage opportunities
"""

import asyncio
import time
import json
import websockets
import logging
from datetime import datetime

# Set up minimal logging
logging.basicConfig(level=logging.WARNING)  # Reduce log output for speed
logger = logging.getLogger(__name__)

try:
    import orjson
    HAS_ORJSON = True
    fast_json_loads = orjson.loads
    print("🔥 Using orjson (FASTEST)")
except ImportError:
    try:
        import ujson
        HAS_ORJSON = False
        HAS_UJSON = True
        import ujson
        fast_json_loads = ujson.loads
        print("⚡ Using ujson (fast)")
    except ImportError:
        HAS_ORJSON = False
        HAS_UJSON = False
        fast_json_loads = json.loads
        print("📊 Using standard json")

class ArbitrageSpeedMonitor:
    def __init__(self):
        self.prices = {}
        self.message_counts = {}
        self.start_time = time.perf_counter()
        self.last_update = {}
        
    def update_price(self, exchange, bid, ask, timestamp=None):
        """Update price and calculate arbitrage opportunities"""
        if timestamp is None:
            timestamp = time.perf_counter()
            
        self.prices[exchange] = {'bid': bid, 'ask': ask, 'time': timestamp}
        self.message_counts[exchange] = self.message_counts.get(exchange, 0) + 1
        self.last_update[exchange] = timestamp
        
        # Calculate arbitrage opportunities
        self.check_arbitrage()
        
    def check_arbitrage(self):
        """Check for arbitrage opportunities across exchanges"""
        if len(self.prices) < 2:
            return
            
        exchanges = list(self.prices.keys())
        opportunities = []
        
        for i, ex1 in enumerate(exchanges):
            for ex2 in exchanges[i+1:]:
                price1 = self.prices[ex1]
                price2 = self.prices[ex2]
                
                # Check if data is fresh (within last 5 seconds)
                current_time = time.perf_counter()
                if (current_time - price1['time'] > 5 or 
                    current_time - price2['time'] > 5):
                    continue
                
                # Calculate potential profits
                # Buy on ex1, sell on ex2
                profit1 = price2['bid'] - price1['ask']
                profit1_pct = (profit1 / price1['ask']) * 100
                
                # Buy on ex2, sell on ex1  
                profit2 = price1['bid'] - price2['ask']
                profit2_pct = (profit2 / price2['ask']) * 100
                
                if profit1_pct > 0.01:  # More than 0.01% profit
                    opportunities.append({
                        'buy_exchange': ex1,
                        'sell_exchange': ex2,
                        'buy_price': price1['ask'],
                        'sell_price': price2['bid'],
                        'profit_usd': profit1,
                        'profit_pct': profit1_pct
                    })
                
                if profit2_pct > 0.01:
                    opportunities.append({
                        'buy_exchange': ex2,
                        'sell_exchange': ex1,
                        'buy_price': price2['ask'],
                        'sell_price': price1['bid'],
                        'profit_usd': profit2,
                        'profit_pct': profit2_pct
                    })
        
        # Display best opportunity
        if opportunities:
            best = max(opportunities, key=lambda x: x['profit_pct'])
            print(f"💰 ARBITRAGE: Buy {best['buy_exchange']} ${best['buy_price']:.2f} → "
                  f"Sell {best['sell_exchange']} ${best['sell_price']:.2f} = "
                  f"+${best['profit_usd']:.2f} ({best['profit_pct']:.3f}%)")
    
    def print_status(self):
        """Print current status"""
        current_time = time.perf_counter()
        runtime = current_time - self.start_time
        
        print(f"\\n📊 ULTRA-FAST ARBITRAGE MONITOR - Runtime: {runtime:.1f}s")
        print("=" * 80)
        
        for exchange in sorted(self.prices.keys()):
            price = self.prices[exchange]
            count = self.message_counts[exchange]
            age = current_time - price['time']
            rate = count / runtime if runtime > 0 else 0
            
            status = "🟢" if age < 1 else "🟡" if age < 3 else "🔴"
            print(f"{status} {exchange:10} | Bid: ${price['bid']:>9.2f} | "
                  f"Ask: ${price['ask']:>9.2f} | {rate:>6.1f} msg/s | "
                  f"Age: {age:>4.1f}s")

    async def binance_feed(self):
        """Ultra-fast Binance BookTicker feed"""
        url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
        
        while True:
            try:
                async with websockets.connect(
                    url, 
                    ping_interval=None, 
                    max_size=1024,
                    compression=None
                ) as ws:
                    print("🚀 Binance BookTicker connected (ULTRA-FAST)")
                    
                    async for message in ws:
                        try:
                            data = fast_json_loads(message)
                            if 'b' in data and 'a' in data:
                                bid = float(data['b'])
                                ask = float(data['a'])
                                self.update_price('Binance', bid, ask)
                        except Exception:
                            continue
                            
            except Exception as e:
                logger.error(f"Binance connection error: {e}")
                await asyncio.sleep(1)
    
    async def bybit_feed(self):
        """Ultra-fast Bybit OrderBook feed"""
        url = "wss://stream.bybit.com/v5/public/spot"
        subscribe_msg = {"op": "subscribe", "args": ["orderbook.1.BTCUSDT"]}
        
        while True:
            try:
                async with websockets.connect(
                    url,
                    ping_interval=None,
                    max_size=2048,
                    compression=None
                ) as ws:
                    await ws.send(json.dumps(subscribe_msg))
                    print("🚀 Bybit OrderBook connected (ULTRA-FAST)")
                    
                    async for message in ws:
                        try:
                            data = fast_json_loads(message)
                            
                            if (isinstance(data, dict) and 
                                data.get('topic', '').startswith('orderbook') and 
                                'data' in data):
                                
                                book_data = data['data']
                                bids = book_data.get('b', [])
                                asks = book_data.get('a', [])
                                
                                if bids and asks:
                                    bid = float(bids[0][0])
                                    ask = float(asks[0][0])
                                    self.update_price('Bybit', bid, ask)
                        except Exception:
                            continue
                            
            except Exception as e:
                logger.error(f"Bybit connection error: {e}")
                await asyncio.sleep(1)
    
    async def okx_feed(self):
        """Ultra-fast OKX Books5 feed"""
        url = "wss://ws.okx.com:8443/ws/v5/public"
        subscribe_msg = {"op": "subscribe", "args": [{"channel": "books5", "instId": "BTC-USDT"}]}
        
        while True:
            try:
                async with websockets.connect(
                    url,
                    ping_interval=None,
                    max_size=2048,
                    compression=None
                ) as ws:
                    await ws.send(json.dumps(subscribe_msg))
                    print("🚀 OKX Books5 connected (ULTRA-FAST)")
                    
                    async for message in ws:
                        try:
                            data = fast_json_loads(message)
                            
                            if (isinstance(data, dict) and 
                                'data' in data and 
                                data.get('arg', {}).get('channel') == 'books5'):
                                
                                book_data = data['data'][0] if data['data'] else {}
                                bids = book_data.get('bids', [])
                                asks = book_data.get('asks', [])
                                
                                if bids and asks:
                                    bid = float(bids[0][0])
                                    ask = float(asks[0][0])
                                    self.update_price('OKX', bid, ask)
                        except Exception:
                            continue
                            
            except Exception as e:
                logger.error(f"OKX connection error: {e}")
                await asyncio.sleep(1)
    
    async def status_printer(self):
        """Print status every few seconds"""
        while True:
            await asyncio.sleep(3)
            self.print_status()
    
    async def run(self):
        """Run all feeds simultaneously"""
        print("🚀 STARTING ULTIMATE ARBITRAGE SPEED MONITOR")
        print("=" * 80)
        print("📊 Connecting to ultra-fast feeds...")
        print("💰 Monitoring for arbitrage opportunities...")
        print("⚡ Press Ctrl+C to stop")
        print()
        
        # Start all feeds concurrently
        tasks = [
            asyncio.create_task(self.binance_feed()),
            asyncio.create_task(self.bybit_feed()),
            asyncio.create_task(self.okx_feed()),
            asyncio.create_task(self.status_printer())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print("\\n🛑 Stopping monitor...")
            self.print_status()
            
            # Print final statistics
            runtime = time.perf_counter() - self.start_time
            total_messages = sum(self.message_counts.values())
            print(f"\\n📈 FINAL STATS:")
            print(f"   ⏱️ Runtime: {runtime:.1f} seconds")
            print(f"   📊 Total messages: {total_messages}")
            print(f"   🚀 Overall rate: {total_messages/runtime:.1f} msg/s")
            print(f"   🥇 Fastest exchange: {max(self.message_counts.items(), key=lambda x: x[1])[0]}")

async def main():
    monitor = ArbitrageSpeedMonitor()
    await monitor.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n👋 Goodbye!")
