``ess`` 简介
===============

an elegant cmd tool for vss by cai.zfeng
----------------------------------------------

1. ``ess`` 为反人类的 ``vss`` 文件目录和经常卡死的 ``vss`` 客户端而生
2. 同时, ``ess`` 也为效率而生, 参考 :ref:`more efficient`

下面是一个使用演示：

.. image:: ../video/checkout.gif
   :width: 80%


.. _getting start:

Geting Start
=================

配置环境变量
-----------------

==========  ======================================================  ========
变量名      值                                                      备注
==========  ======================================================  ========
SSDIR       ``\\ip\db-name``  比如: ``\\192.168.1.104\vssdb``       新建
Path        ``C:\Program Files (x86)\Microsoft Visual SourceSafe``  追加
==========  ======================================================  ========


检查配置是否成功
------------------

使用 ``ss whoami``

.. code-block::

    C:\Users\cai.zfeng>ss whoami
    cai.zfeng
    C:\Users\cai.zfeng>

失败请参考 :ref:`ss whoami`

``ess`` 安装
=======================

安装请参考用户手册 :ref:`ess install`

.. _more efficient:

如何比GUI更高效
====================================

.. important:: 使用命令行需要一点技巧，否则非但不会提升效率，反而降低效率

1. 设定vss根目录的工作目录
---------------------------------

* 在本地新建一个文件夹 ``D:\\vssroots\``
* 将vss的根目录 ``$/`` 的工作目录设定为 ``D:\\vssroots\`` ，任何vss子目录不要设定工作目录，如果已经设定，请参考解决方案: :ref:`cancel work dir`

2. 使用windows文件浏览器
------------------------------------

命令行没有可点击文件目录列表，这是非常致命的，一个良好的解决方案是配合windows的文件浏览器使用。

3. 打开命令行快速进入目标目录
---------------------------------

* 从window文件浏览器进入目标目录, 执行 ``ess`` 命令
* ``shift + 鼠标右键`` -> 单击 ``PowerShellウインドウをここで開く（S）``

.. _workflow:

vss常用工作流
=====================

独占模式下
-------------------------

=====================================          ======================        ====================
工作流                                         对象                          效率参考
=====================================          ======================        ====================
``checkout  -->  edit  -->  checkin``          ``excel/text``                see :ref:`checkout-checkin-workflow`
``checkout  -->  undo checkout``               ``excel/text``                see :ref:`checkout-undocheckout-workflow`
``get --> open``                               ``excel/text/binary``         see :ref:`get-open-workflow`
``get history  -->  compare``                  ``excel/text``
``add``                                        ``excel/text/binary``
=====================================          ======================        ====================


并行模式下
----------------------

``Continuious updating...``

附录1：ss基本用法
==================

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
