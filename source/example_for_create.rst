.. _an example for create:

Example for create
-------------------------

使用相对路径在当前目录创建子目录

.. code-block::

    ss create mydir -c-

使用绝对路径创建目录

.. code-block::

    ss create $/mydir -c-

.. note::
    默认情况下, 添加一个目录需要一个注释(comment), 如下

    .. code-block::
    
        D:\repo\vss-cmd> ss create $/mydir
        Comment for $/mydir:
    
    这将等待输入一行 ``comment``, **可使用** ``-c-`` **选项取消注释**
