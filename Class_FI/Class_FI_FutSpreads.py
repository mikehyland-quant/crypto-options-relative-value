#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from itertools import combinations
from Class_FI_MktData import MktData


# In[ ]:


class FutureSpread(MktData):
    """
    FutureSpread instrument class (NOT a child of FinancialInstrument).
    """
    def __init__(self, obj1, obj2):
        super().__init__()
        self.near_obj, self.far_obj = self.determine_near_far(obj1, obj2)

        self.my_prod_type = 'future_spread' 
        self.my_name = f"{self.near_obj.my_name}/{self.far_obj.my_name}"

        self.copy_common_fields_from(self.near_obj)

        if self.platform_id == "IBKR":        
#            self.ibkr_conId = None
            self.my_ibkr_id = tuple(sorted([self.near_obj.ibkr_conId, self.far_obj.ibkr_conId]))
            self.ibkr_contract = None
#            self.ibkr_details = None

        self.expiration_date_near = self.near_obj.expiration_date
        self.expiration_date_far = self.far_obj.expiration_date

        self.comm_input_dict['maker'] = self.near_obj.comm_input_dict['maker'] + self.far_obj.comm_input_dict['maker']  
        self.comm_input_dict['taker'] = self.near_obj.comm_input_dict['taker'] + self.far_obj.comm_input_dict['taker'] 

        for attr in ['settlement_dates_dict', 'calendar_days_dict']:
            d = getattr(self, attr)
            near_d = getattr(self.near_obj, attr)
            far_d = getattr(self.far_obj, attr)

            d['near_expiry'] = near_d['expiry']
            d['far_expiry'] = far_d['expiry']
            d.pop('expiry', None)

        self.calendar_days_dict['far-near'] = self.calendar_days_dict['far_expiry'] - self.calendar_days_dict['near_expiry']


    def determine_near_far(self, obj1, obj2):
        if obj1.expiration_date < obj2.expiration_date:
            return obj1, obj2
        else:
            return obj2, obj1   


    def copy_common_fields_from(self, source_obj):
        """
        Copy common instrument/platform fields from a simple instrument,
        usually the near leg.
        """
        fields_to_copy = [
            'crypto_currency',
            'quote_currency',
            'my_platform',
            'platform_id',
            #'platform_symbol',
            #'platform_type',
            'trade_date',
            'last_trade_date_time_nyc',
        ]

        for field in fields_to_copy:
            setattr(self, field, getattr(source_obj, field))

        # Copy mutable dicts so spread does not share state with near leg
        self.unit_scalar_dict = source_obj.unit_scalar_dict.copy()
        self.comm_input_dict = source_obj.comm_input_dict.copy()
        self.settlement_dates_dict = source_obj.settlement_dates_dict.copy()
        self.calendar_days_dict = source_obj.calendar_days_dict.copy()   


    @staticmethod
    def make_futures_spreads(list_):
        futures_list = [obj for obj in list_ if obj.my_prod_type == 'future']
        fut_spd_pairs_list = list(combinations(futures_list, 2))
        fut_spd_obj_list = [FutureSpread(pair[0], pair[1]) for pair in fut_spd_pairs_list]

        return fut_spd_obj_list



# In[ ]:





# In[ ]:




