#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from datetime import datetime, timezone


# In[1]:


class MktData:

    def __init__(self):

        self.unit_scalar_dict = {'price' : 1.0, 'size' : 1.0, 'fee' : 0.0, 'date' : None}

        # Market data dictionary
        self.mkt_data_dict = {
            "bid_size": None,
            "bid_price": None,
            "ask_price": None,
            "ask_size": None,
            "timestamp": None
        }

        self.mkt_comm_dict = {
            "join_bid" : None,
            "join_ask" : None,
            "hit_bid" : None,
            "lift_ask" : None, 
            "timestamp": None
        }     

        # Unit data dictionary (price/size scaled to one unit)
        self.unit_data_dict = {
            "bid_size": None,
            "bid_price": None,
            "ask_price": None,
            "ask_size": None,
            "timestamp": None
        }

        self.unit_comm_dict = {
            "join_bid" : None,
            "join_ask" : None,
            "hit_bid" : None,
            "lift_ask" : None,  
            "timestamp": None
        }     

        self.unit_cf_dict = {
            "join_bid" : None,
            "join_ask" : None,
            "hit_bid" : None,
            "lift_ask" : None,  
            "timestamp": None
        }   

    def _to_float(self, x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None

    def update_mkt_data(self, bid_price=None, ask_price=None, bid_size=None, ask_size=None, misc=0):
        """
        Update price & size for the instrument.
        """    
        self.mkt_data_dict["timestamp"]  = datetime.now(timezone.utc)
        self.unit_data_dict["timestamp"] = self.mkt_data_dict["timestamp"]

        if bid_price is not None:
            bid_price = self._to_float(bid_price)
            self.mkt_data_dict["bid_price"]  = bid_price
            self.mkt_comm_dict['join_bid']   = self.calc_comm(self.mkt_data_dict["bid_price"], 
                                                              self.comm_input_dict['maker'])
            self.mkt_comm_dict['hit_bid']    = self.calc_comm(self.mkt_data_dict["bid_price"], 
                                                              self.comm_input_dict['taker'])
            self.unit_data_dict['bid_price'] = self.mkt_data_dict["bid_price"] * self.unit_scalar_dict['price']            
            self.unit_comm_dict['join_bid']  = self.mkt_comm_dict['join_bid'] * self.unit_scalar_dict['size']            
            self.unit_comm_dict['hit_bid']   = self.mkt_comm_dict['hit_bid'] * self.unit_scalar_dict['size'] 
            self.unit_cf_dict['join_bid']    = -self.unit_data_dict['bid_price'] - self.unit_comm_dict['join_bid']
            self.unit_cf_dict['hit_bid']     = self.unit_data_dict['bid_price'] - self.unit_comm_dict['hit_bid']
            self.mkt_comm_dict['timestamp']  = self.mkt_data_dict["timestamp"]
            self.mkt_comm_dict['timestamp']  = self.mkt_data_dict["timestamp"]


        if ask_price is not None:
            ask_price = self._to_float(ask_price)
            self.mkt_data_dict["ask_price"]  = ask_price
            self.mkt_comm_dict['join_ask']   = self.calc_comm(self.mkt_data_dict["ask_price"], 
                                                              self.comm_input_dict['maker'])
            self.mkt_comm_dict['lift_ask']   = self.calc_comm(self.mkt_data_dict["ask_price"], 
                                                              self.comm_input_dict['taker'])
            self.unit_data_dict['ask_price'] = self.mkt_data_dict["ask_price"] * self.unit_scalar_dict['price']
            self.unit_comm_dict['join_ask']  = self.mkt_comm_dict['join_ask'] * self.unit_scalar_dict['size'] 
            self.unit_comm_dict['lift_ask']  = self.mkt_comm_dict['lift_ask'] * self.unit_scalar_dict['size'] 
            self.unit_cf_dict['join_ask']    = self.unit_data_dict['ask_price'] - self.unit_comm_dict['join_ask']
            self.unit_cf_dict['lift_ask']    = -self.unit_data_dict['ask_price'] - self.unit_comm_dict['lift_ask']
            self.mkt_comm_dict['timestamp']  = self.mkt_data_dict["timestamp"]
            self.mkt_comm_dict['timestamp']  = self.mkt_data_dict["timestamp"]

        if bid_size is not None:
            bid_size  = self._to_float(bid_size)
            self.mkt_data_dict["bid_size"]  = bid_size
            self.unit_data_dict['bid_size'] = self.mkt_data_dict["bid_size"] / self.unit_scalar_dict['size']

        if ask_size is not None:
            ask_size  = self._to_float(ask_size)
            self.mkt_data_dict["ask_size"]  = ask_size
            self.unit_data_dict['ask_size'] = self.mkt_data_dict["ask_size"] / self.unit_scalar_dict['size']

    def calc_comm(self, price, amount):
        type_ = self.comm_input_dict['type']

        if type_ == 'flat_amt':
            return float(amount)
        elif type_ == 'flat_pct':
            return price * amount  
        elif type_ == 'flat_pct_with_min':
            initial_estimate = price * amount
            return max(initial_estimate, self.comm_input_dict['misc'])
        else:
            return 0


# In[ ]:


'''
    self.unit_cf_dict = {
            "join_bid": None,
            "join_ask": None,
            "hit_bid": None,
            "lift_ask": None,
            "timestamp": None
        }



        # NEW
        self._tick_listeners = []

    def add_tick_listener(self, listener):
        if listener not in self._tick_listeners:
            self._tick_listeners.append(listener)

    def remove_tick_listener(self, listener):
        if listener in self._tick_listeners:
            self._tick_listeners.remove(listener)

    def _notify_tick_listeners(self):
        for listener in tuple(self._tick_listeners):
            try:
                listener(self)
            except Exception as e:
                print(f"tick listener error on {getattr(self, 'my_name', 'unknown')}: {e}")

    def _to_float(self, x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None


changed = False
if bid_price != self.mkt_data_dict["bid_price"]:
                changed = True
if ask_price != self.mkt_data_dict["ask_price"]:
                changed = True
if bid_size != self.mkt_data_dict["bid_size"]:
                changed = True
if ask_size != self.mkt_data_dict["ask_size"]:
                changed = True   



if changed:
            self.mkt_data_dict["timestamp"] = now_ts
            self.unit_data_dict["timestamp"] = now_ts
            self.unit_cf_dict["timestamp"] = now_ts
            self._notify_tick_listeners()
'''

