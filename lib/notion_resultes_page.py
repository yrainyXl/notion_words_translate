
#获取到返回的一些查询操作
#获取页面id
def get_page_id(page):
    return page["id"]

#获取checkbox属性
def get_checkbox(page,properties_name):
    return page["properties"][properties_name]["checkbox"]

def get_title(page, prop_name):
    """获取标题类型属性"""
    prop = page["properties"].get(prop_name, {})
    if "title" in prop and len(prop["title"]) > 0:
        return prop["title"][0].get("text", {}).get("content", "")
    return "空标题"

def get_checkbox(page, prop_name):
    """获取复选框类型属性"""
    return page["properties"].get(prop_name, {}).get("checkbox", False)

def get_rich_text(page, prop_name):
    """获取富文本类型属性"""
    prop = page["properties"].get(prop_name, {})
    if "rich_text" in prop:
        return "".join(
            [text.get("text", {}).get("content", "") 
                for text in prop["rich_text"]]
        )
    return ""

def get_select(page, prop_name):
    """获取单选类型属性"""
    select = page["properties"].get(prop_name, {}).get("select")
    return select.get("name") if select else None

def get_multi_select(page, prop_name):
    """获取多选类型属性"""
    multi_select = page["properties"].get(prop_name, {}).get("multi_select", [])
    return [option["name"] for option in multi_select]

def get_date(page, prop_name):
    """获取日期类型属性"""
    date = page["properties"].get(prop_name, {}).get("date")
    if date:
        return {
            "start": date.get("start"),
            "end": date.get("end")
        }
    return {}

def get_number(page, prop_name):
    """获取数字类型属性"""
    return page["properties"].get(prop_name, {}).get("number")

def get_url(page, prop_name):
    """获取URL类型属性"""
    return page["properties"].get(prop_name, {}).get("url")

def get_formula(page, prop_name):
    """获取公式类型属性"""
    formula = page["properties"].get(prop_name, {}).get("formula")
    if formula:
        formula_type = formula.get("type")
        return formula.get(formula_type)
    return None
def print_pages(pages):
    for page in pages:
        print(f"\n--- Page ID: {page['id']} ---")
        properties = page.get("properties", {})
        
        for prop_name, prop_value in properties.items():
            print(f"\n属性名: {prop_name}")
            
            # 处理不同类型属性的值
            if "title" in prop_value:
                # 处理标题类型
                title = prop_value["title"]
                content = [t["text"]["content"] for t in title if "text" in t]
                print(f"类型: title, 值: {''.join(content)}")
                
            elif "rich_text" in prop_value:
                # 处理富文本类型
                rich_text = prop_value["rich_text"]
                content = [t["text"]["content"] for t in rich_text if "text" in t]
                print(f"类型: rich_text, 值: {''.join(content)}")
                
            elif "checkbox" in prop_value:
                # 处理复选框类型
                print(f"类型: checkbox, 值: {prop_value['checkbox']}")
                
            elif "select" in prop_value and prop_value["select"]:
                # 处理选择类型
                print(f"类型: select, 值: {prop_value['select'].get('name', '无')}")
                
            elif "multi_select" in prop_value:
                # 处理多选类型
                values = [opt["name"] for opt in prop_value["multi_select"]]
                print(f"类型: multi_select, 值: {', '.join(values)}")
                
            elif "date" in prop_value and prop_value["date"]:
                # 处理日期类型
                start = prop_value["date"].get("start", "无")
                end = prop_value["date"].get("end", "无")
                print(f"类型: date, 开始: {start}, 结束: {end}")
                
            elif "number" in prop_value:
                # 处理数字类型
                print(f"类型: number, 值: {prop_value['number']}")
                
            elif "url" in prop_value:
                # 处理URL类型
                print(f"类型: url, 值: {prop_value['url']}")
                
            elif "formula" in prop_value:
                # 处理公式类型
                formula_type = prop_value["formula"]["type"]
                value = prop_value["formula"][formula_type]
                print(f"类型: formula({formula_type}), 值: {value}")
                
            else:
                # 其他未处理类型
                print(f"未处理的属性类型: {prop_value.get('type', '未知')}")
                print(f"原始数据: {prop_value}")
                
