import csv
import sys
from tempfile import NamedTemporaryFile
import shutil
import os
import subprocess

def read_price_txt(file_path):
    """读取price.txt文件并返回价格信息和国家代码"""
    prices = []
    with open(file_path, 'r', encoding='utf-8') as f:
        # 跳过空行
        while True:
            line = next(f).strip()
            if line:
                break
        
        # 解析国家代码
        countries = [code.strip() for code in line.split() if code.strip()]
        if len(countries) != 2:
            raise ValueError(f"标题行格式错误: {line}，应该包含两个国家代码")
            
        for line in f:
            # 跳过空行
            if not line.strip():
                continue
            try:
                # 分割并清理数据
                values = [x.strip().replace('\t', '') for x in line.split(',')]
                if len(values) != 2:
                    print(f"警告：无法解析行: {line.strip()}")
                    continue
                    
                # 转换为浮点数
                prices_dict = {}
                # 注意：这里交换了值的顺序，因为在price.txt中是SG,RU，但值是RU,SG
                values.reverse()
                for country, value in zip(countries, values):
                    prices_dict[country] = int(float(value) * 1000000)
                prices.append(prices_dict)
                
            except ValueError as e:
                print(f"警告：无法解析行: {line.strip()}")
                continue
                
    return countries, prices

def parse_price_string(price_str):
    """解析CSV中的Price字段"""
    parts = price_str.split(';')
    prices = {}
    for i in range(0, len(parts), 2):
        country = parts[i].strip()
        try:
            price = int(parts[i + 1].strip())
            prices[country] = price
        except ValueError:
            continue
    return prices

def format_price_string(prices):
    """将价格字典转换为CSV格式的字符串"""
    parts = []
    for country, price in prices.items():
        parts.extend([country, str(price)])
    return '; '.join(parts)

def verify_prices(csv_path, price_txt_path):
    """使用price_checker.py验证价格"""
    print("\n正在验证更新后的价格...")
    try:
        result = subprocess.run(
            ['./venv/bin/python', 'price_checker.py', csv_path, price_txt_path],
            capture_output=True,
            text=True,
            check=True
        )
        print("\n验证结果:")
        print(result.stdout)
        if result.stderr:
            print("验证过程中的警告:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print("验证过程中出现错误:")
        print(e.stdout)
        print(e.stderr)
        raise Exception("价格验证失败")

def update_prices(csv_path, price_txt_path):
    """更新CSV文件中的价格"""
    # 读取price.txt中的价格和国家代码
    countries, expected_prices = read_price_txt(price_txt_path)
    print(f"\n将检查并更新以下国家的价格: {', '.join(countries)}")
    
    # 创建临时文件
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8')
    changes = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            writer = csv.DictWriter(tempfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            
            for row_num, row in enumerate(reader, start=2):
                price_str = row.get('Price', '')
                if not price_str:
                    writer.writerow(row)
                    continue
                
                # 解析CSV中的价格
                prices = parse_price_string(price_str)
                
                # 如果没有SG价格，跳过
                if 'SG' not in prices:
                    writer.writerow(row)
                    continue
                
                # 查找匹配的预期价格
                sg_price = prices['SG']
                price_updated = False
                old_price_str = price_str
                
                for expected in expected_prices:
                    if abs(sg_price - expected['SG']) < 100:  # 允许小误差
                        # 找到匹配的SG价格，检查其他价格是否需要更新
                        for country in countries:
                            if country != 'SG' and (country not in prices or 
                                    abs(prices.get(country, 0) - expected[country]) >= 100):
                                # 需要更新价格
                                old_price = prices.get(country, 'N/A')
                                prices[country] = expected[country]
                                changes.append({
                                    'row': row_num,
                                    'country': country,
                                    'old_price': old_price,
                                    'new_price': expected[country],
                                    'old_price_str': old_price_str,
                                    'new_price_str': format_price_string(prices)
                                })
                                price_updated = True
                        break
                
                if price_updated:
                    # 更新价格字符串
                    row['Price'] = format_price_string(prices)
                
                writer.writerow(row)
        
        # 替换原文件
        shutil.move(tempfile.name, csv_path)
        
    except Exception as e:
        # 清理临时文件
        os.unlink(tempfile.name)
        raise e
    
    return changes

def main():
    if len(sys.argv) != 3:
        print("使用方法: python price_updater.py <csv文件> <price.txt文件>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    price_txt_path = sys.argv[2]
    
    try:
        changes = update_prices(csv_path, price_txt_path)
        
        if changes:
            print("\n价格更新记录:")
            print("行号 | 国家 | 原价格 | 新价格")
            print("-" * 120)  # 增加分隔线长度
            
            for change in changes:
                # 打印基本信息
                print(f"{change['row']:3d} | {change['country']:4s} | {change['old_price']:12} | {change['new_price']:12d}")
                # 打印完整的Price字段内容
                print(f"原始Price: {change['old_price_str']}")
                print(f"更新Price: {change['new_price_str']}")
                print("-" * 120)  # 每条记录之间添加分隔线
            
            print(f"\n总计更新了 {len(changes)} 处价格")
        else:
            print("\n所有价格都是正确的，无需更新")
        
        # 验证更新后的价格
        verify_prices(csv_path, price_txt_path)
            
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
