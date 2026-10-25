---
title: "我的Nvim配置——准备阶段（一）"
slug: "nvim-preparation-1"
date: 2022-04-20T23:13:00+08:00
draft: false
tags: ["Neovim", "Vim"]
categories: ["Neovim 配置"]
summary: "Neovim 配置系列第一篇：0.7.0 的下载安装，以及 XDG 配置目录的路径规则——后面所有配置都建立在这条路径上。"
ShowToc: true
TocOpen: false
hidemeta: false
comments: true
ShowReadingTime: true
ShowShareButtons: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

> **时效提示**：这个系列写于 2022 年，基于 Neovim 0.7 和 Packer。Packer 目前已停止维护，插件管理建议改用 [lazy.nvim](https://github.com/folke/lazy.nvim)，我现在的配置在 [LunaticUD/lazyvim](https://github.com/LunaticUD/lazyvim)。前面的配置路径、选项写法仍然适用。

## nvim下载

1. 在官网下载

下载[NVIM](https://github.com/neovim/neovim/releases/tag/v0.7.0)0.70版本

2. 使用包下载

a. windows下载

```powershell
scoop install neovim
```

b. mac下载

```bash
brew install neovim
```

c.apt包下载

```powershell
sudo apt install neovim
```

d.pacman包下载

```powershell
sudo pacman -Sy neovim
```

## Nvim环境配置

1.Windows下

在环境变量下设置

XDG\_CONFIG\_HOME=nvim的配置文件路经

XDG\_DATA\_HOME=nvim的配置文件路经

2.linux下在home目录的添加

`sudo makedir ~/.config/nvim`
