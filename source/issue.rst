.. _ss whoami:

``SSDIR`` 配置问题
=====================

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

.. _cancel work dir:

取消工作目录设定
=========================

若子目录的工作目录被设定, 通常不能通过vss客户端取消。

可通过修改用户配置文件解决:
``\\192.168.1.104\<vssdb name>\users\<user name>\ss.ini``

.. code-block:: ini

    ...
    Diff_Format = visual
    Diff_Ignore = w-c-e
    Hist_Rect (LAPTOP-GP9FKOKR) = 552, 411, 1512, 1027, 1920, 1080
    History_File_Columns (UI) = 75,85,135,100
    Visual_Diff_Max (LAPTOP-GP9FKOKR) = No
    Visual_Diff_Rect (LAPTOP-GP9FKOKR) = 312, 280, 1752, 1050, 1920, 1080

    [$/]
    Dir (LAPTOP-GP9FKOKR) = D:\repo\vss-cmd\test

    [$/mydir]
    Dir (LAPTOP-GP9FKOKR) = D:\repo\vss-cmd\source

删除多余的 ``Dir`` 配置, 独留vss根目录的配置, 如下所示:

.. code-block:: ini

    [$/]
    Dir (LAPTOP-GP9FKOKR) = D:\repo\vss-cmd\test

最后保存即可


.. _ess -v issue:

``ess -v`` 问题
====================

1. 确认 ``ess`` 是否安装,
使用 ``python -m pip list | findstr ess``

.. code-block::

    PS D:\repo\vss-cmd> python -m pip list | findstr ess   
    ess                           0.0.7b0   
    PS D:\repo\vss-cmd>

如上图出现当前版本号表示已经安装, 若没有请先安装

2. 查看安装位置 ``python -m pip show ess | findstr Location``

3. 安装路径中有个 ``site-packages`` 目录
将与之同级的 ``Scripts`` 目录加入到 ``Path`` 变量

4. 重新打开 ``PowerShell`` 或者 ``cmd`` 或者终端, 运行 ``ess -v``