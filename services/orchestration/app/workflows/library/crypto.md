# AI Workflows: Crypto

## 1. MEV Bot Protection Loop
- **Trigger**: Transaction submitted to the mempool.
- **AI Agents Involved**: SecurityAgent, DealFlow.
- **Expected Output**: Flashbots bundle submission to avoid frontrunning.

## 2. Crypto Tax Liability Tracker
- **Trigger**: Wallet address executes a swap on a DEX.
- **AI Agents Involved**: BudgetMind, ComplianceGate.
- **Expected Output**: Unrealized gain/loss update and tax reserve calculation.

## 3. Smart Contract Audit Bot
- **Trigger**: GitHub commit to a `.sol` or `.vy` file.
- **AI Agents Involved**: ComplianceGate, SecurityAgent.
- **Expected Output**: Reentrancy and overflow vulnerability report.

## 4. On-Chain Whale Alert
- **Trigger**: Movement of >$1M in assets between wallets.
- **AI Agents Involved**: MarketPulse, ChiefPulse.
- **Expected Output**: Telegram alert with sentiment impact analysis.

## 5. Automated DAO Proposal Summary
- **Trigger**: New proposal posted to Snapshot or Tally.
- **AI Agents Involved**: ContentEngine, BoardReady.
- **Expected Output**: 3-bullet summary and voting recommendation.

## 6. DeFi Liquidation Warning
- **Trigger**: Asset price drops within 5% of liquidation threshold.
- **AI Agents Involved**: BudgetMind, DealFlow.
- **Expected Output**: Automated repayment or collateral top-up.

## 7. NFT Rarity & Value Assessment
- **Trigger**: New collection minted on-chain.
- **AI Agents Involved**: MarketPulse, ContentEngine.
- **Expected Output**: Rarity score and "Buy/Sell" recommendation.

## 8. Regulatory Compliance (AML/KYC)
- **Trigger**: Deposit from a Tornado Cash linked address.
- **AI Agents Involved**: ComplianceGate, SecurityAgent.
- **Expected Output**: Account freeze and suspicious activity report.

## 9. Algorithmic Stablecoin Depeg Alert
- **Trigger**: Price deviation of >1% from the peg.
- **AI Agents Involved**: MarketPulse, BudgetMind.
- **Expected Output**: Emergency arbitrage execution or exit strategy.

## 10. Crypto Portfolio Rebalancing
- **Trigger**: Weekly timer or specific asset percentage drift.
- **AI Agents Involved**: BudgetMind, DealFlow.
- **Expected Output**: Series of swap transactions to hit target allocation.

---

## Template Scripts

```python
# 1. MEV Protection
def protect_tx(tx_hash):
    return {"method": "private_rpc", "relay": "flashbots"}

# 2. Tax Liability
def track_taxes(amount_usd, cost_basis):
    gain = amount_usd - cost_basis
    return {"gain": gain, "tax_due": gain * 0.20}

# 3. Contract Audit
def audit_solidity(source_code):
    if "mapping" in source_code and "msg.sender" in source_code:
        return {"vulnerabilities": ["reentrancy_risk"]}

# 4. Whale Alert
def whale_watch(amount):
    if amount > 1000000:
        return {"msg": "WHALE ALERT: 1M USDC moved to Binance"}

# 5. DAO Summary
def summarize_prop(description):
    return {"summary": description[:100] + "...", "vote": "FOR"}

# 6. Liquidation Warning
def check_liquidation(ltv):
    if ltv > 0.75:
        return {"status": "danger", "action": "add_collateral"}

# 7. NFT Assessment
def assess_nft(traits):
    rare_count = len([t for t in traits if t['rarity'] < 0.01])
    return {"rarity_score": rare_count * 10}

# 8. AML Check
def check_aml(address):
    if address in ["0xBlacklisted"]:
        return {"action": "reject", "flag": "high_risk"}

# 9. Depeg Alert
def check_peg(price):
    if abs(1.0 - price) > 0.01:
        return {"alert": "DEPEG", "execute": "drain_lp_pools"}

# 10. Portfolio Rebalance
def rebalance(current, target):
    diff = target - current
    return {"action": "buy" if diff > 0 else "sell", "amount": abs(diff)}
```
