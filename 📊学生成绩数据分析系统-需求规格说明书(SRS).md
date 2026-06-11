# 📊 学生成绩数据分析系统 (SSAS) - 新手学习型需求文档

| 文档版本     | V 1.0                                  | 适用人群 | Python 数据分析初学者 |
| ------------ | -------------------------------------- | -------- | --------------------- |
| **项目代号** | SSAS                                   | 预计周期 | 2 - 3 周              |
| **核心库**   | **Pandas, NumPy, Matplotlib, Seaborn** | 难度系数 | ⭐⭐☆☆☆                 |

------

## 1. 项目愿景 (Project Vision)

### 1.1 为什么做这个项目？

作为一名数据分析新手，你需要一个**真实、接地气**的数据集来练手。学生成绩数据结构简单（数值型为主），业务逻辑清晰，是练习 **Pandas 数据处理** 和 **Matplotlib/Seaborn 可视化** 的最佳切入点。

### 1.2 学习目标（技术映射）

本项目将手把手带你掌握以下技能点：

| 功能模块       | 核心知识点 (What you will learn)                      | 难度 |
| -------------- | ----------------------------------------------------- | ---- |
| **数据加载**   | `Pandas`读取 CSV/Excel (`read_csv`, `read_excel`)     | 入门 |
| **数据清洗**   | `NumPy`缺失值处理 (`np.nan`)、数据类型转换 (`astype`) | 入门 |
| **核心统计**   | `Pandas`聚合计算 (`groupby`, `agg`, `describe`)       | 进阶 |
| **可视化**     | `Matplotlib`绘制基础图表 (直方图、柱状图)             | 进阶 |
| **高级可视化** | `Seaborn`绘制热力图、箱线图、相关性分析               | 高阶 |

------

## 2. 数据字典 (Database Schema)

我们将使用一个名为 `scores.csv`的文件。请在本地创建它，或者让程序自动生成模拟数据。

| 字段名       | 数据类型 | 说明                   | 涉及库 |
| ------------ | -------- | ---------------------- | ------ |
| `student_id` | int      | 学号                   | Pandas |
| `name`       | str      | 学生姓名               | Pandas |
| `gender`     | str      | 性别 ('Male'/'Female') | Pandas |
| `chinese`    | float    | 语文成绩 (0-150)       | NumPy  |
| `math`       | float    | 数学成绩 (0-150)       | NumPy  |
| `english`    | float    | 英语成绩 (0-150)       | NumPy  |
| `physics`    | float    | 物理成绩 (0-100)       | NumPy  |

------

## 3. 功能需求详解 (Functional Requirements)

### 3.1 阶段一：数据加载与清洗 (Pandas 基础)

> **🎯 学习目标**：学会用 Pandas 读取数据，并处理脏数据。

- 

  **FR-01 读取数据**

  - 

    **描述**：编写函数 `load_data(file_path)`，读取 CSV 文件。

  -  

    **代码指引**：

    ```
    import pandas as pd
    
    def load_data(file_path):
        df = pd.read_csv(file_path)
        print(df.head())  # 查看前5行
        return df
    ```

- 

  **FR-02 处理缺失值**

  - 

    **描述**：检测到缺失成绩（NaN），用该科目的**平均分**填充。

  - 

    **涉及库**：`NumPy`(用于识别 NaN)。

  - 

    **代码指引**：

    ```
    # 使用 numpy 来检查空值并填充平均值
    import numpy as np
    
    df['math'].fillna(df['math'].mean(), inplace=True)
    ```

- 

  **FR-03 增加计算列**

  - 

    **描述**：新增一列 `total_score`（总分）和 `avg_score`（平均分）。

  - 

    **代码指引**：

    ```
    # axis=1 表示按行计算
    df['total_score'] = df[['chinese', 'math', 'english']].sum(axis=1)
    ```

### 3.2 阶段二：基础统计分析 (Pandas 进阶)

> **🎯 学习目标**：使用聚合函数快速洞察数据。

- 

  **FR-04 计算班级指标**

  - 

    **描述**：计算全班的各科平均分、最高分、最低分、标准差。

  - 

    **代码指引**：

    ```
    # describe() 会返回计数、均值、标准差、最小值、四分位数、最大值
    stats = df[['math', 'chinese']].describe()
    print(stats)
    ```

- 

  **FR-05 按性别分组统计**

  - 

    **描述**：对比男生和女生的平均成绩差异。

  - 

    **代码指引**：

    ```
    # 按 gender 列分组，然后计算 math 的平均值
    gender_stats = df.groupby('gender')['math'].mean()
    print(gender_stats)
    ```

### 3.3 阶段三：数据可视化 (Matplotlib & Seaborn)

> **🎯 学习目标**：把枯燥的数字变成直观的图表。

- 

  **FR-06 成绩分布直方图 (Matplotlib)**

  - 

    **描述**：查看数学成绩的分布是否呈正态分布（钟形曲线）。

  - 

    **代码指引**：

    ```
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 6))
    plt.hist(df['math'], bins=10, edgecolor='black')
    plt.title('Math Score Distribution')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.show()
    ```

- 

  **FR-07 各科均分柱状图 (Matplotlib)**

  - 

    **描述**：对比语数英三科谁最难（平均分最低）。

  - 

    **代码指引**：

    ```
    subjects = ['Chinese', 'Math', 'English']
    averages = [df['chinese'].mean(), df['math'].mean(), df['english'].mean()]
    
    plt.bar(subjects, averages, color=['blue', 'green', 'red'])
    plt.title('Average Scores by Subject')
    plt.show()
    ```

- 

  **FR-08 成绩相关性热力图 (Seaborn)**

  - 

    **描述**：分析数学好的人物理是不是也好？（相关系数矩阵）。

  - 

    **代码指引**：

    ```
    import seaborn as sns
    
    plt.figure(figsize=(8, 6))
    corr_matrix = df[['chinese', 'math', 'english', 'physics']].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=.5)
    plt.show()
    ```

- 

  **FR-09 箱线图分析 (Seaborn)**

  - 

    **描述**：找出异常值（特别高分或低分的学生）。

  - 

    **代码指引**：

    ```
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='gender', y='math', data=df)
    plt.show()
    ```

------

## 4. 非功能性需求 (Non-Functional)

| 类型         | 要求                                              | 学习意义   |
| ------------ | ------------------------------------------------- | ---------- |
| **代码规范** | 变量名清晰（如 `avg_math_score`），函数需有注释。 | 养成好习惯 |
| **环境隔离** | 必须使用 Conda 或 Virtualenv 创建独立环境。       | 避免库冲突 |
| **版本控制** | 每完成一个功能提交一次 Git Commit。               | 熟悉工作流 |

------

## 5. 新手开发路线图 (Roadmap)

请严格按照以下步骤执行，不要跳步！

### Step 1: 环境准备 (Day 1)

```
# 1. 创建干净的 Python 3.10 环境
conda create -n score_analysis python=3.10 -y

# 2. 激活环境
conda activate score_analysis

# 3. 安装所需的库 (指定版本，避免兼容性问题)
pip install pandas numpy matplotlib seaborn jupyter
```

### Step 2: 数据生成 (Day 2)

- 

  不用找数据源，直接用代码生成 100 条模拟数据（这是数据分析师的基本功）。

- 

  创建 `generate_data.py`。

### Step 3: 编码实现 (Day 3-10)

1. 

   **Day 3-4**：完成 `FR-01`到 `FR-03`。在 Jupyter Notebook 里玩转 DataFrame。

2. 

   **Day 5-6**：完成 `FR-04`到 `FR-05`。练习 `groupby`的各种花式用法。

3. 

   **Day 7-9**：完成 `FR-06`到 `FR-09`。疯狂调试图表的美观度（颜色、标签）。

4. 

   **Day 10**：整理代码，上传至 Gitee。

------

## 6. 项目结构 (Project Structure)

请按此结构组织你的文件夹，这非常专业：

```
student-score-analysis/
│
├── data/                      # 数据文件夹
│   └── scores.csv             # 原始成绩数据
│
├── src/                       # 源代码
│   ├── __init__.py
│   ├── data_loader.py         # FR-01: 负责读取数据
│   ├── data_cleaner.py        # FR-02/03: 负责清洗和计算
│   └── visualizer.py         # FR-06~09: 负责画图
│
├── notebooks/                 # Jupyter 实验笔记
│   └── 01_data_exploration.ipynb
│
├── main.py                    # 主程序入口
├── requirements.txt           # 依赖库列表 (pandas==2.0.0 ...)
└── README.md                 # 项目介绍
```

------

## 7. 避坑指南 (Tips for Beginners)

1. 

   **关于 NumPy**: 你不需要深入学习 NumPy 的矩阵运算，本项目只用它来处理 `NaN`(空值) 和基本统计。

2. 

   **关于中文乱码**: Matplotlib 默认不支持中文。在绘图代码前加上：

   ```
   plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
   plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
   ```

3. 

   **关于 Seaborn**: 如果画图时报错 `ModuleNotFoundError`，记得确认你是否激活了正确的 Conda 环境。

------

## 8. 验收标准 (Checklist)

当你完成项目时，你应该能回答以下问题：

- 

  [ ] 我能用 Pandas 读取 CSV 并显示前 5 行吗？

- 

  [ ] 我知道如何用 `groupby`计算男生的数学平均分吗？

- 

  [ ] 我能画出一张包含标题、坐标轴标签且中文不乱码的柱状图吗？

- 

  [ ] 我能在 Gitee 上看到我的代码提交记录吗？

**加油！开始你的第一行 `import pandas as pd`吧！** 🚀