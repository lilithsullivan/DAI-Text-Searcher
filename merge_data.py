import pandas as pd
import os

# 定义数据文件夹路径
data_dir = "data_source"

print("正在从 data_source 目录读取文件...")

# 组合路径，例如 "data_source/cn.csv"
# dtype={0: str} 确保 ID 列的 0 不会被自动去掉
try:
    df_cn = pd.read_csv(os.path.join(data_dir, 'cn.csv'), header=None, names=['ID', 'Simplified Chinese'], dtype={0: str})
    df_tc = pd.read_csv(os.path.join(data_dir, 'tc.csv'), header=None, names=['ID', 'Traditional Chinese'], dtype={0: str})
    df_en = pd.read_csv(os.path.join(data_dir, 'en.csv'), header=None, names=['ID', 'English'], dtype={0: str})

    print("正在横向对齐中、英、繁数据...")
    # 合并数据
    merged = pd.merge(df_en, df_cn, on='ID', how='outer')
    merged = pd.merge(merged, df_tc, on='ID', how='outer')

    # 将合并后的成品放在根目录，方便网页程序读取
    merged.to_csv('dai_corpus.csv', index=False, encoding='utf-8-sig')
    print("✅ 成功！已生成 dai_corpus.csv")
    print("现在你可以运行: python -m streamlit run app.py")

except FileNotFoundError as e:
    print(f"❌ 错误：找不到文件！请检查 data_source 文件夹内是否有 cn.csv, tc.csv 和 en.csv")
    print(f"具体错误信息: {e}")