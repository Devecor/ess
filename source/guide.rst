Geting Start
=================

配置环境变量
-----------------

==========  =============================================================  ========
变量名      值                                                             备注
==========  =============================================================  ========
SSDIR       ``\\ip\db-name``  for example: ``\\10.167.23.77\fbc_ci``       新建
Path        ``C:\Program Files (x86)\Microsoft Visual SourceSafe``         追加
==========  =============================================================  ========

检查配置是否成功:``ss About``::

    C:\Users\cai.zfeng>ss About
    Microsoft(R) Visual SourceSafe Version 8.0
    Copyright (C) Microsoft Corporation. All rights reserved.
    
    
    C:\Users\cai.zfeng>

常见问题
------------------

1. 以下 ``SSDIR`` 配置错误，请检查环境变量

.. code-block:: guess

    C:\Users\cai.zfeng>ss About
    Visual SourceSafe (VSS) のデータベース 初期化ファイル (srcsafe.ini) が見つかりません。VSS データベースの srcsafe.ini の パスへの SSDIR 環境変数を設定してください。
    
    C:\Users\cai.zfeng>

2. 以下 ``Path`` 追加错误，检查是否与vss安装目录一致

.. code-block:: guess

    C:\Users\cai.zfeng>ss About
    Visual SourceSafe (VSS) のデータベース 初期化ファイル (srcsafe.ini) が見つかりません。VSS データベースの srcsafe.ini の パスへの SSDIR 環境変数を設定してください。
    
    C:\Users\cai.zfeng>


基本用法
------------------

查看当前目录(类似 ``ls`` )::

    ss Dir

在当前目录添加文件::

    ss Add <local files>

查看示例 :ref:`example for Add`
