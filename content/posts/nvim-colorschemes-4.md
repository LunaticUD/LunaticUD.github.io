---
title: "颜色界面——Colorschemes插件（四）"
slug: "nvim-colorschemes-4"
date: 2022-05-08T21:46:00+08:00
draft: false
tags: ["Neovim", "Vim", "主题"]
categories: ["Neovim 配置"]
summary: "在colors中新建colorscheme.vim和catppcuccin.vim文件"
ShowToc: true
TocOpen: false
hidemeta: false
comments: true
ShowReadingTime: true
ShowShareButtons: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

## 创建plugin、colors目录

在colors中新建colorscheme.vim和catppcuccin.vim文件

#### 在plugins.lua文件中加入

```powershell
-- Colorschemes主题
use "lunarvim/colorschemes" -- A bunch of colorschemes you can try out
use({
			"catppuccin/nvim",
			as = "catppuccin"
})
```

#### 重启nvim，按下<F2>键安装，安装完后在colorscheme.vim中加入

```powershell
local colorscheme = "catppuccin"
	-- require "user.conf.github-nvim-theme"
local status_ok, _ = pcall(vim.cmd, "colorscheme " .. colorscheme)
if not status_ok then
	vim.notify("colorscheme " .. colorscheme .. " not found!")
	return
end

if colorscheme == "onedark" then
	require "user.conf.onedark"
end
```

#### 在catppcuccin.vim中加入

```powershell
local status_ok, catppuccin = pcall(require, "catppuccin")
if not status_ok then
	return
end
```
