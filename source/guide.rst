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

如何比GUI更高效
====================================

.. important:: 使用命令行需要一点技巧，否则非但不会提升效率，反而降低效率

1. 设定vss根目录的工作目录
---------------------------------

* 在本地新建一个文件夹 ``D:\\vssroots\``
* 将vss的根目录 ``$/`` 的工作目录设定为 ``D:\\vssroots\`` ，任何vss子目录不要设定工作目录，如果已经设定，请参考解决方案: :ref:`cancel work dir`
* 使用 ``ss get $/* -r`` 可以下载vss项目所有的文件和目录，但通常会因为数据量太大而极度耗时，更遭的是会造成电脑卡死
* 可按需下载当前需要使用的文件 ``ss get <vss items>``

2. 使用windows文件浏览器
------------------------------------

命令行没有可点击文件目录列表，这是非常致命的，一个良好的解决方案是直接使用windows的文件浏览器。


3. 打开命令行快速进入目标目录
---------------------------------

使用快捷键 ``shift + 鼠标右键`` -> 单击 ``PowerShellウインドウをここで開く（S）``

.. tip::
    常见问题：
    1. 子目录已经被设定了工作目录

vss常用工作流
=====================

独占模式下
-------------------------

=====================================          ======================        ====================
工作流                                         对象                          效率参考
=====================================          ======================        ====================
``checkout  -->  edit  -->  checkin``          ``excel/text``                
``get --> open``                               ``excel/text/binary``         see :ref:`get-open-workflow`
``get history  -->  compare``                  ``excel/text``                
``add``                                        ``excel/text/binary``         
=====================================          ======================        ====================


并行模式下
----------------------

``Continuious updating...``
