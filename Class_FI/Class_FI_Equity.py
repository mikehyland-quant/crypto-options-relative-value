#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Class_FI import FinancialInstrument


# In[ ]:


class Equity(FinancialInstrument):
    """
    Spot instrument class (child of FinancialInstrument).
    """
    def __init__(self, row):
        super().__init__(row)

        self.unit_scalar_dict = {'price' : row.price_scalar, 
                                 'size' : row.size_scalar, 
                                 'fee' : row.scalar_fee, 
                                 'date' : row.scalar_date}

