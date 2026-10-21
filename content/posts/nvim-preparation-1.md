---
title: "我的Nvim配置——准备阶段（一）"
slug: "nvim-preparation-1"
date: 2022-04-20T23:13:00+08:00
draft: false
tags: ["Neovim", "Vim"]
categories: ["Neovim 配置"]
summary: "XDGCONFIGHOME=nvim的配置文件路经"
ShowToc: true
TocOpen: false
hidemeta: false
comments: true
ShowReadingTime: true
ShowShareButtons: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

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
