---
title: "Windows下的软件编译与测序质控"
slug: "windows-software-build-qc"
date: 2025-10-05T17:30:00+08:00
draft: false
tags: ["生信", "Windows", "质控"]
categories: ["生信分析"]
summary: "MSYS2 是基于Cygwin软件开发而来的工具和库的集合，为您提供了一个易于使用的环境，用于构建、安装和运行本机 Windows 软件。拥有一个软件包安装和更新的Pacman包管理系统，它拥有一个强大的功能，不限于依赖"
ShowToc: true
TocOpen: false
hidemeta: false
comments: true
ShowReadingTime: true
ShowShareButtons: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

## 一、Msys的编译

![2025-10-05_144929](/images/posts/windows-software-build-qc/01.png)

  
MSYS2 是基于Cygwin软件开发而来的工具和库的集合，为您提供了一个易于使用的环境，用于构建、安装和运行本机 Windows 软件。拥有一个软件包安装和更新的Pacman包管理系统，它拥有一个强大的功能，不限于依赖关系解析、简单的系统升级，以及直接的可重复的包构建，其软件存储库包含3500多个预构建软件包。

### （一）、[参考官网安装](https://www.msys2.org/)

1. 安装包下载  
   <https://github.com/msys2/msys2-installer/releases/download/2025-08-30/msys2-x86_64-20250830.exe>  
   <https://mirrors.tuna.tsinghua.edu.cn/msys2/distrib/x86_64/msys2-x86_64-20250830.exe>
2. 软件源更换  
   使用现代的C运行时库，比较完备的环境Mingw-UCRT，并参照清华源使用帮助更换清华源为首选：

   ```
   sed -i "s#https\?://mirror.msys2.org/#https://mirrors.tuna.tsinghua.edu.cn/msys2/#g" /etc/pacman.d/mirrorlist*
   ```
3. 软件源更新

   ```
   pacman -Syu
   pacman -Su
   # 安装完整开发工具链
   pacman -S --needed base-devel mingw-w64-ucrt-x86_64-toolchain
   pacman -S git
   ```

## 二、质控

![2025-10-05_151124](/images/posts/windows-software-build-qc/02.png)

  

![2025-10-05_163416](/images/posts/windows-software-build-qc/03.png)

  
为 FastQ 数据提供超快的一体化预处理和质量控制的工具。fastp 支持对文件夹中的多个 FASTQ 文件进行批处理。  
FastQ 数据即是生物信息分析的起点​

1. 测序平台技术不同把测序的数据分为短读长、长读长数据类型
   - 短读长：即 Illumina NovaSeq、MGI 🔸➖➡**Fastp**
   - 长读长：即 Nanopore、PacBio、Cyclone 🔸➖➡**Fastplong**
2. 测序的方法又分单端与双端测序
   - 双端：即​​全基因组测序​、宏基因组测序​、转录组测序​、外显子组测序​等需求比对更准、组装更好、能发现更大范围的变异的研究。​
   - 单端：即基因表达定量​、ChIP-seq​、小RNA测序​、某些大型筛查项目​等适用于成本低、通量高，目标明确、不需要配对信息的筛查式研究

### （一）、Fastp安装

```bash
pacman -S mingw-w64-ucrt-x86_64-isal
pacman -S mingw-w64-ucrt-x86_64-libdeflate
git clone https://github.com/OpenGene/fastp.git
# 编译
cd fastp
make -j
# 安装
make install
pacman -S mingw-w64-ucrt-x86_64-highway
```

### （二）、Fastp -h详解（参考腾讯元宝对Fastp -h的详解，🌟为常用）

```
fastp -i R1.fq.gz -o clean_R1.fq.gz -I R2.fq.gz -O clean_R2.fq.gz \ # 输入输出
      -q 20 \                                                       # 碱基质量大于Q20
      -u 20 \                                                       # 不合格碱基不超过20%
      -l 50 \                                                       # 最小50bp读长，
      -5 -3 \                                                       # 切除前端、尾端低质量区
      -g -w 8 \                                                     # 切除PolyG尾，8线程加速处理
      -j report.json -h report.html                                 # 输出报告
```

#### 1. 输入/输出

-i, --in1 # 🌟输入单端或双端数据的R1文件  
-o, --out1 # 🌟输出质控后R1输出路径  
-I, --in2 # 🌟输入双端测序的R2文件  
-O, --out2 # 🌟输出双端测序的R2输出路径  
-z, --compression # 🌟GZIP压缩级别，节省存储空间（默认4）  
--merged\_out # 🌟合并后的输出文件，使用 -m参数时必选  
--interleaved\_in # 输入为交错式FASTQ，用于处理已合并的PE数据  
--stdin # 从标准输入读取，在管道操作时使用  
--stdout # 输出到标准输出，配合管道传递给下游工具

#### 2. 质量控制⭐⭐⭐

1. 质量过滤​

   ```
     -q, --qualified_quality_phred      # 🌟合格碱基的质量阈值（默认Q15）
     -u, --unqualified_percent_limit    # 🌟允许不合格碱基的最大比例（默认40%），以控制整体读长质量
     -n, --n_base_limit                 # 🌟允许N碱基的最大数量（默认5），过滤含过多未知碱基的读长
     -e, --average_qual                 # 平均质量阈值，严格过滤低质量reads
   ```
2. 长度过滤​

   ```
   -l, --length_required     # 🌟最小读长要求（默认15bp），过滤过短读长（如接头污染）
   --length_limit            # 最大读长限制，移除异常长读长（如嵌合体）
   ```
3. 特殊过滤​

   ```
   -g, --trim_poly_g           # 🌟切除PolyG尾，适用于​​双色化学法测序的NextSeq/NovaSeq数据
   -x, --trim_poly_x           # 切除PolyX尾，处理其他平台可能的均聚物错误
   -Y, --complexity_threshold  # 低复杂度过滤阈值（默认30%），宏基因组分析中过滤简单重复序列
   ```

#### 3. 接头处理⭐⭐⭐

```
-a, --adapter_sequence           # 🌟指定Read1接头序列，在已知接头时手动指定
--adapter_fasta                  # 🌟提供接头FASTA文件，多接头混合时批量过滤
--adapter_sequence_r2            # 指定Read2接头序列，适用于PE数据中R2接头与R1不同时使用
-A, --disable_adapter_trimming   # 禁用接头修剪，仅当确认数据无接头时使用
```

#### 4. 读长裁剪

```
-f, --trim_front1         # 🌟从R1前端切除碱基，切除低质量起始碱基
-5, --cut_front           # 🌟滑动窗口切除前端低质量区，​​自动切除前端连续低质量碱基​​
-3, --cut_tail            # 🌟滑动窗口切除尾部低质量区，​​自动切除末端连续低质量碱基​​
-W, --cut_window_size     # 🌟滑动窗口大小（默认4bp），调整切除灵敏度，值越小越敏感
-M, --cut_mean_quality    # 🌟窗口质量阈值，调整严格度（默认Q20）
-t, --trim_tail1          # 从R1尾部切除碱基，修复末端质量下降问题
```

#### 5. 双端测序专属功能​

```
-m, --merge               # 🌟合并重叠的PE读长，​​适用于扩增子测序​​，提高序列准确性
-c, --correction          # 🌟校正重叠区错配碱基，适用于合并PE读长时纠正测序错误
--overlap_len_require     # 最小重叠长度（默认30bp），以控制合并/校正的严格性
--unpaired1/--unpaired2   # 保存未配对读长，当部分读长被过滤时保留单端数据
```

#### 6. 高级分析

```
-p, --overrepresentation_analysis      # 过表达序列分析，检测高丰度序列
-P, --overrepresentation_sampling      # 过表达采样率，调整分析效率（默认20）
-Q, --disable_quality_filtering        # 禁用质量过滤，仅做接头修剪时
-L, --disable_length_filtering         # 禁用长度过滤，保留所有长度读长
```

#### 7. 报告与监控​

```
-j, --json         # 🌟JSON格式报告（默认fastp.json），​​自动化流程必用​​，机器可读
-h, --html         # 🌟HTML格式报告（默认fastp.html），​​人工查看质控结果​​，含图表
-w, --thread       # 🌟线程数（默认3），​​加速处理​​（设为CPU核心数-1）
-V, --verbosev     # 输出详细日志，调试或监控大文件处理进度
```

#### 8. 特殊场景功能

```
-U, --umi        # 🌟UMI处理，适用于​​单细胞/低频突变检测必用​​，去重PCR重复
--umi_loc        # UMI位置（index/read），指定UMI在测序读长中的位置
-D, --dedup      # 去除PCR重复，全基因组测序减少数据量
-6, --phred64    # 转换Phred64为Phred33，处理早期Illumina数据（<1.8版本）
```

### （三）、Fastplong安装

```bash
pacman -S mingw-w64-ucrt-x86_64-highway
git clone https://github.com/OpenGene/fastplong.git
# 编译
cd fastplong
make -j
# 安装
make install
```

（四）、Fastplong -h详解（参考腾讯元宝对Fastplong -h的详解，🌟为常用）

```
fastplong -i raw.fastq.gz -o clean.fastq.gz \ # 输入输出
          -a adapters.fa \                    # 接头FASTA文件
          -q 10 -u 50 \                       # 宽松质量过滤（因长读长原始错误率高）
          # -q 15 -u 20 \                     # 严格：质量过滤
          -n 10 \                             # 过滤>10% N碱基的读长
          # -n 5 \                            # 严格：允许更少N碱基
          # -m 12 \                           # 严格：要求平均质量≥Q12
          -l 1000 \                           # 最小长度1kb
          # -l 5000 \                         # 严格：只保留>5kb读长
          -5 -3 \                             # 切除首尾低质量区
          -w 16 \                             # 16线程加速
          # -x --poly_x_min_len 15 \          # 严格：切除PolyX尾
          -j report.json -h report.html       # 输出报告
```

#### 1. 输入/输出

```
-i, --in                   # 🌟输入文件​​，长读长数据文件
-o, --out                  # 🌟输出文件，质控后输出路径
-z, --compression          # 🌟GZIP压缩级别，节省存储空间（默认4）
--failed_out               # 保存未通过过滤的readsm，分析过滤原因，以研究低质量序列特征
--stdin                    # 从标准输入读取，用于管道操作
--stdout                   # 输出到标准输出，管道传递给下游工具
--reads_to_process         # 处理指定数量的reads，测试或小规模分析
--dont_overwrite           # 禁止覆盖现有文件，保护已有数据
```

#### 2. 接头处理

```
-s, --start_adapter             # 🌟5'端接头序列，指定已知的5'端接头
-e, --end_adapter               # 🌟3'端接头序列，指定已知的3'端接头
-a, --adapter_fasta             # 🌟接头FASTA文件，包含多个接头序列
-d, --distance_threshold        # 接头识别距离阈值，调整灵敏度（默认0.25），值越大越严格
--trimming_extension            # 额外切除长度，确保彻底切除接头（默认多切10bp）
-A, --disable_adapter_trimming  # 禁用接头修剪，确认数据无接头时
```

#### 3. 读长裁剪

```
-f, --trim_front            # 🌟从5'端切除碱基，切除固定长度的起始低质量碱基
-t, --trim_tail             # 🌟从3'端切除碱基，切除固定长度的末端低质量碱基
-5, --cut_front             # 🌟5'端滑动窗口修剪，​​自动切除前端连续低质量区​​
-3, --cut_tail              # 🌟3'端滑动窗口修剪，​​自动切除末端连续低质量区​​
-W, --cut_window_size       # 滑动窗口大小，调整灵敏度（默认4bp）
-M, --cut_mean_quality      # 窗口质量阈值，调整严格度（默认Q20）
```

#### 4. 质量控制​

```
-q, --qualified_quality_phred           # 🌟合格碱基质量阈值，单碱基质量要求（默认Q15）
-u, --unqualified_percent_limit         # 🌟允许不合格碱基比例，控制整体质量（默认40%）
-n, --n_percent_limit                   # 🌟允许N碱基百分比（默认10%，即>10%N的读长被丢弃）
-l, --length_required                   # 🌟最小长度要求，过滤过短读长（默认20bp）
--n_base_limit                          # 允许N碱基数量，过滤含过多N的读长（默认无限制）
-Q, --disable_quality_filtering         # 禁用质量过滤，仅做接头修剪时
-y, --low_complexity_filter             # 启用低复杂度过滤，过滤简单重复序列
-Y, --complexity_threshold              # 复杂度阈值，调整严格度（默认30%）
-L, --disable_length_filtering          # 禁用长度过滤，保留所有长度读长
--length_limit                          # 最大长度限制，过滤异常长读长（如嵌合体）
-m, --mean_qual                         # 最小平均质量，丢弃平均质量过低的读长（默认无限制）
```

#### 5. 报告与监控​

```
-j, --json                   # 🌟JSON格式报告，​​自动化流程必用​​
-h, --html                   # 🌟HTML格式报告，​​人工查看质控结果​​
-w, --thread                 # 🌟线程数，​​加速处理​​（默认3）
-R, --report_title           # 报告标题，自定义报告标题
-V, --verbose                # 详细日志，监控处理进度
```
