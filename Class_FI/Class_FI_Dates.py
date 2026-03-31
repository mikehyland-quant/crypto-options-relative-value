#!/usr/bin/env python
# coding: utf-8

# In[1]:


#imports
from datetime import datetime, time, timedelta, date
from dateutil import parser
from zoneinfo import ZoneInfo

import numbers

import pandas_market_calendars as mcal
_NYSE = mcal.get_calendar("NYSE")   # module-level, built once


# In[2]:


class Dates():
    """
    Build date-related fields for a simple instrument without mutating it.
    """
    '''
    called for simple contracts (not BAGs) from 
    Class_IBKRCleint at 
    async def create_simple_contract(self, obj):
    '''

    @staticmethod
    def calc(obj):  
        trade_date                              = date.today()

        settlement_dates_dict                   = {}

        date_comm_pmt                           = trade_date + timedelta(days=obj.settlement_days_dict["comm"])
        settlement_dates_dict['comm']           = Dates.next_nyse_trading_day(date_comm_pmt)

        time_diff                               = obj.settlement_days_dict["trade"] - obj.settlement_days_dict["comm"]
        date_trade_pmt                          = settlement_dates_dict['comm'] + timedelta(days=time_diff)
        settlement_dates_dict['trade']          = Dates.next_nyse_trading_day(date_trade_pmt)

        calendar_days_dict                      = {'trade' : None, "comm" : None}
        calendar_days_dict['comm']              = (settlement_dates_dict['comm'] - trade_date).days
        calendar_days_dict['trade']             = (settlement_dates_dict['trade'] - trade_date).days

        expiration_date                         = None
        last_trade_date_time_nyc                = None

        if obj.my_prod_type in ['future', 'option']:
### need if IBKR statement here        
            expiration_date                     = Dates.date_from_string(obj.ibkr_details.realExpirationDate)  

            date_expiry_pmt                     = expiration_date + timedelta(days=obj.settlement_days_dict["expiry"])
            settlement_dates_dict['expiry']     = Dates.next_nyse_trading_day(date_expiry_pmt)

            tz_exch                             = ZoneInfo(obj.ibkr_details.timeZoneId)
            tz_nyc                              = ZoneInfo("America/New_York")

            last_trade_time                     = Dates.time_from_number(obj.ibkr_details.lastTradeTime, 24)
            if last_trade_time is None:
                last_trade_time                 = Dates.time_from_string('16:00')

            last_trade_date_time_exch           = datetime.combine(expiration_date, last_trade_time, tzinfo=tz_exch)          
            last_trade_date_time_nyc            = last_trade_date_time_exch.astimezone(tz_nyc)

            calendar_days_dict['expiry']       = (settlement_dates_dict['expiry'] - trade_date).days

        return {
            'trade_date': trade_date,
            'settlement_dates_dict': settlement_dates_dict,
            'calendar_days_dict': calendar_days_dict,
            'expiration_date': expiration_date,
            'last_trade_date_time_nyc': last_trade_date_time_nyc,
        }


    @staticmethod
    def calc_and_attach(obj):        
        results_dict = Dates.calc(obj)

        obj.trade_date                             = results_dict['trade_date']    
        obj.settlement_dates_dict                  = results_dict['settlement_dates_dict'] 
        obj.calendar_days_dict                     = results_dict['calendar_days_dict'] 
        obj.expiration_date                        = results_dict['expiration_date'] 
        obj.last_trade_date_time_nyc               = results_dict['last_trade_date_time_nyc'] 


    @staticmethod
    def date_from_string(date_string): 
        if isinstance(date_string, str) and date_string.strip():
            answer = parser.parse(date_string)
            return answer.date()
        else:
            return None


    @staticmethod
    def time_from_string(time_string):
        if isinstance(time_string, str) and time_string.strip():
            h, m = map(int, time_string.split(":"))
            return time(hour=h, minute=m)
        else:
            return None


    @staticmethod
    def time_from_number(time_number, multiplier=1): 
        if isinstance(time_number, numbers.Real):
            product =  time_number * multiplier            
            hours = int(product) % 24
            minutes = int(round((product - int(product)) * 60))

            # handle rounding edge case (e.g. 1.999 -> 2:00)
            if minutes == 60:
                hours = (hours + 1) % 24
                minutes = 0

            return time(hour=hours, minute=minutes)        
        else:
            return None


    @staticmethod
    def next_nyse_trading_day(date_):
        if date_ is not None:
            schedule = _NYSE.valid_days(start_date=date_, end_date=date_ + timedelta(days=10))
            return schedule[schedule.date >= date_].min().date()
        return None            

