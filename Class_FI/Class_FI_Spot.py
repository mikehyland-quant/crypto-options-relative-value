#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Class_FI import FinancialInstrument


# In[ ]:


class Spot(FinancialInstrument):
    """
    Spot instrument class (child of FinancialInstrument).
    """
    def __init__(self, row):
        super().__init__(row)



