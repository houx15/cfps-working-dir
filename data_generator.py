"""
CFPS数据生成器
根据用户需求自动化整理CFPS数据
"""

import pandas as pd
import numpy as np
import os
from typing import List, Dict, Optional
import warnings

warnings.filterwarnings("ignore")

from utils import get_dta_path
from configs import CFPS_BASE_DIR, SUPPORTED_YEARS, OUTPUT_DIR


class CFPSDataGenerator:
    """CFPS数据生成器类"""

    def __init__(self, merge_file_path: str = "cfps-merge.csv"):
        """
        初始化数据生成器

        Args:
            merge_file_path: cfps-merge.csv文件路径
        """
        self.merge_file_path = merge_file_path
        self.merge_df = None
        self._load_merge_file()

    def _load_merge_file(self):
        """加载变量映射文件"""
        try:
            self.merge_df = pd.read_csv(self.merge_file_path)
            print(f"成功加载变量映射文件，共{len(self.merge_df)}个变量")
        except Exception as e:
            raise Exception(f"无法加载变量映射文件: {e}")

    def get_available_variables(self) -> List[str]:
        """获取所有可用变量列表"""
        return self.merge_df["variable"].tolist()

    def get_variable_mapping(
        self, variables: List[str], years: List[int]
    ) -> Dict[str, Dict[int, str]]:
        """
        获取变量在各年份的列名映射

        Args:
            variables: 需要的变量列表
            years: 需要的年份列表

        Returns:
            变量映射字典 {variable: {year: column_name}}
        """
        mapping = {}

        for var in variables:
            if var not in self.merge_df["variable"].values:
                print(f"警告: 变量 '{var}' 在映射文件中未找到")
                continue

            var_row = self.merge_df[self.merge_df["variable"] == var].iloc[0]
            mapping[var] = {}

            for year in years:
                year_str = str(year)
                if (
                    year_str in var_row.index
                    and pd.notna(var_row[year_str])
                    and var_row[year_str] != 0
                ):
                    # 检查是否有对应的label列
                    label_col = f"{year}-label"
                    if label_col in var_row.index and pd.notna(var_row[label_col]):
                        mapping[var][year] = var_row[label_col]
                    else:
                        mapping[var][year] = var_row[year_str]
                else:
                    print(f"警告: 变量 '{var}' 在 {year} 年不可用")

        return mapping

    def read_dta_with_missing_handling(
        self, file_path: str, columns: List[str]
    ) -> pd.DataFrame:
        """
        读取DTA文件并处理缺失值

        Args:
            file_path: DTA文件路径
            columns: 需要读取的列名列表

        Returns:
            处理后的DataFrame
        """
        try:
            # 读取DTA文件，设置convert_categoricals=False来读取数值而不是标签
            df = pd.read_stata(
                file_path,
                columns=columns,
                preserve_dtypes=False,
                convert_categoricals=False,
            )

            # 处理缺失值：将-10, -9, -8, -2, -1替换为NaN
            missing_values = [-10, -9, -8, -2, -1]
            for col in df.columns:
                if df[col].dtype in ["int64", "float64"]:
                    df[col] = df[col].replace(missing_values, np.nan)

            return df

        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            return pd.DataFrame()

    def generate_dataset(
        self,
        years: List[int],
        variables: List[str],
        output_name: str,
        include_weight: bool = False,
    ) -> str:
        """
        生成数据集

        Args:
            years: 需要的年份列表
            variables: 需要的变量列表
            output_name: 输出文件名（不含扩展名）
            include_weight: 是否包含权重变量

        Returns:
            输出文件路径
        """
        print(f"开始生成数据集...")
        print(f"年份: {years}")
        print(f"变量: {variables}")
        print(f"输出文件名: {output_name}")

        # 验证年份
        invalid_years = [y for y in years if y not in SUPPORTED_YEARS]
        if invalid_years:
            raise ValueError(f"不支持的年份: {invalid_years}")

        # 获取变量映射
        var_mapping = self.get_variable_mapping(variables, years)

        # 存储所有年份的数据
        all_data = []

        for year in years:
            print(f"\n处理 {year} 年数据...")

            # 获取该年份的DTA文件路径
            dta_path = get_dta_path(year, "adult")

            if not os.path.exists(dta_path):
                print(f"警告: 文件不存在 {dta_path}")
                continue

            # 构建该年份需要的列
            year_columns = ["pid"]  # 基础列
            # if include_weight:
            #     year_columns.append("weight")

            # 添加变量列
            for var in variables:
                if var in var_mapping and year in var_mapping[var]:
                    year_columns.append(var_mapping[var][year])

            # 读取数据
            year_df = self.read_dta_with_missing_handling(dta_path, year_columns)

            if year_df.empty:
                print(f"警告: {year} 年数据为空")
                continue

            # 添加年份列
            year_df["year"] = year

            # 重命名变量列为标准名称
            rename_dict = {}
            for var in variables:
                if var in var_mapping and year in var_mapping[var]:
                    rename_dict[var_mapping[var][year]] = var

            year_df = year_df.rename(columns=rename_dict)

            # 只保留需要的列
            final_columns = ["year", "pid"] + [
                var for var in variables if var in year_df.columns
            ]
            # if include_weight and "weight" in year_df.columns:
            #     final_columns.append("weight")

            year_df = year_df[final_columns]
            all_data.append(year_df)

            print(f"{year} 年数据: {len(year_df)} 条记录")

        if not all_data:
            raise Exception("没有成功读取任何数据")

        # 合并所有年份数据
        print(f"\n合并数据...")
        final_df = pd.concat(all_data, ignore_index=True)

        # 输出为parquet文件
        output_path = os.path.join(OUTPUT_DIR, f"{output_name}.parquet")
        final_df.to_parquet(output_path, index=False)

        print(f"\n数据集生成完成!")
        print(f"总记录数: {len(final_df)}")
        print(f"年份分布: {final_df['year'].value_counts().sort_index().to_dict()}")
        print(f"输出文件: {output_path}")

        return output_path


def main():
    """主函数 - 示例用法"""
    # 创建数据生成器
    generator = CFPSDataGenerator()

    # 显示可用变量
    print("可用变量示例:")
    available_vars = generator.get_available_variables()
    print(available_vars[:10])  # 显示前10个变量

    # 示例：生成一个简单的数据集
    years = [2018, 2020]
    variables = ["gender", "hukou", "education"]
    output_name = "cfps_demo"

    try:
        output_path = generator.generate_dataset(
            years=years,
            variables=variables,
            output_name=output_name,
            include_weight=True,
        )
        print(f"\n成功生成数据集: {output_path}")
    except Exception as e:
        print(f"生成数据集时出错: {e}")


if __name__ == "__main__":
    main()
