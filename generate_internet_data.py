"""
生成CFPS互联网相关变量2010-2022年数据
"""

from data_generator import CFPSDataGenerator

# 定义全局变量列表，避免重复定义
INTERNET_VARS = [
    "gender",  # 性别 - 重要！
    "internetLearn",  # 互联网学习
    "internetWork",  # 互联网工作
    "internetSocial",  # 互联网社交
    "internetEntertain",  # 互联网娱乐
    "internetCommercial",  # 互联网商业
    "internetLearn20201",  # 互联网学习2020-1
    "internetLearn20202",  # 互联网学习2020-2
    "internetLearn20221",  # 互联网学习2022-1
    "internetLearn20222",  # 互联网学习2022-2
    "game",  # 游戏
    "gameFreq",  # 游戏频率
    "shopping",  # 购物
    "shoppingFreq",  # 购物频率
    "video",  # 视频
    "videoFreq",  # 视频频率
    "wechat",  # 微信
    "wechatFreq",  # 微信频率
    "internetImportLearn",  # 互联网重要性-学习
    "internetImportWork",  # 互联网重要性-工作
    "internetImportSocial",  # 互联网重要性-社交
    "internetImportEntertain",  # 互联网重要性-娱乐
    "internetImportCommercial",  # 互联网重要性-商业
    "infoInternet",  # 信息互联网
    "infoTV",  # 信息电视
    "infoNews",  # 信息新闻
    "infoRadio",  # 信息广播
    "infoMobile",  # 信息手机
]

# 年份列表
YEARS = [2010, 2012, 2014, 2016, 2018, 2020, 2022]


def generate_internet_dataset():
    """生成互联网相关变量的完整数据集"""

    # 创建数据生成器
    generator = CFPSDataGenerator()

    print("=== CFPS互联网数据生成器 ===")
    print(f"变量数量: {len(INTERNET_VARS)}")
    print(f"年份范围: {min(YEARS)}-{max(YEARS)}")
    print(f"变量列表: {INTERNET_VARS}")

    # 检查变量可用性
    print("\n检查变量可用性...")
    mapping = generator.get_variable_mapping(INTERNET_VARS, YEARS)

    # 显示每个变量的可用年份
    available_vars = {}
    for var, year_mapping in mapping.items():
        if year_mapping:  # 如果变量有可用年份
            available_vars[var] = list(year_mapping.keys())
            print(f"  {var}: {sorted(year_mapping.keys())}")
        else:
            print(f"  {var}: 无可用年份")

    print(f"\n找到 {len(available_vars)} 个可用变量")

    # 生成数据集
    try:
        print("\n开始生成数据集...")
        output_path = generator.generate_dataset(
            years=YEARS,
            variables=INTERNET_VARS,
            output_name="cfps_internet_2010_2022",
            include_weight=True,
        )

        print(f"\n✅ 数据集生成成功!")
        print(f"输出文件: {output_path}")

        # 显示数据集信息
        import pandas as pd

        df = pd.read_parquet(output_path)
        print(f"\n数据集信息:")
        print(f"总记录数: {len(df):,}")
        print(f"年份分布:")
        year_counts = df["year"].value_counts().sort_index()
        for year, count in year_counts.items():
            print(f"  {year}: {count:,} 条记录")

        print(f"\n列名: {list(df.columns)}")

        return output_path

    except Exception as e:
        print(f"❌ 生成数据集时出错: {e}")
        return None


def analyze_gender_differences(data_path=None):
    """分析互联网变量的性别差异并生成图表"""
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os

    # 设置中文字体
    plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    # 创建输出目录
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("=== 互联网变量性别差异分析 ===")

    # 定义变量组
    group1_vars = [
        "internetLearn",
        "internetWork",
        "internetSocial",
        "internetEntertain",
        "internetCommercial",
    ]
    group2_vars = [
        "internetImportLearn",
        "internetImportWork",
        "internetImportSocial",
        "internetImportEntertain",
        "internetImportCommercial",
    ]
    group3_vars = [
        "infoInternet",
        "infoTV",
        "infoNews",
        "infoRadio",
        "infoMobile",
    ]

    try:
        # 如果提供了数据路径，直接使用；否则使用默认路径
        if data_path is None:
            data_path = "output/cfps_internet_analysis.parquet"

        if not os.path.exists(data_path):
            print(f"❌ 数据文件不存在: {data_path}")
            print("请先生成数据集，或提供正确的数据文件路径")
            return None

        # 读取数据
        df = pd.read_parquet(data_path)
        print(f"数据加载完成，共 {len(df)} 条记录")

        # 添加性别变量（假设gender变量存在）
        # 这里需要根据实际数据调整性别变量的名称
        gender_col = "gender"
        for col in df.columns:
            if "gender" in col.lower() or "sex" in col.lower():
                gender_col = col
                break

        if gender_col is None:
            print("警告：未找到性别变量，将使用所有数据进行分析")
            df["gender_group"] = "All"
        else:
            # 创建性别分组
            df["gender_group"] = df[gender_col].map({1: "Male", 0: "Female"})
            df = df.dropna(subset=["gender_group"])

        # 创建三个PDF文件
        pdf_files = [
            f"{output_dir}/internet_usage_gender_differences.pdf",
            f"{output_dir}/internet_importance_gender_differences.pdf",
            f"{output_dir}/internet_info_gender_differences.pdf",
        ]

        var_groups = [group1_vars, group2_vars, group3_vars]
        titles = [
            "互联网使用频率性别差异",
            "互联网重要性性别差异",
            "互联网信息获取性别差异",
        ]

        for pdf_file, vars_group, title in zip(pdf_files, var_groups, titles):
            print(f"\n生成 {title} 图表...")

            # 计算可用的变量和年份
            available_vars = []
            available_years = []

            for var in vars_group:
                if var in df.columns:
                    available_vars.append(var)

            for year in YEARS:
                year_data = df[df["year"] == year]
                if len(year_data) > 0:
                    available_years.append(year)

            if not available_vars or not available_years:
                print(f"跳过 {title}：没有可用数据")
                continue

            # 创建子图布局：年份为行，变量为列
            n_rows = len(available_years)
            n_cols = len(available_vars)

            fig, axes = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 3 * n_rows))

            # 处理单行或单列的情况
            if n_rows == 1 and n_cols == 1:
                axes = [[axes]]
            elif n_rows == 1:
                axes = [axes]
            elif n_cols == 1:
                axes = [[ax] for ax in axes]
            else:
                axes = axes

            fig.suptitle(f"{title}", fontsize=16, fontweight="bold")

            # 为每个年份和变量创建子图
            for row, year in enumerate(available_years):
                year_data = df[df["year"] == year]

                for col, var in enumerate(available_vars):
                    ax = axes[row][col]

                    # 准备数据 - 固定顺序：男性(1)在前，女性(0)在后
                    plot_data = []
                    labels = []
                    colors = []

                    # 按固定顺序处理性别：先男性(1)，后女性(0)
                    gender_order = ["Male", "Female"]
                    for gender in gender_order:
                        gender_data = year_data[year_data["gender_group"] == gender]
                        var_data = gender_data[var].dropna()

                        if len(var_data) > 0:
                            plot_data.append(var_data)
                            labels.append(f"{gender} (n={len(var_data)})")

                            # 设置固定颜色：男性蓝色，女性粉色
                            if gender == "Male":
                                colors.append("lightblue")
                            else:  # Female
                                colors.append("lightpink")

                    if plot_data:
                        # 创建箱线图
                        bp = ax.boxplot(plot_data, labels=labels, patch_artist=True)

                        # 设置固定颜色
                        for patch, color in zip(bp["boxes"], colors):
                            patch.set_facecolor(color)
                            patch.set_alpha(0.7)

                        # 设置标题和标签
                        ax.set_title(f"{var} ({year})", fontsize=10, fontweight="bold")
                        ax.set_ylabel("数值", fontsize=8)
                        ax.grid(True, alpha=0.3)

                        # 添加统计信息
                        if len(plot_data) == 2:
                            from scipy import stats

                            try:
                                stat, p_value = stats.ttest_ind(
                                    plot_data[0], plot_data[1]
                                )
                                ax.text(
                                    0.02,
                                    0.98,
                                    f"p={p_value:.3f}",
                                    transform=ax.transAxes,
                                    verticalalignment="top",
                                    bbox=dict(
                                        boxstyle="round", facecolor="white", alpha=0.8
                                    ),
                                    fontsize=8,
                                )
                            except:
                                pass
                    else:
                        ax.set_title(f"{var} ({year}) - 无数据", fontsize=10)
                        ax.text(
                            0.5,
                            0.5,
                            "无数据",
                            transform=ax.transAxes,
                            ha="center",
                            va="center",
                            fontsize=12,
                            alpha=0.5,
                        )

            plt.tight_layout()
            # 保存为PDF格式
            plt.savefig(pdf_file, format="pdf", bbox_inches="tight")
            plt.close()

            print(f"✅ {title} 图表已保存到: {pdf_file}")

        print(f"\n🎉 所有分析图表已生成完成！")
        print(f"输出目录: {output_dir}")
        print("生成的文件:")
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                print(f"  - {pdf_file}")

    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")
        import traceback

        traceback.print_exc()


def generate_and_analyze():
    """生成数据并进行性别差异分析"""
    print("=== 生成数据并进行性别差异分析 ===")

    # 第一步：生成完整数据集
    print("\n第一步：生成完整数据集...")
    generator = CFPSDataGenerator()

    try:
        # 生成数据集
        output_path = generator.generate_dataset(
            years=YEARS,
            variables=INTERNET_VARS,
            output_name="cfps_internet_analysis",
            include_weight=True,
        )
        print(f"✅ 数据集生成成功: {output_path}")

        # 第二步：进行性别差异分析
        print("\n第二步：进行性别差异分析...")
        analyze_gender_differences(output_path)

    except Exception as e:
        print(f"❌ 生成数据时出错: {e}")


if __name__ == "__main__":
    print("选择操作:")
    print("1. 生成完整数据集 (2010-2022)")
    print("2. 性别差异分析 (生成图表)")
    print("3. 生成数据并分析 (推荐)")

    choice = input("请输入选择 (1, 2 或 3): ").strip()

    if choice == "1":
        generate_internet_dataset()
    elif choice == "2":
        analyze_gender_differences()
    elif choice == "3":
        generate_and_analyze()
    else:
        print("无效选择，默认生成数据并分析...")
        generate_and_analyze()
