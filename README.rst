======================
Atomars Alterdice API
======================

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
    :target: https://www.python.org/downloads/release/python-360/
    :alt: Python3.6



This is an unofficial python API for Atomars and Alterdice exchanges.

Install
-------

1)  Clone this repo

    .. code:: bash

        $ cd ~/
        $ git clone https://github.com/hyperevo/Atomars-alterdice-API


2)  Install using pip

    .. code:: bash

        $ cd Atomars-alterdice-API
        $ pip3 install -e .


Usage
---------
Note: Many of the functions in the API are async. So you have to use await or ensure_future etc... To use the API in another python program, first import asyncio and the API, then login using your username and password, then call whatever function you would like. Because the API is asyncio, we will need to do this within a class so that we can "await" for functions to complete. Here is a simple example to get the balances:

    .. code:: python

        import asyncio
        from atom_alter_API.api import AtomarsAlterdiceAPI

        class TestClass():

            def __init__(self):
                self.api = AtomarsAlterdiceAPI(API_login_username, API_login_password)

            async def run(self):
                await self.api.login()
                balances = await self.api.get_balances()
                print(balances)

        if __name__ == "__main__":

            testClass = TestClass()
            asyncio.ensure_future(testClass.run())

            loop = asyncio.get_event_loop()
            loop.run_forever()
            loop.close()



See the docs folder for more info. Also see tests for some more code examples.