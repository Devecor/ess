.. _an example for checkout:

Example for ``checkout``
-----------------------------

签出单个文件到当前的 **本地目录**

.. code-block::

    ss checkout $/testproject/t.py    // 绝对路径
    ss checkout testproject/t.py      // 相对路径

签出多个文件到当前的 **本地目录**

.. code-block::

    ss checkout t.py t.c

签出整个目录下的文件

.. code-block::

    ss checkout $/mydir              // 绝对路径
    ss checkout mydir                // 相对路径

.. important::
    但是不包含子目录, 除非使用 ``-r``

.. note::
    符号 ``$/`` 表示vss项目的根目录
