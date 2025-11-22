"""
使用 fontTools 库扫描当前目录下的字体文件。
支持两种输出模式：
1. 仅显示 PostScript 名称 (nameID=6)
2. 显示所有 nameID 对应的信息
"""

from fontTools.ttLib import TTFont
import os
from pathlib import Path


def get_font_name_data(font_path: str) -> dict | None:
    """
    读取字体文件的所有 name 表数据。

    :param font_path: 字体文件路径
    :return: 包含文件路径和所有 name 记录的字典，如果出错则返回 None
    """
    try:
        font = TTFont(font_path, lazy=True)
        name_data = []

        # 遍历所有 name 记录
        for record in font['name'].names:
            try:
                # 尝试将名称记录解码为 Unicode
                content = record.toUnicode()
            except UnicodeDecodeError:
                # 如果解码失败，使用十六进制表示原始字节
                content = record.string.hex()

            name_data.append({
                'nameID': record.nameID,
                'platformID': record.platformID,
                'langID': record.langID,
                'content': content
            })

        font.close()

        return {
            'file_path': font_path,
            'name_data': name_data
        }

    except Exception as e:
        print(f"读取字体文件 {os.path.basename(font_path)} 失败：{e}")
        return None


def scan_fonts_in_current_directory() -> list[dict]:
    """
    扫描当前目录及其子目录下的所有字体文件，并读取其 name 表数据。
    """
    font_info_list = []
    font_extensions = ('.ttf', '.otf', '.ttc', '.otc')

    current_directory = Path(__file__).resolve().parent

    for root, _, files in os.walk(current_directory):
        for file in files:
            if file.lower().endswith(font_extensions):
                file_path = os.path.abspath(os.path.join(root, file))
                font_data = get_font_name_data(file_path)

                if font_data:
                    font_info_list.append(font_data)

    return font_info_list


def display_font_info(font_info_list: list[dict], mode: int):
    """
    根据指定模式显示字体信息。

    :param font_info_list: 包含字体信息的列表
    :param mode: 1 - 仅显示 PostScript 名称, 2 - 显示所有信息
    """
    if not font_info_list:
        print("\n在当前程序目录及其子目录下未找到任何可识别的有效字体文件。")
        return

    current_directory = Path(__file__).resolve().parent

    if mode == 1:
        print(f"\n共找到 {len(font_info_list)} 个有效字体文件 (仅显示 PostScript 名称):")
        print("-" * 80)
        for i, font_info in enumerate(font_info_list, 1):
            relative_path = os.path.relpath(font_info['file_path'], current_directory)
            postscript_name = "N/A"
            # 查找 nameID=6 的记录
            for name_record in font_info['name_data']:
                if name_record['nameID'] == 6:
                    postscript_name = name_record['content']
                    break
            print(f"{i:3d}. 文件: {relative_path:<40} | PostScript 名称 (nameID=6): {postscript_name}")
        print("-" * 80)

    elif mode == 2:
        print(f"\n共找到 {len(font_info_list)} 个有效字体文件 (显示所有 nameID 信息):")
        print("=" * 80)
        for i, font_info in enumerate(font_info_list, 1):
            relative_path = os.path.relpath(font_info['file_path'], current_directory)
            print(f"\n[{i}] 文件: {relative_path}")
            print("-" * 60)
            for name_record in font_info['name_data']:
                print(
                    f"  nameID={name_record['nameID']:2d}, platformID={name_record['platformID']}, langID={name_record['langID']:4d}: {name_record['content']}")
        print("=" * 80)


def main():
    print("字体文件扫描工具")
    print("1. 仅输出 PostScript 名称 (nameID=6)")
    print("2. 输出所有 nameID 信息")

    while True:
        try:
            choice = int(input("\n请选择模式 (1 或 2): "))
            if choice in [1, 2]:
                break
            else:
                print("无效的选择，请输入 1 或 2。")
        except ValueError:
            print("无效的输入，请输入一个数字 (1 或 2)。")

    print(f"\n正在使用 fontTools 扫描当前程序目录下的字体文件 (模式: {choice})...")
    font_info_list = scan_fonts_in_current_directory()

    display_font_info(font_info_list, choice)


if __name__ == "__main__":
    main()