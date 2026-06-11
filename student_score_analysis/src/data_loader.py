import pandas as pd
import os

def load_and_inspect(file_path):
    """加载数据并初步查看"""
    df = pd.read_csv(file_path, encoding='utf-8')
    print("1. 数据形状 (行数, 列数):", df.shape)
    print("\n2. 前5行数据:")
    print(df.head())
    print("\n3. 数据基本信息:")
    print(df.info())
    print("\n4. 检查缺失值:")
    print(df.isna().sum())
    return df

def Ranking(df):
    # 排名
    df['total'] = df[['chinese', 'math', 'english', 'physics']].sum(axis=1)
    df['rank'] = df['total'].rank(method='min', ascending=False).astype(int)
    # 按排名排序
    df.sort_values(by='rank', ascending=True, inplace=True)
    print(df.head())
    return df

def Pass_rate(df,subject='math'):
    # 及格率
    # 计算数学及格率
    pass_subject = ((df[subject] >= 60) if subject == 'physics' else (df[subject] >= 90)).sum()
    rate_subject = pass_subject/ len(df) * 100
    print(f"\n{subject}及格率：{rate_subject:.1f}%")
    return df

def Overall_description(df):

    # 1. 整体描述（各科的平均分、标准差、最高分等）
    print("各科成绩描述性统计:")
    print(df[['chinese', 'math', 'english', 'physics']].describe())

    # 2. 按性别分组统计平均分
    print("\n按性别分组平均分:")
    group_stats = df.groupby('gender')[['chinese', 'math', 'english', 'physics']].mean()
    print(group_stats)
    return

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_df = load_and_inspect(os.path.join(base_dir, 'data', 'clean_scores.csv'))
    Ranking(raw_df)
    Pass_rate(raw_df,'physics')
    Overall_description(raw_df)