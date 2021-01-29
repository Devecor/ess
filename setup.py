# coding=utf-8

from setuptools import setup

'''
the install script for elegant-vss-command-line
'''

setup(
    name="ess",  #pypi中的名称，pip或者easy_install安装时使用的名称，或生成egg文件的名称
    version="0.0.1",
    author="蔡正鋒",
    author_email="devecor@outlook.com",
    description=("elegant vss command line"),
    license="MIT",
    keywords="ess",
    url="http://vss-cmd.devecor.cn",
    packages=['vsstool', 'vsstool/util'],  # 需要打包的目录列表

    # 需要安装的依赖
    install_requires=[
        # 'redis>=2.10.5',
        # 'setuptools>=16.0',
    ],

    python_requires='>=3.6',

    # 添加这个选项，在windows下Python目录的scripts下生成exe文件
    # 注意：模块与函数之间是冒号:
    entry_points={'console_scripts': [
        'ess = vsstool.ess:main',
    ]},

    # classifiers=[  # 程序的所属分类列表
    #     "Development Status :: 3 - Alpha",
    #     "Topic :: Utilities",
    #     "License :: OSI Approved :: GNU General Public License (GPL)",
    # ],
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
        #   'Environment :: Web Environment',
        #   'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
        #   'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Python Software Foundation License',
        #   'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
        #   'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Communications :: Email',
          'Topic :: Office/Business',
          'Topic :: Software Development :: Bug Tracking',
          ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False
)