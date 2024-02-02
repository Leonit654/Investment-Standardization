1. Accept column mapping and cash flow type mapping inverted (reported_column: standard_column) and do the necessary
   changes in the code to make it work. [Done]
2. Create cash orders [Done]
3. Include trade, cash flow and cash order creation inside `Synchronizer` [Done]
4. Add instructions to readme:
    - setup project
    - run project
    - provide urls and payload for synchronizing `qkuk` and `skurs` [Done]
5. Pass trade upload data through a serializer (You might use `CashFlowInputSerializer`) [Done]
6. Add a `CashFlowSerializer` and `TradeSerializer` to validate sanitized data and create cash flows and trades in the
   database respectively [Done]
7. Add a django command `load_initial_data` which loads cash flow types and add it to README [Done]
8. Improve README by adding instructions to clone repo, create venv, install packages, load initial data,
   runserver [Done]

9. Read excel with separate sheets for trades and cash flows [Done]
10. Synchronize sme_finance and growth-lending [Done]
11. Add the following features:
    - add new column by merging different columns. For example there are `fee_amount` and `other_cost`
      in the cash flows dataset, and their sum (`fee_amount` + `other_cost`) represents cash flow `amount`.
    - Make this feature more general so user can take sum of two other columns, or multiply, or subtract [Done]

12. Include trade formulas in new trade django model (`apps.trades.models`) [Done]
13. Implement create only new trade or cash flow if it doesn't exist (without throwing error) [Done]
14. Make it possible for trades to use `values_to_replace` and `merge_columns` [Done]
15. Check integrity of data synchronization (Example qkuk cashflow with identifier = t_65837) [Done]
16. Optimize synchronization runtime [Done]
17. Insert data with no error, return error messages for rows with errors, possible with specific identifier
18. Return overall error messages.
19. Implement the view where user can upload trades and cash flows in separate files, and both of them are synchronized

