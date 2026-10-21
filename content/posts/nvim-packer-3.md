---
title: "我的Nvim——packer.nvim插件管理器（三）"
slug: "nvim-packer-3"
date: 2022-04-28T09:03:00+08:00
draft: false
tags: ["Neovim", "Vim", "插件"]
categories: ["Neovim 配置"]
summary: "a. Unix, Linux Installation"
ShowToc: true
TocOpen: false
hidemeta: false
comments: true
ShowReadingTime: true
ShowShareButtons: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

## 1. 安装

#### a. Unix, Linux Installation

```bash
git clone --depth 1 https://github.com/wbthomason/packer.nvim\
 ~/.local/share/nvim/site/pack/packer/start/packer.nvim
```

#### b. Windows Powershell Installation

```bash
# 默认
git clone https://github.com/wbthomason/packer.nvim "$env:LOCALAPPDATA\nvim-data\site\pack\packer\start\packer.nvim"
# 或者
git clone https://github.com/wbthomason/packer.nvim "$env:XDG_DATA_HOME\nvim-data\site\pack\packer\start\packer.nvim"
```

## 2.配置

在配置路径中创建lua文件夹，并在文件夹下创建plugins.lua文件

在plugins.lua中写入

```powershell
return require('packer').startup({
	function()
		-- Packer can manage itself
		use 'wbthomason/packer.nvim'
        -- {添加插件}

	end,
	config = {
		max_jobs = 16,
		display = {
			open_fn = function()
				return require('packer.util').float({ border = 'single' })
			end
		}
	}
})
```

![](/images/posts/nvim-packer-3/01.png)
