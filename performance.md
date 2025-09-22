# Performance Report

**Generated on:** 2025-09-21 22:14:18

---

## Executive Summary

This report analyzes the performance of algorithmic trading strategies over the backtest period. The strategies generated 197 total trades with a final portfolio value of $9404.26 (starting from $10000.00).

## Key Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Return** | -5.96% |
| **Annualized Return** | -3.56% |
| **Sharpe Ratio** | -4.868 |
| **Maximum Drawdown** | 7.36% |
| **Volatility (Annualized)** | 1.14% |
| **Win Rate** | 33.50% |
| **Profit Factor** | 0.46 |
| **Total Trades** | 197 |

## Trade Statistics

| Statistic | Value |
|-----------|-------|
| **Winning Trades** | 66 |
| **Losing Trades** | 131 |
| **Average Win** | $7.58 |
| **Average Loss** | $-8.37 |
| **Largest Win** | $25.01 |
| **Largest Loss** | $-26.04 |

## Risk Analysis

| Risk Metric | Value |
|-------------|-------|
| **Maximum Drawdown** | 7.36% |
| **Max DD Duration** | 374 periods |
| **Volatility** | 1.14% |
| **Sharpe Ratio** | -4.868 |

## Equity Curve

```
Equity Curve ($9286.19 - $10024.04)
|        *                                                                      
|*      ****                                                                    
| *******  *                                                                    
|           **        ***                                                       
|            **       * **                                                      
|             *    ***   **                                                     
|              *****      *                                                     
|                         ***                                                   
|                           *                                                   
|                            *                                                  
|                            *                                                  
|                            **                                                 
|                             *                                                 
|                             *                                                 
|                             *              *****                              
|                              **           *     ***                           
|                               ****     ****       **                        **
|                                  *     *           ****                    *  
|                                   *****               **               *  **  
--------------------------------------------------------------------------------
Initial: $10000.00 | Final: $9404.26
```

## Returns Analysis

**Periodic Returns Statistics:**

- **Mean Return:** -0.0144%
- **Median Return:** 0.0000%
- **Standard Deviation:** 0.0720%
- **Min Return:** -0.2737%
- **Max Return:** 0.2598%

## Final Positions

| Symbol | Quantity | Average Price | Market Value |
|--------|----------|---------------|-------------|
| AAPL | 35 | $167.37 | $5857.83 |

## Error Analysis

**Total Errors:** 16

**Error Summary:**
- 2025-09-20 14: 16

## Performance Interpretation

The strategy shows **negative performance** with losses over the backtest period. The **Sharpe ratio is poor**, suggesting weak risk-adjusted returns. **Maximum drawdown is low**, indicating good risk management. The **win rate is low**, indicating poor trade selection. 

**Profit factor is poor** (<1.0), suggesting losses exceed gains. **High trade frequency** provides good statistical sample size. ## Recommendations

- **Consider strategy revision** - Negative returns suggest fundamental issues with the approach.
- **Improve risk-adjusted returns** - Low Sharpe ratio indicates poor risk management or weak returns.
- **Review signal quality** - Low win rate suggests signals may be unreliable or poorly timed.
- **Optimize trade management** - Low profit factor indicates poor risk-reward ratio in trades.
- **Address execution errors** - Presence of errors may impact strategy performance and reliability.
- **Monitor live performance** - Compare actual results with backtest expectations.
- **Regular strategy review** - Periodically reassess and update strategy parameters.
