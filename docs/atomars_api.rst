=================================
Atomars Python API Documentation
=================================


Before making any requests, you must first login:


::

    api = AtomarsAPI(username, password)
    await api.login()



Requesting balances
~~~~~~~~~~~~~~~~~~~~~

**get_balances(self, only_non_zero: bool = False) -> Dict:**

*Parameters:*

1. only_non_zero: boolean that determines whether to return only non zero balances or not


**Example:**

::

    <<
    await api.get_balances()
    >>
    'HLS': {'balance': 19957756355391,
         'balance_available': 19957756355391,
         'currency': {'iso3': 'HLS', 'name': 'Helios Protocol'}},
    'HOT': {'balance': 0,
         'balance_available': 0,
         'currency': {'iso3': 'HOT', 'name': 'Holo'}},
    ...


