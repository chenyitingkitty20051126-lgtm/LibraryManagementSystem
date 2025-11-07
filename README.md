#  简易图书馆资源管理系统 (Library Management System)

使用 **Python + 面向对象 OOP + JSON 持久化** 开发的终端图书管理系统。

---

## 功能 Features

| 功能模块 | 描述 |
|----------|------|
| 添加图书 | 新增 Book 实例，自动保存 |
| 查询图书 | 支持：按书名模糊查询 / 按作者精确查询 |
| 修改图书信息 | 修改书名 / 作者 / 出版社 / 标记借出 |
| 删除图书 | 借出状态下不能删除（数据安全保护） |
| 借阅 / 归还 | 支持借阅记录和借阅次数统计 |
| 自动保存 JSON（附加） | 每次操作自动写入 `library.json` |
| 借阅历史统计（附加） | 可查询某人的借阅历史 |

---

## 程序架构（Illustration 图示）

> 满足课程 PPT 要求：**至少一幅图示 + 清楚表明系统结构**

 **系统架构图（Data Flow）**

<img src="img/System_DataFlow.png" width="550">

**UML 类图（Class Diagram）**

<img src="img/UML_ClassDiagram.png" width="550">

 **程序流程图（Main Loop Flowchart）**

<img src="img/Flowchart.png" width="550">

> 图片均存放在 `/img` 文件夹，若图片未显示，请检查文件路径。

---

## 🛠 运行方法（Run）

运行主程序：

```bash
python library.py
