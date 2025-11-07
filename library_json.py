import json
import os
class Book:
    def __init__(self, ID, name, author, publisher):
        self.ID = ID
        self.name = name
        self.author = author
        self.publisher = publisher
        self.borrow = True          # True：可借；False：已借出
        self.borrow_count=0         # 附加功能：借阅次数
    def print_book(self):
        return f"{self.ID} 《{self.name}》 {self.author} {self.publisher} " \
               f"{'可借' if self.borrow else '已借出'} 已借{self.borrow_count}次"


class Library:
    def __init__(self,db_file="library.json"):
        self.db_file = db_file
        self.booklist = []          # 馆藏图书列表
        self.borrow_book = {}       # 借阅记录：{图书ID: 借阅人姓名}
        self.history={}             # 历史借阅
        self._load()                # 自动加载
    # 附加功能：自动加载
    def _load(self):
        if not os.path.exists(self.db_file):
            return
        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.booklist = [Book(**b) for b in data["books"]]
            self.borrow_book = data.get("current", {})
            self.history = {k: v for k, v in data.get("history", {}).items()}
            print("已自动加载本地数据。")
        except Exception as e:
            print("加载失败，启动空库：", e)
    # 附加功能：手动/自动保存     
    def save(self):
        try:
            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump({
                    "books": [x.__dict__ for x in self.booklist],
                    "current": self.borrow_book,
                    "history": self.history
                }, f, ensure_ascii=False, indent=2)
            print("已自动保存到本地。")
        except Exception as e:
            print("保存失败：", e)
    # 添加图书
    def add_book(self):
        ID   = input("请输入图书编号：")
        name = input("请输入书名：")
        author    = input("请输入作者：")
        publisher = input("请输入出版社：")

        # 编号查重
        for x in self.booklist:
            if x.ID == ID:
                print("添加失败：编号已存在！")
                return

        book = Book(ID, name, author, publisher)
        self.booklist.append(book)
        print("添加成功！")
        print(f"新书信息：{book.print_book()}")
        self.save()             # 自动保存

    # 查询图书
    def search_book(self, mode, keyword):
        keyword = keyword.strip()
        if mode == 'name':
            hits = [x for x in self.booklist if keyword in x.name]
        elif mode == 'author':
            hits = [x for x in self.booklist if x.author == keyword]
        else:
            hits = []

        if hits:
            print(f"查询成功，共 {len(hits)} 本：")
            for x in hits:
                print(x.print_book())
        else:
            print("查询失败：未找到符合条件的图书。")

    # 修改图书信息
    def update_book_name(self, ID, name):
        for x in self.booklist:
            if x.ID == ID:
                x.name = name
                print("修改成功！")
                print(f"修改后信息：{x.print_book()}")
                self.save()             # 自动保存
                return
        print("修改失败：未找到该编号图书。")
    def update_book_author(self, ID, author):
        for x in self.booklist:
            if x.ID == ID:
                x.author = author
                print("修改成功！")
                print(f"修改后信息：{x.print_book()}")
                self.save()             # 自动保存
                return
        print("修改失败：未找到该编号图书。")
    def update_book_publisher(self, ID, publisher):
        for x in self.booklist:
            if x.ID == ID:
                x.publisher = publisher
                print("修改成功！")
                print(f"修改后信息：{x.print_book()}")
                self.save()             # 自动保存
                return
        print("修改失败：未找到该编号图书。")
    def update_book_borrow(self, ID):
        for x in self.booklist:
            if x.ID == ID:
                if not x.borrow:
                    print("标记失败：该书已处于借出状态。")
                    return
                x.borrow = False
                x.borrow_count += 1          # 借出次数+1
                print("标记成功！")
                print(f"标记后信息：{x.print_book()}")
                self.save()             # 自动保存
                return
        print("标记失败：未找到该编号图书。")
    
    # 删除图书
    def delete(self, ID):
        for x in self.booklist:
            if x.ID == ID:
                if not x.borrow:
                    print("删除失败：该书已借出，无法删除。")
                    return
                self.booklist.remove(x)
                print("删除成功！")
                print(f"已删除图书信息：{x.print_book()}")
                self.save()             # 自动保存
                return
        print("删除失败：未找到该编号图书。")
    
    # 借阅图书（附加：统计）
    def borrow(self, ID, borrower):
        for x in self.booklist:
            if x.ID == ID:
                if not x.borrow:
                    print("借阅失败：该书已借出。")
                    return
                x.borrow = False
                x.borrow_count += 1     # 统计+1
                self.borrow_book[ID] = borrower
                self.history.setdefault(borrower, []).append(ID)    #写入历史 
                print("借阅成功！")
                print(f"借阅图书信息：{x.print_book()}")
                print(f"借阅人：{borrower}")
                self.save()             # 自动保存
                return
        print("借阅失败：未找到该编号图书。")
    
    # 归还图书（附加：统计）
    def return_book(self, ID):
        for x in self.booklist:
            if x.ID == ID:
                if x.borrow:
                    print("归还失败：该书未被借阅。")
                    return
                x.borrow = True
                self.borrow_book.pop(ID, None)
                print("归还成功！")
                print(f"归还图书信息：{x.print_book()}")
                self.save()             # 自动保存
                return
        print("归还失败：未找到该编号图书。")
    
    # 附加功能：统计某人历史
    def user_history(self, borrower):
        ids = self.history.get(borrower, [])
        if not ids:
            print(f"{borrower} 暂无借阅历史。")
            return
        print(f"{borrower} 历史借阅记录（{len(ids)} 次）：")
        for i, bid in enumerate(ids, 1):
            book = next((b for b in self.booklist if b.ID == bid), None)
            if book:
                print(f"  {i}. {book.print_book()}")
            else:
                print(f"  {i}. [图书已下架] {bid}")
# 主程序
library = Library()
while True:
    print("输入数字即可\n1 添加图书  2 查询图书  3 修改信息  4 删除图书  5 借阅图书  6 归还图书  7 借阅统计  0 退出")
    choice = input("请选择操作：").strip()
    if choice == "1":
        library.add_book()
    elif choice == "2":
        mode = input("按书名查询请输入 name，按作者查询请输入 author：").strip()
        keyword = input("请输入关键词：").strip()
        library.search_book(mode, keyword)
    elif choice == "3":
        print("1 修改书名  2 修改作者  3 修改出版社  4 标记为已借出")
        sub = input("请选择修改项：").strip()
        book_id = input("请输入图书编号：").strip()
        if sub == "1":
            new_name = input("新书名：").strip()
            library.update_book_name(book_id, new_name)
        elif sub == "2":
            new_author = input("新作者：").strip()
            library.update_book_author(book_id, new_author)
        elif sub == "3":
            new_pub = input("新出版社：").strip()
            library.update_book_publisher(book_id, new_pub)
        elif sub == "4":
            library.update_book_borrow(book_id)
        else:
            print("选择错误，请重试！")
    elif choice == "4":
        book_id = input("请输入要删除的图书编号：").strip()
        library.delete(book_id)
    elif choice == "5":
        borrower = input("请输入借阅人姓名：").strip()
        book_id = input("请输入图书编号：").strip()
        library.borrow(book_id, borrower)
    elif choice == "6":
        book_id = input("请输入要归还的图书编号：").strip()
        library.return_book(book_id)
    elif choice == "7":
        borrower = input("请输入要统计的借阅人姓名：").strip()
        library.user_history(borrower)
    elif choice == "0":
        library.save()          # 退出时自动保存
        print("查询完成，下次再见")
        break
    else:
        print("输入无效，请重新选择")