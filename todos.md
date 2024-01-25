1. Accept column mapping and cash flow type mapping inverted (reported_column: standard_column) and do the necessary
    changes in the code to make it work. [Done]
2. Create cash orders [Done]
3. Include trade, cash flow and cash order creation inside `Synchronizer` [Done]
4. Add instructions to readme:
   - setup project
   - run project
   - provide urls and payload for synchronizing `qkuk` and `skurs`
5. Pass trade upload data through a serializer (You might use `CashFlowInputSerializer`.
6. Add a `CashFlowSerializer` and `TradeSerializer` to validate sanitized data and create cash flows and trades in the 
   database respectively 

5. Create only new rows from the same file
6. Read excel with separate sheets for trades and cash flows
7. Synchronize sme_finance and growth-lending 
8. Include trade formulas in new trade django model (`apps.trades.models`)
9. Add a django command `load_initial_data` which loads cash flow types and add it to README
10. Improve README by adding instructions to clone repo, create venv, install packages, load initial data, runserver
