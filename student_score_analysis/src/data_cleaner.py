import pandas as pd
import numpy as np
import os
class DataCleaner:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.score_cols = ['chinese', 'math', 'english']  # 满分150的成绩列
        self.full_score_cols = ['chinese', 'math', 'english', 'physics']  # 所有成绩列


    def clean_missing_values(self):
        # ========== 处理缺失值（NaN） ============ 处理成绩异常值（越界值） ==========
        # 问题：存在不合理成绩，如 chinese=-16（负分）
        # 规则：语文/数学/英语 满分150，有效范围 0~150；物理 满分100，有效范围 0~100
        # 方案：将超出有效范围的成绩视为异常，替换为均值填充
        # 问题：成绩列可能存在 NaN（原始缺失）
        # 方案：用各科目的平均分（排除NaN后计算）填充缺失值

        # 先确保成绩列为数值类型，非数值转为NaN
        for col in self.full_score_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        # 语数英：超出 0~150 范围的设为 NaN
        for col in self.score_cols:
            self.df.loc[(self.df[col] < 0) | (self.df[col] > 150), col] = np.nan
        # 物理：超出 0~100 范围的设为 NaN
        self.df.loc[(self.df['physics'] < 0) | (self.df['physics'] > 100), 'physics'] = np.nan

        # 用各科中位数填充所有 NaN（inplace 对切片不生效，必须逐列赋值）
        for col in self.full_score_cols:
            self.df[col] = self.df[col].fillna(self.df[col].median())
        return self

    def clean_duplicates(self):
        # 重复值处理组
        self.df.drop_duplicates(inplace=True)
        self.df.drop_duplicates(subset=['student_id'], keep='first', inplace=True)  # 按学号去重，保留第一个
        self.df.dropna(subset=['student_id'], inplace=True) # 删除缺失学号的行
        return self

    def clean_strings(self):
        # 文本清洗组
        # ========== 修复 student_id 格式不一致 ========== 统一 gender 列的取值 ========== 统一 name 列的格式 ==========
        # 问题：部分学号带前导零，如 "001006"，而大部分学号为 "1006" 格式
        # 方案：将 student_id 统一转为整数类型，去除前导零
        self.df['student_id'] = pd.to_numeric(self.df['student_id'], errors='coerce')
        self.df['student_id'] = self.df['student_id'].astype(int)
        # 问题：大部分值为 "Male"/"Female"，但存在缩写 "F"
        # 方案：将 "F" 替换为 "Female"，"M" 替换为 "Male"，保证取值只有两种
        gender_map = {'m': '男', 'male': '男','F': '女', 'female': '女'}
        self.df['gender'] = self.df['gender'].str.casefold().map(gender_map).fillna('Unknown')
        unknown_mask = self.df['gender'] == 'Unknown'
        random_genders = np.random.choice(['男', '女'], size=len(unknown_mask))
        self.df.loc[unknown_mask, 'gender'] = random_genders[unknown_mask]
        # 问题：部分姓名为拼音格式如 "Xuesheng9"，而大部分为中文 "学生1"
        # 方案：识别拼音格式的姓名，将其替换为对应的中文格式 "学生X"
        # 去除空格
        self.df['name'] = self.df['name'].str.strip()
        self.df['name'] = self.df['name'].str.replace(r'(?i)Xuesheng(\d+)', r'学生\1', regex=True)
        mask = self.df['name'].str.match(r'^学生\d+$', na=False)
        self.df.loc[~mask, 'name'] = "学生" + self.df.loc[~mask, 'name'].str.findall(r'\d').str.join('').str[:3]
        return self.df

    def add_new_col(self):
        # ========== 新增计算列 ==========
        # total_score = chinese + math + english + physics（总分）
        # avg_score = total_score / 4（四科平均分）
        self.df['total_score'] = self.df[self.full_score_cols].sum(axis=1).round(1)
        self.df['average_score'] = self.df[self.full_score_cols].mean(axis=1).round(1)
        return self

    def data_export(self, filename='clean_scores.csv'):
        """导出清洗后的数据"""
        # 1. 定义项目根目录（src 的父目录）
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 2. 组合完整输出路径：项目根目录/data/filename
        full_output_dir = os.path.join(project_root, 'data')
        # 3. 如果输出目录不存在，则创建它
        os.makedirs(full_output_dir, exist_ok=True)
        # 4. 组合完整的文件路径
        full_file_path = os.path.join(full_output_dir, filename)
        self.df.to_csv(full_file_path, index=False)
        print(f"数据已导出至: {full_file_path}")
        return self


    def run_pipeline(self):
        self.clean_missing_values()
        self.clean_duplicates()
        self.clean_strings()
        self.add_new_col()
        self.data_export()
        return self.df