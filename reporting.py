"""
Performance Reporting Module

This module computes comprehensive performance metrics for algorithmic trading strategies
including total return, periodic returns, Sharpe ratio, maximum drawdown, and generates
a detailed performance report in Markdown format.
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Optional
import math
import statistics
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

@dataclass
class PerformanceMetrics:
    """Container for performance metrics"""
    total_return: float
    annualized_return: float
    sharpe_ratio: float
    max_drawdown: float
    max_drawdown_duration: int
    volatility: float
    win_rate: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    largest_win: float
    largest_loss: float

class PerformanceReporter:
    """Computes and reports trading strategy performance metrics"""
    
    def __init__(self, initial_capital: float = 10000.0, risk_free_rate: float = 0.02):
        self.initial_capital = initial_capital
        self.risk_free_rate = risk_free_rate
        self.trading_days_per_year = 252
        
    def calculate_performance(self, backtest_report: Dict) -> PerformanceMetrics:
        """Calculate comprehensive performance metrics from backtest results"""

        positions = backtest_report.get("positions", {})
        orders = backtest_report.get("orders", [])
        errors = backtest_report.get("errors", [])
        
        # Calculate portfolio value over time
        portfolio_values, returns = self._calculate_portfolio_series(orders, positions)
        
        if not portfolio_values:
            return self._empty_metrics()
        
        # Calculate basic metrics
        total_return = (portfolio_values[-1] - self.initial_capital) / self.initial_capital
        
        # Calculate annualized return
        days = len(portfolio_values)
        years = days / self.trading_days_per_year
        annualized_return = (portfolio_values[-1] / self.initial_capital) ** (1 / years) - 1 if years > 0 else 0
        
        # Calculate volatility (annualized)
        volatility = statistics.stdev(returns) * math.sqrt(self.trading_days_per_year) if len(returns) > 1 else 0
        
        # Calculate Sharpe ratio
        excess_return = annualized_return - self.risk_free_rate
        sharpe_ratio = excess_return / volatility if volatility > 0 else 0
        
        # Calculate maximum drawdown
        max_dd, max_dd_duration = self._calculate_max_drawdown(portfolio_values)
        
        # Calculate trade statistics
        trade_stats = self._calculate_trade_statistics(orders)
        
        return PerformanceMetrics(
            total_return=total_return,
            annualized_return=annualized_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_dd,
            max_drawdown_duration=max_dd_duration,
            volatility=volatility,
            win_rate=trade_stats["win_rate"],
            profit_factor=trade_stats["profit_factor"],
            total_trades=trade_stats["total_trades"],
            winning_trades=trade_stats["winning_trades"],
            losing_trades=trade_stats["losing_trades"],
            avg_win=trade_stats["avg_win"],
            avg_loss=trade_stats["avg_loss"],
            largest_win=trade_stats["largest_win"],
            largest_loss=trade_stats["largest_loss"]
        )
    
    def _calculate_portfolio_series(self, orders: List[Dict], final_positions: Dict) -> Tuple[List[float], List[float]]:
        """Calculate portfolio value series and returns from orders"""
        if not orders:
            return [], []
        
        # Sort orders by timestamp
        sorted_orders = sorted(orders, key=lambda x: x["time"])
        
        # Track portfolio value over time
        portfolio_values = [self.initial_capital]
        current_cash = self.initial_capital
        positions = {}
        
        for order in sorted_orders:
            if order["status"] != "FILLED":
                continue
                
            symbol = order["symbol"]
            side = order["side"]
            quantity = order["qty"]
            price = order["price"]
            
            # Initialize position if needed
            if symbol not in positions:
                positions[symbol] = {"quantity": 0, "avg_price": 0.0}
            
            pos = positions[symbol]
            
            if side == "BUY":
                # Update position
                old_qty = pos["quantity"]
                new_qty = old_qty + quantity
                if new_qty > 0:
                    pos["avg_price"] = (pos["avg_price"] * old_qty + price * quantity) / new_qty
                pos["quantity"] = new_qty
                current_cash -= quantity * price
            elif side == "SELL":
                # Update position
                sell_qty = min(quantity, pos["quantity"])
                pos["quantity"] -= sell_qty
                if pos["quantity"] == 0:
                    pos["avg_price"] = 0.0
                current_cash += sell_qty * price
            
            # Calculate current portfolio value
            portfolio_value = current_cash
            for sym, pos_data in positions.items():
                portfolio_value += pos_data["quantity"] * pos_data["avg_price"]
            
            portfolio_values.append(portfolio_value)
        
        # Calculate returns
        returns = []
        for i in range(1, len(portfolio_values)):
            if portfolio_values[i-1] != 0:
                ret = (portfolio_values[i] - portfolio_values[i-1]) / portfolio_values[i-1]
                returns.append(ret)
        
        return portfolio_values, returns
    
    def _calculate_max_drawdown(self, portfolio_values: List[float]) -> Tuple[float, int]:
        """Calculate maximum drawdown and its duration"""
        if not portfolio_values:
            return 0.0, 0
        
        peak = portfolio_values[0]
        max_dd = 0.0
        max_dd_duration = 0
        current_dd_duration = 0
        
        for value in portfolio_values:
            if value > peak:
                peak = value
                current_dd_duration = 0
            else:
                dd = (peak - value) / peak
                max_dd = max(max_dd, dd)
                current_dd_duration += 1
                max_dd_duration = max(max_dd_duration, current_dd_duration)
        
        return max_dd, max_dd_duration
    
    def _calculate_trade_statistics(self, orders: List[Dict]) -> Dict:
        """Calculate trade-level statistics"""
        filled_orders = [o for o in orders if o["status"] == "FILLED"]
        
        if not filled_orders:
            return {
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "avg_win": 0.0,
                "avg_loss": 0.0,
                "largest_win": 0.0,
                "largest_loss": 0.0
            }
        
        # Group orders by symbol and calculate P&L for each trade
        symbol_orders = {}
        for order in filled_orders:
            symbol = order["symbol"]
            if symbol not in symbol_orders:
                symbol_orders[symbol] = []
            symbol_orders[symbol].append(order)
        
        trade_pnls = []
        for symbol, symbol_order_list in symbol_orders.items():
            symbol_order_list.sort(key=lambda x: x["time"])
            
            # Calculate P&L for each round trip
            position = 0
            avg_price = 0.0
            
            for order in symbol_order_list:
                if order["side"] == "BUY":
                    if position >= 0:  # Adding to long position
                        new_position = position + order["qty"]
                        if new_position > 0:
                            avg_price = (avg_price * position + order["price"] * order["qty"]) / new_position
                        position = new_position
                    else:  # Covering short position
                        cover_qty = min(order["qty"], abs(position))
                        pnl = cover_qty * (avg_price - order["price"])
                        trade_pnls.append(pnl)
                        position += cover_qty
                        if position == 0:
                            avg_price = 0.0
                
                elif order["side"] == "SELL":
                    if position <= 0:  # Adding to short position
                        new_position = position - order["qty"]
                        if new_position < 0:
                            avg_price = (avg_price * abs(position) + order["price"] * order["qty"]) / abs(new_position)
                        position = new_position
                    else:  # Closing long position
                        close_qty = min(order["qty"], position)
                        pnl = close_qty * (order["price"] - avg_price)
                        trade_pnls.append(pnl)
                        position -= close_qty
                        if position == 0:
                            avg_price = 0.0
        
        # Calculate statistics
        winning_trades = [pnl for pnl in trade_pnls if pnl > 0]
        losing_trades = [pnl for pnl in trade_pnls if pnl < 0]
        
        total_trades = len(trade_pnls)
        winning_count = len(winning_trades)
        losing_count = len(losing_trades)
        
        win_rate = winning_count / total_trades if total_trades > 0 else 0.0
        avg_win = statistics.mean(winning_trades) if winning_trades else 0.0
        avg_loss = statistics.mean(losing_trades) if losing_trades else 0.0
        largest_win = max(winning_trades) if winning_trades else 0.0
        largest_loss = min(losing_trades) if losing_trades else 0.0
        
        gross_profit = sum(winning_trades)
        gross_loss = abs(sum(losing_trades))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf') if gross_profit > 0 else 0.0
        
        return {
            "win_rate": win_rate,
            "profit_factor": profit_factor,
            "total_trades": total_trades,
            "winning_trades": winning_count,
            "losing_trades": losing_count,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "largest_win": largest_win,
            "largest_loss": largest_loss
        }
    
    def _empty_metrics(self) -> PerformanceMetrics:
        """Return empty metrics when no data is available"""
        return PerformanceMetrics(
            total_return=0.0,
            annualized_return=0.0,
            sharpe_ratio=0.0,
            max_drawdown=0.0,
            max_drawdown_duration=0,
            volatility=0.0,
            win_rate=0.0,
            profit_factor=0.0,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            avg_win=0.0,
            avg_loss=0.0,
            largest_win=0.0,
            largest_loss=0.0
        )
    
    def generate_equity_curve_ascii(self, portfolio_values: List[float], width: int = 80, height: int = 20) -> str:
        """Generate ASCII art equity curve"""
        if not portfolio_values:
            return "No data available for equity curve"
        
        min_val = min(portfolio_values)
        max_val = max(portfolio_values)
        val_range = max_val - min_val
        
        if val_range == 0:
            return "No variation in portfolio value"
        
        # Create ASCII grid
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Plot points
        for i, value in enumerate(portfolio_values):
            x = int((i / (len(portfolio_values) - 1)) * (width - 1)) if len(portfolio_values) > 1 else width // 2
            y = int(((value - min_val) / val_range) * (height - 1))
            if 0 <= x < width and 0 <= y < height:
                grid[height - 1 - y][x] = '*'
        
        # Connect points with lines
        for i in range(len(portfolio_values) - 1):
            x1 = int((i / (len(portfolio_values) - 1)) * (width - 1)) if len(portfolio_values) > 1 else width // 2
            x2 = int(((i + 1) / (len(portfolio_values) - 1)) * (width - 1)) if len(portfolio_values) > 1 else width // 2
            y1 = int(((portfolio_values[i] - min_val) / val_range) * (height - 1))
            y2 = int(((portfolio_values[i + 1] - min_val) / val_range) * (height - 1))
            
            # Simple line drawing
            steps = max(abs(x2 - x1), abs(y2 - y1))
            if steps > 0:
                for step in range(steps + 1):
                    x = x1 + (x2 - x1) * step // steps
                    y = y1 + (y2 - y1) * step // steps
                    if 0 <= x < width and 0 <= y < height:
                        grid[height - 1 - y][x] = '*'
        
        # Add axes
        for i in range(height):
            grid[i][0] = '|'
        for i in range(width):
            grid[height - 1][i] = '-'
        
        # Convert to string
        lines = [''.join(row) for row in grid]
        
        # labels
        result = f"Equity Curve (${min_val:.2f} - ${max_val:.2f})\n"
        result += '\n'.join(lines)
        result += f"\nInitial: ${self.initial_capital:.2f} | Final: ${portfolio_values[-1]:.2f}"
        
        return result
    
    def generate_performance_report(self, backtest_report: Dict, output_file: str = None) -> str:
        """
        Generate comprehensive performance report in Markdown format
            
        Returns:
            Markdown report content as string
        """
        # Calculate performance metrics
        metrics = self.calculate_performance(backtest_report)
        
        orders = backtest_report.get("orders", [])
        errors = backtest_report.get("errors", [])
        positions = backtest_report.get("positions", {})
        
        # Calculate portfolio series for equity curve
        portfolio_values, returns = self._calculate_portfolio_series(orders, positions)
        
        # Generate report content
        report_content = self._generate_markdown_content(metrics, orders, errors, positions, portfolio_values, returns)
        
        if output_file is None:
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(current_dir, "performance.md")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_content
    
    def _generate_markdown_content(self, metrics: PerformanceMetrics, orders: List[Dict], 
                                 errors: List[str], positions: Dict, portfolio_values: List[float], 
                                 returns: List[float]) -> str:
        """Generate the markdown report content"""
        
        # Header
        content = "# Performance Report\n\n"
        content += f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        content += "---\n\n"
        
        # Executive Summary
        content += "## Executive Summary\n\n"
        content += f"This report analyzes the performance of algorithmic trading strategies "
        content += f"over the backtest period. The strategies generated {metrics.total_trades} total trades "
        content += f"with a final portfolio value of ${portfolio_values[-1]:.2f} "
        content += f"(starting from ${self.initial_capital:.2f}).\n\n"
        
        # Key Performance Metrics Table
        content += "## Key Performance Metrics\n\n"
        content += "| Metric | Value |\n"
        content += "|--------|-------|\n"
        content += f"| **Total Return** | {metrics.total_return:.2%} |\n"
        content += f"| **Annualized Return** | {metrics.annualized_return:.2%} |\n"
        content += f"| **Sharpe Ratio** | {metrics.sharpe_ratio:.3f} |\n"
        content += f"| **Maximum Drawdown** | {metrics.max_drawdown:.2%} |\n"
        content += f"| **Volatility (Annualized)** | {metrics.volatility:.2%} |\n"
        content += f"| **Win Rate** | {metrics.win_rate:.2%} |\n"
        content += f"| **Profit Factor** | {metrics.profit_factor:.2f} |\n"
        content += f"| **Total Trades** | {metrics.total_trades} |\n\n"
        
        # Trade Statistics
        content += "## Trade Statistics\n\n"
        content += "| Statistic | Value |\n"
        content += "|-----------|-------|\n"
        content += f"| **Winning Trades** | {metrics.winning_trades} |\n"
        content += f"| **Losing Trades** | {metrics.losing_trades} |\n"
        content += f"| **Average Win** | ${metrics.avg_win:.2f} |\n"
        content += f"| **Average Loss** | ${metrics.avg_loss:.2f} |\n"
        content += f"| **Largest Win** | ${metrics.largest_win:.2f} |\n"
        content += f"| **Largest Loss** | ${metrics.largest_loss:.2f} |\n\n"
        
        # Risk Metrics
        content += "## Risk Analysis\n\n"
        content += "| Risk Metric | Value |\n"
        content += "|-------------|-------|\n"
        content += f"| **Maximum Drawdown** | {metrics.max_drawdown:.2%} |\n"
        content += f"| **Max DD Duration** | {metrics.max_drawdown_duration} periods |\n"
        content += f"| **Volatility** | {metrics.volatility:.2%} |\n"
        content += f"| **Sharpe Ratio** | {metrics.sharpe_ratio:.3f} |\n\n"
        
        # Equity Curve
        content += "## Equity Curve\n\n"
        if portfolio_values:
            content += "```\n"
            content += self.generate_equity_curve_ascii(portfolio_values)
            content += "\n```\n\n"
        else:
            content += "No portfolio data available for equity curve.\n\n"
        
        # Returns Analysis
        if returns:
            content += "## Returns Analysis\n\n"
            content += f"**Periodic Returns Statistics:**\n\n"
            content += f"- **Mean Return:** {statistics.mean(returns):.4%}\n"
            content += f"- **Median Return:** {statistics.median(returns):.4%}\n"
            content += f"- **Standard Deviation:** {statistics.stdev(returns):.4%}\n"
            content += f"- **Min Return:** {min(returns):.4%}\n"
            content += f"- **Max Return:** {max(returns):.4%}\n\n"
        
        # Final Positions
        content += "## Final Positions\n\n"
        if positions:
            content += "| Symbol | Quantity | Average Price | Market Value |\n"
            content += "|--------|----------|---------------|-------------|\n"
            for symbol, pos_data in positions.items():
                qty = pos_data.get("quantity", 0)
                avg_price = pos_data.get("avg_price", 0.0)
                market_value = qty * avg_price
                content += f"| {symbol} | {qty} | ${avg_price:.2f} | ${market_value:.2f} |\n"
        else:
            content += "No positions held at end of backtest.\n"
        content += "\n"
        
        # Error Analysis
        if errors:
            content += "## Error Analysis\n\n"
            content += f"**Total Errors:** {len(errors)}\n\n"
            content += "**Error Summary:**\n"
            error_types = {}
            for error in errors:
                error_type = error.split(":")[0] if ":" in error else "Unknown"
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            for error_type, count in error_types.items():
                content += f"- {error_type}: {count}\n"
            content += "\n"
        
        # Performance Interpretation
        content += "## Performance Interpretation\n\n"
        content += self._generate_performance_interpretation(metrics)
        
        # Recommendations
        content += "## Recommendations\n\n"
        content += self._generate_recommendations(metrics, len(errors))
        
        return content
    
    def _generate_performance_interpretation(self, metrics: PerformanceMetrics) -> str:
        """Generate narrative interpretation of performance results"""
        interpretation = ""
        
        # Overall performance assessment
        if metrics.total_return > 0.1:
            interpretation += "The strategy demonstrates **strong positive performance** with significant returns. "
        elif metrics.total_return > 0:
            interpretation += "The strategy shows **modest positive performance** with small but positive returns. "
        else:
            interpretation += "The strategy shows **negative performance** with losses over the backtest period. "
        
        # Risk assessment
        if metrics.sharpe_ratio > 1.0:
            interpretation += "The **Sharpe ratio is excellent**, indicating strong risk-adjusted returns. "
        elif metrics.sharpe_ratio > 0.5:
            interpretation += "The **Sharpe ratio is good**, showing decent risk-adjusted performance. "
        else:
            interpretation += "The **Sharpe ratio is poor**, suggesting weak risk-adjusted returns. "
        
        # Drawdown assessment
        if metrics.max_drawdown < 0.1:
            interpretation += "**Maximum drawdown is low**, indicating good risk management. "
        elif metrics.max_drawdown < 0.2:
            interpretation += "**Maximum drawdown is moderate**, showing acceptable risk levels. "
        else:
            interpretation += "**Maximum drawdown is high**, indicating significant risk exposure. "
        
        # Win rate assessment
        if metrics.win_rate > 0.6:
            interpretation += "The **win rate is high**, suggesting good trade selection. "
        elif metrics.win_rate > 0.4:
            interpretation += "The **win rate is moderate**, showing mixed trade quality. "
        else:
            interpretation += "The **win rate is low**, indicating poor trade selection. "
        
        interpretation += "\n\n"
        
        if metrics.profit_factor > 2.0:
            interpretation += "**Profit factor is excellent** (>2.0), indicating that winning trades significantly outweigh losing trades. "
        elif metrics.profit_factor > 1.5:
            interpretation += "**Profit factor is good** (>1.5), showing profitable trade distribution. "
        elif metrics.profit_factor > 1.0:
            interpretation += "**Profit factor is positive** (>1.0), indicating net profitability. "
        else:
            interpretation += "**Profit factor is poor** (<1.0), suggesting losses exceed gains. "
        
        if metrics.total_trades < 10:
            interpretation += "**Low trade frequency** may limit statistical significance of results. "
        elif metrics.total_trades > 100:
            interpretation += "**High trade frequency** provides good statistical sample size. "
        
        return interpretation
    
    def _generate_recommendations(self, metrics: PerformanceMetrics, error_count: int) -> str:
        """Generate recommendations based on performance analysis"""
        recommendations = []
        
        # Performance-based recommendations
        if metrics.total_return < 0:
            recommendations.append("**Consider strategy revision** - Negative returns suggest fundamental issues with the approach.")
        
        if metrics.sharpe_ratio < 0.5:
            recommendations.append("**Improve risk-adjusted returns** - Low Sharpe ratio indicates poor risk management or weak returns.")
        
        if metrics.max_drawdown > 0.2:
            recommendations.append("**Implement better risk controls** - High maximum drawdown suggests need for position sizing or stop-loss mechanisms.")
        
        if metrics.win_rate < 0.4:
            recommendations.append("**Review signal quality** - Low win rate suggests signals may be unreliable or poorly timed.")
        
        if metrics.profit_factor < 1.2:
            recommendations.append("**Optimize trade management** - Low profit factor indicates poor risk-reward ratio in trades.")
        
        if error_count > 0:
            recommendations.append("**Address execution errors** - Presence of errors may impact strategy performance and reliability.")
        
        if metrics.total_trades < 20:
            recommendations.append("**Extend backtest period** - Limited trade sample may not be representative of strategy performance.")
        
        # General recommendations
        recommendations.append("**Monitor live performance** - Compare actual results with backtest expectations.")
        recommendations.append("**Regular strategy review** - Periodically reassess and update strategy parameters.")
        
        if not recommendations:
            recommendations.append("**Strategy shows good performance** - Consider scaling up or optimizing further.")
        
        return "\n".join(f"- {rec}" for rec in recommendations) + "\n"


def main():
    """Example usage of the PerformanceReporter"""
    # This would typically be called from main.py after running backtest
    print("Performance Reporter Module")
    print("This module should be integrated with the main backtest system.")
    print("Use PerformanceReporter.generate_performance_report() to create reports.")


if __name__ == "__main__":
    main()
