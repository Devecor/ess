Geting Start
=================

配置环境变量
-----------------

==========  ======================================================  ========
变量名      值                                                      备注
==========  ======================================================  ========
SSDIR       ``\\ip\db-name``  比如: ``\\10.167.23.77\fbc_ci``       新建
Path        ``C:\Program Files (x86)\Microsoft Visual SourceSafe``  追加
==========  ======================================================  ========


执行第一个指令
-----------------

检查配置是否成功:``ss About``

.. code-block::

    C:\Users\cai.zfeng>ss About
    Microsoft(R) Visual SourceSafe Version 8.0
    Copyright (C) Microsoft Corporation. All rights reserved.
    
    
    C:\Users\cai.zfeng>

常见问题
------------------

1. 以下 ``SSDIR`` 配置错误，请检查环境变量

.. code-block::

    C:\Users\cai.zfeng>ss About
    Visual SourceSafe (VSS) のデータベース 初期化ファイル (srcsafe.ini) が見つかりません。VSS データベースの srcsafe.ini の パスへの SSDIR 環境変数を設定してください。
    
    C:\Users\cai.zfeng>

2. 以下 ``Path`` 追加错误，检查是否与vss安装目录一致

.. code-block::

    C:\Users\cai.zfeng>ss about
    'ss' は、内部コマンドまたは外部コマンド、
    操作可能なプログラムまたはバッチ ファイルとして認識されていません。


基本用法
===============

查看当前目录
---------------

.. code-block::

    ss dir

切换目录
---------------

.. code-block::

    ss cp <vss path>

.. tip::
    see :ref:`an example for cp`

取得文件
-------------

.. code-block::

    ss get <vss items>

.. tip::
    see :ref:`an example for get`

新建目录
---------------

.. code-block::

    ss create <dir name>

.. tip::
    see :ref:`an example for create`

在当前目录添加文件
------------------

.. code-block::

    ss add <local files>

.. tip::
    see :ref:`an example for add`

删除文件和文件夹
--------------------

.. code-block::

    ss delete <vss items>

.. tip::
    see :ref:`an example for delete`

签出文件 ``checkout``
--------------------------

.. code-block::

    ss checkout <vss files>

.. tip::
    see :ref:`an example for checkout`

签入文件 ``checkin``
---------------------------

.. code-block::

    ss checkin <file path in vss>

.. tip::
    see :ref:`an example for checkin`

取消签出文件 ``undocheckout``
---------------------------------

.. code-block::

    ss undocheckout <file path in vss>

.. tip::
    这意味着放弃该文件的任何修改

    see :ref:`an example for undocheckout`

vss常用工作流
=====================

独占模式下
-------------------------

=====================================          ==================
工作流                                         对象              
=====================================          ==================
``checkout  -->  edit  -->  checkin``          ``excel/text``        
``get``                                        ``excel/text/binary`` 
``get history  -->  compare``                  ``excel/text``        
``add``                                        ``excel/text/binary``
=====================================          ==================


并行模式下
----------------------

``Continuious updating...``
