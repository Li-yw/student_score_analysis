from src import data_loader, data_cleaner, visualizer

def main():
    # 1. 加载
    cleaner = data_cleaner.DataCleaner('data/scores.csv')
    # 2. 清洗
    clean_df = cleaner.run_pipeline()

    # 3. 分析并保存结果
    report = clean_df.describe().to_string()
    with open('./outputs/analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write("学生成绩分析报告\n=================\n")
        f.write(report)

    # 4. 可视化
    visualizer.plot_subject_avg(clean_df)
    visualizer.plot_histogram(clean_df,'physics')
    visualizer.plot_correlation_heatmap(clean_df)

if __name__ == '__main__':
    main()