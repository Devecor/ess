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