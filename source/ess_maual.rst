.. _ess doc:

``ess`` 用户手册
=================


.. _ess install:

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

控制台没有报错表示安装成功,键入 ``ess -v`` 验证安装,如下表示安装正确

.. code-block::

    PS D:\repo\vss-cmd> ess -v
    ess 0.0.7-beta
    PS D:\repo\vss-cmd> 

异常的情况下, 请参考 :ref:`ess -v issue`

ess使用
--------------------

.. important::
    * 配置两个环境变量, 参考 :ref:`getting start`

1. 取得所有目录（一劳永逸的初始化）

.. tip::
    * 直接从vss取得所有文件，通常因为数据量太大而极度耗时，更遭的是会造成电脑卡死。
    * 所以只取得所有目录,不取文件

.. code-block::

    cd /d D:\vssroots\
    # 将vss当前目录置为根目录
    ss cp $/
    ess get -d -r

.. note::
    * 大型项目在根目录运行``ess get -d -r``仍然会卡住, 请使用 ``ess get -d``逐级取得
    * 在 ``PG`` , ``SS`` 这样的子目录中, 通常可以快速执行
    * 这是VSS的问题, 不是ess的问题, 后续版本会优化。

2. 典型场景使用参考 :ref:`workflow`
