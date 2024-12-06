import csv
import sys

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

def check_prices(csv_path, price_txt_path):
    """检查价格是否匹配"""
    # 读取price.txt中的价格和国家代码
    countries, expected_prices = read_price_txt(price_txt_path)
    print(f"\n将检查以下国家的价格: {', '.join(countries)}")
    
    # 读取CSV文件
    results = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            price_str = row.get('Price', '')
            if not price_str:
                continue
            
            # 解析CSV中的价格
            prices = parse_price_string(price_str)
            
            # 检查是否包含所有需要的国家代码
            if not all(country in prices for country in countries):
                continue
            
            # 检查是否匹配price.txt中的任何一组价格
            for expected in expected_prices:
                # 检查第一个国家的价格是否匹配
                if abs(prices[countries[0]] - expected[countries[0]]) < 100:  # 允许小误差
                    # 找到匹配的价格，检查第二个国家的价格
                    is_match = abs(prices[countries[1]] - expected[countries[1]]) < 100  # 允许小误差
                    results.append({
                        'row': row_num,
                        'actual_prices': {country: prices[country] for country in countries},
                        'expected_prices': expected,
                        'match': is_match
                    })
                    break
    
    return countries, results

def main():
    if len(sys.argv) != 3:
        print("使用方法: python price_checker.py <csv文件> <price.txt文件>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    price_txt_path = sys.argv[2]
    
    countries, results = check_prices(csv_path, price_txt_path)
    
    print("\n价格检查结果:")
    # 构建动态的表头
    header = "行号 |"
    for country in countries:
        header += f" {country}实际价格 | {country}期望价格 |"
    header += " 结果"
    print(header)
    print("-" * (len(header) + 20))
    
    for result in results:
        row = f"{result['row']:3d} |"
        for country in countries:
            row += f" {result['actual_prices'][country]:11d} | {result['expected_prices'][country]:11d} |"
        status = "✓ 正确" if result['match'] else "✗ 错误"
        row += f" {status}"
        print(row)
    
    # 汇总
    total = len(results)
    matches = sum(1 for r in results if r['match'])
    print(f"\n总结: 共检查 {total} 行，其中 {matches} 行价格正确，{total - matches} 行价格错误")

if __name__ == "__main__":
    main()
