# Preluma 课程报告写作指南

## 中文题目
Preluma：基于 Python 的课前学习准备度诊断平台设计与实现

## English Title
Preluma: Design and Implementation of a Python-Based Pre-Class Readiness Diagnostic Platform

## 摘要要点
本项目使用 Python 实现一个面向学生和教师的课前学习准备度平台。学生可以选择课程主题，完成预习引导、知识理解、测验和错题诊断；教师可以通过数据看板查看学生准备度、薄弱技能和学习趋势。项目核心部分使用 CSV 文件进行数据持久化，手动实现统计分析、归并排序和二分查找，并将运行结果保存到 result.txt。界面层使用 Streamlit 和 Plotly 提升交互体验。

## 关键字
Python；课前学习；学习分析；CSV；归并排序；二分查找；Streamlit

## 正文章节建议

1. 研究背景与意义
   - 课前预习质量影响课堂参与度。
   - 教师需要快速了解学生薄弱点。
   - Preluma 将学生端预习和教师端诊断结合。

2. 文献综述
   - 智能教学系统
   - 学习分析 Learning Analytics
   - 形成性评价 Formative Assessment

3. 任务分析
   - 学生端：主题选择、知识卡片、测验、错题诊断。
   - 教师端：CSV 数据读取、统计分析、排序、搜索、可视化。
   - 课程要求：CSV、统计、手动排序、手动搜索、计时、result.txt。

4. 方法阐述
   - 模块设计：main.py, data_loader.py, analyzer.py, models.py, storage_core.py, algorithms_core.py, analytics_core.py, streamlit_app.py。
   - 数据结构：StudentRecord, AnalysisResult。
   - 算法：Merge Sort, Binary Search, manual mean/variance。
   - 异常处理：CSV 文件不存在、数字转换错误、网络失败 fallback。

5. 结果分析
   - 展示运行截图。
   - 展示 result.txt 内容。
   - 展示教师看板和学生测验结果。

6. 总结
   - 项目达到预期目标。
   - 核心算法符合课程要求。
   - 后续可加入真实课程资料库、教师账户、更多学习模型。

7. 参考文献
   - Python 官方文档
   - Streamlit 官方文档
   - Learning Analytics 相关论文或教材

8. 附录
   - 核心代码片段
   - 项目结构
   - 测试结果
