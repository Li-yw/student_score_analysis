import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

SUBJECTS = {'chinese': '语文',
            'math': '数学',
            'english': '英语',
            'physics': '物理'}

def plot_subject_avg(clean_df):
    averages = [clean_df[col].mean() for col in SUBJECTS]
    subject_labels = list(SUBJECTS.values())
    plt.figure(figsize=(10,6))
    bars = plt.bar(subject_labels, averages, color=['skyblue', 'lightgreen', 'orange', 'pink'])
    plt.title('各科平均分对比')
    plt.ylabel('平均分')
    # 在柱子上方添加数值
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}', ha='center', va='bottom')
    #plt.savefig('各科平均分.png')  # 保存图片
    plt.show()

def plot_histogram(clean_df,subject='math'):
    plt.figure(figsize=(10,6))
    plt.hist(clean_df['math'], bins=15, edgecolor='black', alpha=0.7)
    plt.title(f"{SUBJECTS[subject]}成绩分布直方图")
    plt.xlabel('分数')
    plt.ylabel('人数')
    plt.grid(True, linestyle='--', alpha=0.5)
    #plt.savefig('数学成绩分布.png')
    plt.show()

def plot_correlation_heatmap(clean_df):
    plt.figure(figsize=(8,6))
    # 计算相关系数矩阵
    corr = clean_df[SUBJECTS.keys()].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, square=True)
    plt.title('各科成绩相关性热力图')
    #plt.savefig('成绩相关性热力图.png')
    plt.show()

# 替换你原来的 bar_plot 函数
def plot_math_distribution(clean_df):
    plt.style = 'whitegrid'
    plt.figure(figsize=(10, 6))
    sns.histplot(data=clean_df, x='math', bins=20, kde=True)
    plt.title('数学成绩分布')
    plt.xlabel('分数')
    plt.ylabel('学生人数')
    plt.show()


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'data', 'clean_scores.csv')
    subjects = SUBJECTS
    clean_df = pd.read_csv(csv_path)
    plot_subject_avg(clean_df)
    plot_histogram(clean_df,'physics')
    plot_correlation_heatmap(clean_df)
    # 然后调用它
    plot_math_distribution(clean_df)