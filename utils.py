import os
from configs import CFPS_BASE_DIR, SUPPORTED_YEARS


# 用year可以获取数据地址
def get_dta_path(year: int, data_type: str = "adult"):
    if data_type == "crossyear":
        return os.path.join(CFPS_BASE_DIR, "2018", f"cfps2018_crossyear.dta")
    elif data_type == "crossyearid":
        return os.path.join(CFPS_BASE_DIR, "2020", f"cfps2020_crossyearid.dta")
    elif data_type == "community":
        return os.path.join(CFPS_BASE_DIR, "2010", f"cfps2010_comm.dta")

    try:
        assert year in SUPPORTED_YEARS
    except AssertionError:
        raise ValueError(f"Invalid year: {year}")

    year = str(year)

    if data_type == "adult":
        return os.path.join(CFPS_BASE_DIR, year, f"cfps{year}_adult.dta")
    elif data_type == "child":
        return os.path.join(CFPS_BASE_DIR, f"cfps{year}_child.dta")
    elif data_type == "famecon":
        return os.path.join(CFPS_BASE_DIR, year, f"cfps{year}_famecon.dta")
    elif data_type == "famconf":
        return os.path.join(CFPS_BASE_DIR, year, f"cfps{year}_famconf.dta")
    else:
        raise ValueError(f"Invalid data type: {data_type}")
