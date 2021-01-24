.. _an example for get:

Example for get
-------------------------

取得单个文件

.. code-block::

    ss get $/mydir/guide.txt        // 绝对路径
    ss get mydir/guide.txt          // 相对路径

取得目录下的所有文件（不含子目录）

.. code-block::

    ss get mydir

.. note::
    若本地中 ``mydir`` 目录不存在, vss会提示你创建

    还会提示是否将本地的 ``mydir`` 目录作为vss的 ``mydir`` 项目的默认文件夹

取得vss当前目录下的所有文件（不含子目录）

.. code-block::

    ss get *

取得项目全部文件

.. code-block::

    ss get $/* -r

.. note:: 加 ``-r`` 表示递归的取得子目录下的所有文件

取得历史版本

.. important:: vss中任何一个文件夹都是一个项目/子项目


