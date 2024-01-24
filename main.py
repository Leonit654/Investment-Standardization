import pandas as pd

from services.sanitization import Sanitizer

path = "/home/qendrim/data/originators/impact_factoring/cmp_ah/impact_factoring_trades_cmp_ah.csv"
df = pd.read_csv(path)
df = df.rename(columns=lambda x: x.strip())
sanitizer = Sanitizer(
    df,
    data_type_mapping={
        "float": [
            'default_amount',
            'expected_net_return',
            'outstanding_principal_amount',
            'purchase_amount',
            'rollovered_amount',
            'trade_receivable_amount',
            'write_off_amount',
            "cash_allocated"
        ],
        "percentage": ['interest_rate_exp'],
        "date": ["trade_receivable_date", "due_date", "extension_date"]
    })

sanitizer.run()

df = sanitizer.df
a = 2

