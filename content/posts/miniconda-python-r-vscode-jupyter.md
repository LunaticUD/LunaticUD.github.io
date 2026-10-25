---
title: "Miniconda安装python和r构建vscode-jupyter"
slug: "miniconda-python-r-vscode-jupyter"
date: 2024-12-17T23:05:00+08:00
draft: false
tags: ["Python", "R", "Conda", "VSCode"]
categories: ["环境配置"]
summary: "在 Windows 上用 Miniconda 建一个同时装 Python 3.9 和 R 的虚拟环境，注册成 VSCode 的 Jupyter 内核，附完整命令、内核切换和 settings.json。"
ShowToc: true
TocOpen: false
hidemeta: false
comments: true
ShowReadingTime: true
ShowShareButtons: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

## 引言：

> 就个人而言，首先本人更喜欢手动配置自己需要的东西，不想带一些不需要的包，多少有些洁癖，其次本人更喜欢一体化的去管理一个项目，miniconda正是我现在寻找的一项选择。本文仅供记录和参考

## 软件准备及安装

### [Miniconda的安装](https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Windows-x86_64.exe)

![](/images/posts/miniconda-python-r-vscode-jupyter/01.png)

### [Visual Studio Code的安装](https://code.visualstudio.com/docs/?dv=win64user)

![](/images/posts/miniconda-python-r-vscode-jupyter/02.png)

## Miniconda的安装python和R

```bash
# 创建一个虚拟环境并安装python和R指定版本和包
conda create -n data python=3.9 ipykernel conda-forge::r-base r-essentials
# ipykernel配置添加jupyter内核
python -m ipykernel install --user --name data
# 进入r解释器配置vscode的jupyter内核
R.exe
install.packages('IRkernel')
IRkernel::installspec()
# 为jupyter网页版添加python-lsp和R-lsp
conda install -c conda-forge python-lsp-server r-languageserver jupyterlab-lsp
# kernelspec配置删除内核
jupyter kernelspec list
jupyter kernelspec remove data
```

## 切换内核

### 打开一个\*.ipynb文本文件

![](/images/posts/miniconda-python-r-vscode-jupyter/03.png)

### 右上角显示选择内核点击

![](/images/posts/miniconda-python-r-vscode-jupyter/04.png)

### 切换内核

![](/images/posts/miniconda-python-r-vscode-jupyter/05.png)

## 配置Vscode

### Setting.json文件配置

```json
{
    "workbench.startupEditor": "none",
    "window.menuBarVisibility": "toggle",
    "window.commandCenter": false,
    "chat.commandCenter.enabled": false,
    "explorer.confirmDelete": false,
    "files.autoSave": "afterDelay",
    "update.mode": "none",
    "editor.fontSize": 18, // 字号
    "editor.fontFamily": "JetBrains Mono, Consolas, 'Courier New'", // 字体
    "editor.lineNumbers": "relative", // 相对行号
    "editor.lineHeight": 27, // 行高
    "python.analysis.completeFunctionParens": true,  // 让它补全函数名时自动加括号
    "python.analysis.autoSearchPaths": true,  // 自动搜索项目路径下的库
    "terminal.integrated.defaultProfile.windows": "Windows PowerShell", // 配置终端   
    "editor.quickSuggestions": {
        "comments": "off",
        "strings": "off",
        "other": "on"
    },
    "editor.hover.enabled": false,
    "editor.parameterHints.enabled": false,
    "workbench.iconTheme": "vscode-jetbrains-icon-theme-2023-auto",
    "jupyter.askForKernelRestart": false,
    "workbench.activityBar.location": "bottom",
    "workbench.layoutControl.enabled": false,
    "explorer.confirmDragAndDrop": false,
    "breadcrumbs.enabled": false
}
```

### 必要插件安装

#### Python；

![](/images/posts/miniconda-python-r-vscode-jupyter/06.png)

  
jupyter；  

![](/images/posts/miniconda-python-r-vscode-jupyter/07.png)

#### R；

![](/images/posts/miniconda-python-r-vscode-jupyter/08.png)

### 美化插件

![](/images/posts/miniconda-python-r-vscode-jupyter/09.png)

![](/images/posts/miniconda-python-r-vscode-jupyter/10.png)

## 尽情享受吧！

![](/images/posts/miniconda-python-r-vscode-jupyter/11.png)

![](/images/posts/miniconda-python-r-vscode-jupyter/12.png)
