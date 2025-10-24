# CFPS数据处理工程

一个用于自动化整理中国家庭追踪调查(CFPS)数据的Python工具包。

## 📋 项目简介

本项目提供了一个强大的数据生成器，可以根据您的需求自动化整理CFPS数据。支持多年份数据合并、变量映射、缺失值处理等功能。

## 🚀 主要功能

- ✅ **多年份数据合并**：支持2010-2022年任意年份组合
- ✅ **智能变量映射**：自动处理不同年份间的变量名差异
- ✅ **缺失值处理**：自动将CFPS的缺失值编码转换为标准NaN
- ✅ **权重支持**：可选择是否包含权重变量
- ✅ **高效存储**：输出parquet格式，支持快速读取
- ✅ **灵活配置**：支持自定义变量和年份选择
- ✅ **性别差异分析**：自动生成箱线图展示性别差异
- ✅ **可视化输出**：生成PDF格式的分析图表

## 📁 项目结构

```
cfps-working-dir/
├── data_generator.py      # 主要的数据生成器类
├── utils.py              # 工具函数（数据路径获取）
├── configs.py            # 配置文件
├── cfps-merge.csv        # 变量映射文件
├── test_generator.py     # 测试脚本
├── usage_example.py      # 使用示例
└── README.md            # 项目说明文档
```

## 🛠️ 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install pandas numpy pyarrow matplotlib seaborn scipy
```

## 📖 使用方法

### 基本使用

```python
from data_generator import CFPSDataGenerator

# 创建数据生成器
generator = CFPSDataGenerator()

# 生成数据集
output_path = generator.generate_dataset(
    years=[2018, 2020, 2022],           # 选择年份
    variables=['gender', 'hukou', 'education'],  # 选择变量
    output_name="my_cfps_data",         # 输出文件名
    include_weight=True                 # 是否包含权重
)
```

### 查看可用变量

```python
# 获取所有可用变量
available_vars = generator.get_available_variables()
print(f"总共 {len(available_vars)} 个变量")

# 查看前20个变量
print(available_vars[:20])
```

### 检查变量可用性

```python
# 检查特定变量在特定年份的可用性
mapping = generator.get_variable_mapping(
    variables=['gender', 'hukou', 'education'],
    years=[2018, 2020]
)
print(mapping)
```

## 📊 支持的变量类型

### 人口统计学变量
- `gender` - 性别
- `hukou` - 户口类型
- `education` - 教育水平
- `minzu` - 民族
- `age` - 年龄

### 教育相关变量
- `primary` - 小学教育
- `middle` - 初中教育
- `high` - 高中教育
- `bachelor` - 本科教育

### 其他变量
- `military` - 军人身份
- `onlychild` - 独生子女
- `residence3` - 3岁居住地
- `hukou3` - 3岁户口
- `residence12` - 12岁居住地
- `hukou12` - 12岁户口

## 🔧 配置说明

### 数据路径配置

在 `configs.py` 中设置您的CFPS数据路径：

```python
CFPS_BASE_DIR = "/path/to/your/cfps/data"
SUPPORTED_YEARS = [2010, 2012, 2014, 2016, 2018, 2020, 2022]
```

### 变量映射文件

`cfps-merge.csv` 文件包含了所有变量的映射关系，包括：
- 变量名在各年份的对应列名
- 变量的标签信息
- 变量的可用性信息

## 📝 使用示例

### 示例1：生成人口统计学数据集

```python
from data_generator import CFPSDataGenerator

generator = CFPSDataGenerator()

# 选择人口统计学变量
demographic_vars = ['gender', 'hukou', 'education', 'minzu', 'age']
years = [2018, 2020, 2022]

# 生成数据集
output_path = generator.generate_dataset(
    years=years,
    variables=demographic_vars,
    output_name="cfps_demographic_2018_2022",
    include_weight=True
)

print(f"数据集已生成: {output_path}")
```

### 示例2：生成教育相关数据集

```python
# 选择教育相关变量
education_vars = ['education', 'primary', 'middle', 'high', 'bachelor']
years = [2020, 2022]

output_path = generator.generate_dataset(
    years=years,
    variables=education_vars,
    output_name="cfps_education_2020_2022",
    include_weight=True
)
```

### 示例3：性别差异分析

```python
# 运行性别差异分析脚本
python generate_internet_data.py
# 选择选项 3: 性别差异分析 (生成图表)

# 或者直接调用分析函数
from generate_internet_data import analyze_gender_differences
analyze_gender_differences()
```

这将生成三个PDF文件：
- `output/internet_usage_gender_differences.pdf` - 互联网使用频率性别差异
- `output/internet_importance_gender_differences.pdf` - 互联网重要性性别差异  
- `output/internet_info_gender_differences.pdf` - 互联网信息获取性别差异

## 🧪 测试

运行测试脚本验证功能：

```bash
python test_generator.py
```

运行使用示例：

```bash
python usage_example.py
```

## 📋 输出数据格式

生成的数据集包含以下列：

- `year` - 年份
- `pid` - 个人ID
- `weight` - 权重（如果选择包含）
- 您选择的所有变量列

数据以parquet格式存储，支持快速读取和分析。

## ⚠️ 注意事项

1. **数据路径**：请确保在 `configs.py` 中正确设置CFPS数据路径
2. **文件存在性**：确保对应的DTA文件存在于指定路径
3. **变量可用性**：某些变量可能在某些年份不可用，系统会给出警告
4. **缺失值处理**：系统自动将CFPS的缺失值编码(-10, -9, -8, -2, -1)转换为NaN

## 🔄 数据清理流程

1. **变量映射**：根据cfps-merge.csv自动匹配各年份的变量名
2. **数据读取**：从DTA文件读取指定列
3. **缺失值处理**：将CFPS的缺失值编码转换为标准NaN
4. **数据合并**：将多年份数据合并为统一格式
5. **输出存储**：保存为parquet格式文件

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目采用MIT许可证。

---

**注意**：本项目需要访问CFPS原始数据文件。请确保您有合法的数据访问权限。
