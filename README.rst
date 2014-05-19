IoT Relay - TempoDB: A TempoDB Plugin for IoT Relay
========================================================================
Release v1.0.1

iotrelay-tempodb is a data handler plugin for IoT Relay. It watches for
data it has registered an interest in and relays it in batches to a
TempoDB time series database.

iotrelay-tempodb is available on PyPI and can be installed via pip.

.. code-block:: bash

    $ pip install iotrelay-tempodb

Before using iotrelay-tempodb an TempoDB account and database must be
created. See https://tempo-db.com/ for more. Add API key and API Secret
to the IOT Relay configuration file, ``~/.iotrelay.cfg`` once they have
been given by TempoDB.

.. code-block:: ini

    [iotrelay-tempodb]
    api key = your api key
    api secret = your api secret

The ``reading types`` to be relayed to TempoDB should also be
registered. In this example, reading types of power and weather will be
relayed to TempoDB.

.. code-blcok:: ini

    [iotrelay-tempodb]
    reading types = power, weather
    api key = your api key
    api secret = your api secret

By default iotrelay-tempodb will batch 30 readings of each type before
sending the batch to TempoDB. In the previous example, two separate
batches would be maintained for power and weather readings. The batch
size may be changed by adding the ``batch size`` option to the
``iotrelay-tempodb`` section of ``~/.iotrelay.cfg``.

.. code-blcok:: ini

    [iotrelay-tempodb]
    batch size = 30
    reading types = power, weather
    api key = your api key
    api secret = your api secret


Copyright © 2014, Emmanuel Levijarvi
All rights reserved.
