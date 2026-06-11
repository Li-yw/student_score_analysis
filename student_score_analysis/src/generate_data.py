import numpy as np  # 导入 NumPy 库并别名为 np，用于数值计算和随机数生成
import pandas as pd  # 导入 Pandas 库并别名为 pd，用于数据处理和 DataFrame 操作
import os  # 导入 os 模块，用于处理文件路径

np.random.seed(42)  # 设置随机种子，保证每次运行结果一致（可复现）

n = 200  # 定义基础记录数量

# ==================== 1. 生成基础干净数据 ====================
# range(start, stop) 生成 1~200 的整数序列，list() 转为列表
student_ids = list(range(1001, n + 1001))
names = [f"学生{i}" for i in range(1, n + 1)]  # 列表推导式：遍历 1~200，用 f-string 格式化生成姓名
genders = np.random.choice(["Male", "Female"], size=n)  # 从列表中随机选择，size 指定生成 n 个值

chinese = np.random.uniform(60, 151, size=n).round(1)  # 生成 [low, high) 范围内的随机整数数组，左闭右开
math = np.random.uniform(60, 151, size=n).round(1)
english = np.random.uniform(60, 151, size=n).round(1)
physics = np.random.uniform(40, 101, size=n).round(1)

df = pd.DataFrame({  # 创建 DataFrame，传入字典：键为列名，值为列数据
    "student_id": student_ids,
    "name": names,
    "gender": genders,
    "chinese": chinese,
    "math": math,
    "english": english,
    "physics": physics,
})

score_cols = ["chinese", "math", "english", "physics"]  # 定义成绩列名列表，后续复用
all_cols = df.columns.tolist()  # 定义全部列名列表

# 将学号列和成绩列转为 object 类型，允许后续混入字符串（避免 FutureWarning）
df["student_id"] = df["student_id"].astype(object)
df[score_cols] = df[score_cols].astype(object)

# ==================== 2. 缺失值：随机 5% 记录，随机 1-2 个字段设为 NaN ====================
missing_indices = np.random.choice(n, size=int(n * 0.05), replace=False)  # replace=False 表示不放回抽样，确保索引不重复
for idx in missing_indices:  # for 循环遍历每个被选中的索引
    num_fields = np.random.choice([1, 2])  # 随机选择要置空 1 个还是 2 个字段
    fields = np.random.choice(all_cols, size=num_fields, replace=False)  # 从所有列中随机选取指定数量的列名
    for f in fields:  # 遍历选中的字段
        df.at[idx, f] = np.nan  # df.at[row, col] 按行列标签精确访问单个单元格，赋值为 NaN（缺失值）

# ==================== 3. 异常值：随机 3% 记录，某科成绩设为异常值 ====================
outlier_indices = np.random.choice(n, size=int(n * 0.03), replace=False)
for idx in outlier_indices:
    col = np.random.choice(score_cols)  # 随机选一门成绩科目
    max_score = 100 if col == "physics" else 150  # 三元表达式：条件为 True 取前者，否则取后者
    outlier_val = np.random.choice([  # 从两个候选异常值中随机选一个
        np.random.randint(-50, 0),  # 负数异常值
        np.random.randint(max_score + 50, 300),  # 远超满分的异常值
    ])
    df.at[idx, col] = outlier_val

# ==================== 4. 格式不一致 ====================
# 4a. 姓名字段混入特殊字符
special_char_indices = np.random.choice(n, size=8, replace=False)
for idx in special_char_indices:
    original = str(df.at[idx, "name"])  # str() 将值转为字符串，防止 NaN 等非字符串类型报错
    variant = np.random.choice([  # 随机选一种特殊字符拼接方式
        f"#{original}",  # f-string 中 # 拼在原姓名前面
        f"{original}_",  # 下划线拼在后面
        f"{original}!",  # 感叹号拼在后面
    ])
    df.at[idx, "name"] = variant

# 4b. 性别字段混入非标准值
gender_variant_indices = np.random.choice(n, size=8, replace=False)
gender_variants = ["male", "female", "M", "F", "未知", "male", "F", "female"]  # 非标准性别值列表
for idx, variant in zip(gender_variant_indices, gender_variants):  # zip() 将两个列表按位置配对，同时遍历
    df.at[idx, "gender"] = variant

# ==================== 5. 重复记录：复制 2-3 条完整记录 ====================
duplicate_indices = np.random.choice(n, size=3, replace=False)
duplicate_rows = df.iloc[duplicate_indices].copy()  # df.iloc[] 按位置索引取行，.copy() 深拷贝避免修改原数据
df = pd.concat([df, duplicate_rows], ignore_index=True)  # pd.concat() 沿轴拼接多个 DataFrame；ignore_index=True 重置索引

# ==================== 6. 数据类型错误 ====================
# 6a. 学号字段中某些值改为字符串
id_str_indices = np.random.choice(n, size=5, replace=False)
for idx in id_str_indices:
    original_id = df.at[idx, "student_id"]
    if pd.notna(original_id):  # pd.notna() 判断值是否非空（不是 NaN），是则返回 True
        df.at[idx, "student_id"] = f"00{int(original_id)}"  # int() 转整数后再用 f-string 拼接前缀 "00"，造成数字与字符串混用

# 6b. 成绩字段中混入字符串
str_score_indices = np.random.choice(n, size=6, replace=False)
str_score_vals = ["缺考", "null", "缺考", "null", "缺考", "null"]
for idx, val in zip(str_score_indices, str_score_vals):
    col = np.random.choice(score_cols)
    df.at[idx, col] = val  # 将数值型成绩替换为字符串，制造类型混用

# ==================== 7. 不一致的命名规范：部分"学生"替换为"Xuesheng" ====================
pinyin_indices = np.random.choice(n, size=10, replace=False)
for idx in pinyin_indices:
    original = str(df.at[idx, "name"])
    if "学生" in original:  # in 运算符检查子串是否存在于字符串中
        df.at[idx, "name"] = original.replace("学生", "Xuesheng")  # str.replace(old, new) 将所有匹配的子串替换

# ==================== 保存 ====================
script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取脚本所在目录的绝对路径
project_root = os.path.dirname(script_dir)  # 上一级即项目根目录
df.to_csv(os.path.join(project_root, "data", "scores.csv"), index=False, encoding="utf-8")  # to_csv() 导出为 CSV；index=False 不写行索引；encoding="utf-8" 指定编码
print(f"数据集已生成，共 {len(df)} 条记录，保存为 scores.csv")  # len() 获取 DataFrame 行数
print(f"包含脏数据的问题记录占比约 10%")
