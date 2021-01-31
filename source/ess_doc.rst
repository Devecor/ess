.. _ess doc:

``ess`` 用户手册
==============

``ess`` 简介
---------------

**ess : an elegant command tool for vss by cai.zfeng**

1. ``ess`` 为反人类的 ``vss`` 文件目录和经常卡死的 ``vss`` 客户端而生
2. 同时, ``ess`` 也为效率而生
3. 为了效率, 用户应该接受和学习这种新的工作方式: :ref:`more efficient`

``ess`` 安装
---------------

1. 安装 ``Python``

安装过程中记得勾选 ``add to path`` 选项,安装完成后,命令行中键入 ``python -V`` 如下表示安装成功

.. code-block::

    PS D:\repo\vss-cmd> python -V
    Python 3.8.1

2. 下载并安装 ``ess``

* 下载 ``ess`` : `clik here to Download <https://github.com/flow-edge/vss-cmd/releases/tag/0.0.7-beta>`_
* 使用以下命令之一安装:

.. code-block::

    python -m pip install C:\Users\p\Downloads\ess-0.0.7b0.tar.gz
    # 或者
    python -m pip install C:\Users\p\Downloads\ess-0.0.7b0-py3-none-any.whl
    # 或者
    pip install C:\Users\p\Downloads\ess-0.0.7b0.tar.gz
    # 或者
    pip install C:\Users\p\Downloads\ess-0.0.7b0-py3-none-any.whl

控制台没有报错表示安装成功,键入 ``ess -h`` 验证安装,如下表示安装正确

.. code-block::

    PS D:\repo\vss-cmd\dist> ess -h
    usage: ess [-h] [-v] [-s] [-l] [--debug] {get,cho,chi,ucho} ...

    here is an elegant command tool for vss by cai.zfeng. enjoy!

    positional arguments:
    {get,cho,chi,ucho}  elegant sub cmd
        get               从vss上取得最新文件（仅当前目录）
        cho               checkout
        chi               checkin
        ucho              undocheckout

    optional arguments:
    -h, --help          show this help message and exit
    -v, --version       查看当前版本
    -s, --sync-dir      同步cwd和所有文件（不含子目录）
    -l, --list          列出当前目录下的所有文件
    --debug             debug模式

ess使用
--------------------

.. important::
    除 ``-h`` 和 ``-v`` 外,所有 ``ess`` 命令都基于一个sync命令 ``ess -s``,
    因此,请首先sync.

1. 取得所有目录（一劳永逸的初始化）

.. tip::
    * 直接从vss取得所有文件，通常因为数据量太大而极度耗时，更遭的是会造成电脑卡死。
    * 所以只取得所有目录,不取文件

.. code-block::

    cd /d D:\vssroots\
    # 将vss当前目录置为根目录
    ss cp $/
    ess get -d -r

2. sync当前目录（一切之始）

.. tip::
    * 同步vss的当前目录（cwd）和取最新文件
    * ess所有命令都要求先执行此命令（ ``-h`` 和 ``-v`` 除外）

.. code-block::
    
    ess -s

3. 典型场景使用参考 :ref:`workflow`
