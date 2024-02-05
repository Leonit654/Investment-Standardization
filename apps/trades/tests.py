from services.tasks import synchronizer
# import pandas as pd
import os
import pandas as pd
import os

file_path = os.path.join("C:", "Users", "elton", "Desktop", "Trade Management", "data", "qkuk", "trades.xlsx")


trade = pd.read_excel("C:\\Users\\elton\\Desktop\\Trade Management\\data\\qkuk\\trades.xlsx" )
print(trade)


synchronizer.delay(file=trade,file_type="trade", columns_to_rename={
   "loan_id": "identifier",
   "issue_date":"issue_date",
   "maturity_date":"maturity_date",
   "purchase_amount":"invested_amount",
   "interest_rate_exp":"interest_rate"
})