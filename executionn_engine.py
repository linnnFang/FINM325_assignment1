'''

In the execution engine, simulate occasional failures and raise ExecutionError; catch and log these errors to continue processing.
--------------------------
Execution Engine

Iterate through the list of MarketDataPoint objects in timestamp order.
For each tick:
- Invoke each strategy to generate signals.
- Instantiate and validate Order objects.
- Execute orders by updating the portfolio dictionary.
- Wrap order creation and execution in try/except blocks for resilience.

we got data to turn it into signal
then make order and calculate our position
'''
from models import MarketDataPoint, Order, OrderError, ExecutionError, MarketDataContainer
from strategies import MovingAverageCrossover, Momentum

# Iterate through the list of MarketDataPoint objects in timestamp order.
# we get a list from the dataloader, then apply the strategies to 
# Invoke each strategy to generate signals.    

# signals from strategies execution




def generateSignals(marketdataPT):
    '''
    genenrate siganls by two strategies
    '''
    positions = MarketDataContainer.all_position[marketdataPT[0]]
    MA_signals = MovingAverageCrossover.generate_signals(marketdataPT[0], positions)
    mont_signals = Momentum.generate_signals(marketdataPT[0], positions)
    return MA_signals,mont_signals
    

def Makeorder(signal):
    '''
    turn signals into order and validate

    signal format is ("SELL", tick.symbol, self._qty, tick.price)
    '''

    action, symbol, qty, price = signal
    if action not in ("BUY", "SELL"):
        raise OrderError("action must be BUY or SELL")
    if qty <= 0:
        raise OrderError("quantity must be > 0")
    if price <= 0:
        raise OrderError("price must be > 0")
    if action == "SELL":
        held = int(positions.get(symbol, {}).get("total_shares", 0))
        if held < qty:
            raise OrderError(f"insufficient shares to sell (have {held}, need {qty})")

    return Order(symbol, qty, price, action, status="NEW")

def portfolioPosition():
    '''
    after order, our initial position
    '''
def execute(order):
    '''
    fill exactly at order.price
    '''
    if order.price <= 0:
            raise ExecutionError("invalid execution price")
    return order.price

def execution(marketlist):
    '''
    turn signals -> orders -> execute -> update portfolio
    '''
    marketlist = sorted(marketlist, key=lambda t: t.timestamp)
    # turn signals and make order
    for i in range(len(marketList)):
        MA_sig, Momentum_sig =generateSignals(marketlist[i])
        MA_order= Makeorder(MA_sig)
        Momentum_order = Makeorder(Momentum_sig)
