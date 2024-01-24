from .synchronizer import Synchronizer
import pandas as pd
from typing import Literal


class CashFlowSynchronizer(Synchronizer):
    def __init__(self, file, file_type: Literal["cash_flow"], df, columns_to_rename):
        super().__init__(file, file_type, columns_to_rename)
        self.df = df

    def get_cash_flow_type(self):
        return self.df["cash_flow_type"].unique()

    def filtered_cash_flow_type_dataframe(self, column_name, filter=None, is_na=False):
        if is_na == False:
            return self.df[self.df[column_name] == filter]
        else:
            return self.df[~self.df[column_name].isna()]

    def cash_order_df(self):
        df = self.filtered_cash_flow_type_dataframe("cash_flow_type", "cash_order", is_na=False)
        df.loc[df['amount'] > 0, 'cash_flow_type'] = 'deposit'
        df.loc[df['amount'] <= 0, 'cash_flow_type'] = 'withdrawal'
        df.drop(columns=['trade_identifier'], inplace=True)
        return df

    def run(self):
        df = super().run()
