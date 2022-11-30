---
Date: 2022-11-30
Update: 2022-11-30
Author: 目棃
Description: 说明文档
---

> 本文档 [`Front-matter`](https://github.com/BTMuli/Mucli#FrontMatter) 由 [MuCli](https://github.com/BTMuli/Mucli) 自动生成于
`2022-11-30 23:34:11`

## 前言

本项目起源于某次计网实验，要求实现 TCP 点对点通信，详见：[PythonSocket通信小试 | 棃星落月](https://next.btmuli.top/posts/2022/11/1f937280.html)。

## 配置说明

项目依赖见 [`requirements.txt`](requirements.txt)。

使用如下命令导出：

```bash
pip freeze > requirements.txt
```

使用如下命令安装：

```bash
pip install -r requirements.txt
```

## 打包说明

项目采用 Pyinstaller 打包，运行命令如下：

```bash
pyinstaller -F app.py -i lib/cover.ico --distpath .
```

## Release

项目打包后的可执行文件见 [Release](https://github.com/BTMuli/socket_demo/releases)。

## License

本项目采用 [MIT](LICENSE) 协议开源。
