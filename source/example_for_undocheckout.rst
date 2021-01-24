.. _an example for undocheckout:

Example for undocheckout
-----------------------------

取消签出单个文件

.. code-block::

    ss undocheckout $/testproject/test.txt

取消签出多个文件

.. code-block::

    ss undocheckout test.txt test.c

取消当前目录的所有签出

.. code-block::

    ss undocheckout * -p

取消目标目录的所有签出

.. code-block::

    ss undocheckout mydir
    ss undocheckout $/mydir

.. note::
    仅 ``-p`` 标识当前目录

    以上两命令不影响子目录, 除非使用 ``-r``

.. warning::
    ``ss undocheckout *`` 的影响范围是整个目录, 慎用