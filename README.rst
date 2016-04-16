===============================
bibletk
===============================

.. image:: https://img.shields.io/travis/jeroyang/bibletk.svg
        :target: https://travis-ci.org/jeroyang/bibletk

.. image:: https://img.shields.io/pypi/v/bibletk.svg
        :target: https://pypi.python.org/pypi/bibletk


Toolkit for bible
合和本聖經工具，給製作聖經經節簡報的辛苦同工。

作者
------
* 楊家融 <jeroyang@gmail.com>

使用方法
--------
* Installation
    $ pip install bibletk

* Make Powerpoint
將要作成聖經經節簡報的經文列表，存在一個純文字檔案中。
如 input.txt：

    創1:1-10
    創世記一章11-18
    出一1

在命令列輸入

    $ bibletk -i input.txt -o output.pptx

程式會自動產生一個 output.pptx 其中有我們想要的經文

軟體授權
-------
* Free software: MIT license
* Documentation: https://bibletk.readthedocs.org.
