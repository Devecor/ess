.. _an example for checkin:

Example for ``checkin``
------------------------------

签入单个文件

.. code-block::

    ss checkin $/testproject/t.py -c-
    ss checkin t.py -c-

.. note::
    默认情况下, 签入一个文件需要一个注释(comment), 如下

    .. code-block::
    
        D:\repo\vss-cmd> ss checkin test/test.txt
        Comment for test.txt:
    
    这将等待输入一行 ``comment``, **可使用** ``-c-`` **选项取消注释**