1. Accept column mapping and cash flow type mapping inverted (reported_column: standard_column) and do the necessary
    changes in the code to make it work.
2. Create cash orders
3. Include trade, cash flow and cash order creation inside `Synchronizer`
4. Add to readme instructions how to synchronize `qkuk` and `skurs`
5. Create only new rows from the same file
6. Read excel with separate sheets for trades and cash flows
7. Synchronize sme_finance and growth-lending 
8. Include trade formulas in new trade django model (`apps.trades.models`)
