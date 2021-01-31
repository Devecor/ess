.. _get-open-workflow:

``Get --> Open``
=====================

1. 在文件管理其中打开目标目录

2. 打开 ``powerShell`` 命令行快速进入目标目录

``shift + 鼠标右键`` -> 单击 ``PowerShellウインドウをここで開く（S）``

3. 键入命令 ``ess -s``

4. 回到文件浏览器双击打开文件

.. important::
    * 上述操作要求目标目录存在
    * 要解决这个问题, 提前进入根目录 ``D:\vssroots``
      (这是示例,具体目录取决于你的配置), 键入以下命令
      
    .. code-block::
      
        ss cp $/
        ess get -d -r
