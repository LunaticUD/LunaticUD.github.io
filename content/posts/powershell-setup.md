---
title: "powershell配置"
slug: "powershell-setup"
date: 2024-12-11T17:03:00+08:00
draft: false
tags: ["PowerShell", "Windows"]
categories: ["环境配置"]
summary: "函数中创建变量$curdir写入路径；路径由Split以“”分割，只取最后一个，以设置简洁路径"
ShowToc: true
TocOpen: false
hidemeta: false
comments: true
ShowReadingTime: true
ShowShareButtons: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

## powershell配置

## 0.结果展示

![](/images/posts/powershell-setup/01.png)

  

![](/images/posts/powershell-setup/02.png)

## 1.配置输出符号

```powershell
function Prompt {
		$curdir = "$(Get-Location)".Split("\") | Select-Object -Last 1
		return "⚡" + $curdir + "💨"
}
```

> 先创建函数  
> 函数中创建变量$curdir写入路径；路径由Split以“\”分割，只取最后一个，以设置简洁路径  
> 返回

## 2.配置命令

### rm -rf

```
function rmrf ($dir_path){
  Remove-Item -Recurse -Force $dir_path
}
```

### mv

```
function mv($file_path, $des_name) {
  Move-Item -Path $file_path -Destination $des_name
}
```

### head

```
function head($dir_path, $num){
		type $dir_path | Select -First $num
}
```

### tail

```
function tail($dir_path, $num){
		type $dir_path | Select -Last $num
}
```

## 3.配置lsd

### 下载lsd

1. scoop下载  
   `scoop install lsd`
2. 网页下载  
   lsd:  
   github:https://github.com/lsd-rs/lsd  
   gitcode:https://gitcode.com/gh\_mirrors/lsd/lsd/overview

### 配置lsd

```
function l{
		lsd.exe -l
}
function la{
		lsd.exe -a
}
function lla{
		lsd.exe -la
}
function lt{
		lsd.exe --tree
}
```

## 4.创建永久别名

```powershell
# 更改别名
Remove-Item alias:ls
Set-Alias -Name ls -Value lsd.exe
```

## 5.更改文件编码

将配置文件另存为UTF-16LE编码保存
