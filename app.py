import streamlit as st
import pandas as pd

# 设置网页标题和布局
st.set_page_config(page_title="龙腾世纪：审判 语料对比", layout="wide")

st.title("🐉 Dragon Age: Inquisition 本地化对比工具")
st.markdown("---")

# 加载数据
@st.cache_data # 缓存数据，这样搜索起来飞快
def load_data():
    return pd.read_csv('dai_corpus.csv')

df = load_data()

# 侧边栏：搜索设置
st.sidebar.header("搜索设置")
search_query = st.sidebar.text_input("输入关键词（中/英/ID）", "")
show_all = st.sidebar.checkbox("无搜索时显示前100条", value=True)

# 搜索逻辑
if search_query:
    # 在所有列中查找包含关键词的行（忽略大小写）
    result = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)]
else:
    result = df.head(100) if show_all else pd.DataFrame()

# 结果展示
if not result.empty:
    st.write(f"🔍 找到 {len(result)} 条记录")
    
    # 使用 Dataframe 展示，支持点击列头排序
    st.dataframe(
        result, 
        use_container_width=True,
        column_config={
            "ID": st.column_config.TextColumn("文本 ID"),
            "English": st.column_config.TextColumn("英文原文", width="large"),
            "Simplified Chinese": st.column_config.TextColumn("简体中文", width="large"),
            "Traditional Chinese": st.column_config.TextColumn("繁体中文", width="large")
        }
    )
else:
    st.info("未找到匹配的内容，请尝试其他关键词。")

# 页脚研究小贴士
st.sidebar.markdown("---")
st.sidebar.info("💡 **研究小贴士**：\n你可以通过搜索特定的术语（如 'Fade' 或 'Inquisitor'）来观察三语在宗教、头衔上的翻译取舍。")