.. _an example for add:

Example for ``add``
----------------------

添加单个文件到vss

.. code-block::

    ss add E:\repo\vss-cmd\test\text.txt -c-

添加当前目录下的所有文件到vss

.. code-block::

    ss add * -c-

递归添加当前目录及子目录下的所有文件到vss

.. code-block::

    ss add * -r -c-

.. note::
    默认情况下, 添加一个文件需要一个注释(comment), 如下

    .. code-block::
    
        D:\repo\vss-cmd> ss add test/test.txt
        Comment for test.txt:
    
    这将等待输入一行 ``comment``, **可使用** ``-c-`` **选项取消注释**