#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Class_FI_Dates import Dates
from Class_FI_MktData import MktData
from datetime import date


# In[2]:


class FinancialInstrument(MktData):
    """
    Parent class for all financial instruments.
    """

    def __init__(self, row):
        super().__init__()

        self.my_prod_type = row.my_prod_type
        self.my_name = row.my_name

        self.crypto_currency = row.crypto_currency
        self.quote_currency = row.quote_currency

        self.my_platform = row.my_platform
        self.platform_id = row.platform_id
        self.platform_symbol = row.platform_symbol
        self.platform_type = row.platform_type

        if self.platform_id == "IBKR":
            self.ibkr_conId = int(row.ibkr_conId)
            self.my_ibkr_id = (self.ibkr_conId)
            self.ibkr_contract = None
            self.ibkr_details = None

        self.comm_input_dict = {'type' : row.comm_type, 
                                'maker' : row.comm_maker,  
                                'taker' : row.comm_taker, 
                                'misc' : row.comm_misc} 

        self.settlement_days_dict  = {'trade' : int(row.settle_days_trade), "comm" : int(row.settle_days_comm)}

        if self.my_prod_type in ['future', 'option']:
            self.settlement_days_dict['expiry'] = int(row.settle_days_expiry)             


    def attach_dates(self):
        Dates.calc_and_attach(self)

