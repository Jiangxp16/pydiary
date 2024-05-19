from core.util import config_utils
zh_dict = {
    "Cancel": "取消",
    "OK": "确定",
    "PASSWORD": "密码",
    "password": "密码",
    "Password:": "密码：",
    "Input Password": "输入密码",
    "Add Password or Leave It Empty.": "设置密码（可为空）",
    "Password must be less than 16 characters!": "密码不能超过16个字符",
    "Password not match!": "密码不匹配!",
    "Mon": "周一",
    "Tue": "周二",
    "Wed": "周三",
    "Thu": "周四",
    "Fri": "周五",
    "Sat": "周六",
    "Sun": "周日",
    "AUTO": "自动",
    "location": "位置",
    "whether": "天气",
    "Diary": "日记",
    "Interest": "兴趣",
    "Bill": "账单",
    "Note": "笔记",
    "Exit": "退出",
    "All": "全部",
    "Movie": "电影",
    "TV": "电视",
    "Comic": "动漫",
    "Game": "游戏",
    "Book": "书籍",
    "Music": "音乐",
    "Others": "其它",
    "Added": "添加日期",
    "Name": "名称",
    "Sort": "分类",
    "Prog": "进度",
    "Pub": "发布",
    "Last": "最后日期",
    "Score\r\n(db)": "评分\r\n(db)",
    "Score\r\n(imdb)": "评分\r\n(imdb)",
    "Score": "评分",
    "Remark": "备注",
    "Search...": "搜索...",
    "Delete information in current page?": "删除当前页内容？",
    "Import from xlsx file [REPLACE!]": "从xlsx文件导入[覆盖]",
    "Export to xlsx file": "导出到xlsx文件",
    "Date": "日期",
    "Inout": "收支",
    "Type": "类型",
    "Amount": "金额",
    "Item": "项目",
    "In": "收入",
    "Out": "支出",
    "Total": "合计",
    "Import from xlsx file": "从xlsx文件导入",
    "Begin": "初始日期",
    "Process": "进度",
    "Desire": "期望值",
    "Priority": "优先级",
    "Content": "内容",
    "Input Old Password": "输入旧密码",
    "OLD PASSWORD": "旧密码",
    "Old password not match!": "旧密码不匹配",
    "Input New Password": "输入新密码",
    "New Password": "新密码",
    "New password not match!": "新密码不匹配",
}
def tr(x): return x


def tr_cn(text: str):
    return zh_dict.get(text, text)


language = config_utils.load_config("global", "language")
if language == "zh":
    tr = tr_cn