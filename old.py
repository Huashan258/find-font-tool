from fontTools.ttLib import TTFont
import os
from pathlib import Path


def get_font_postscript_name(font_path: str) -> tuple[str | None, str | None]:

    try:
        font = TTFont(font_path, lazy=True)

        family_name = None
        postscript_name = None
        for record in font['name'].names:
            if record.nameID == 1:
                family_name = record.toUnicode()
            elif record.nameID == 6:
                postscript_name = record.toUnicode()

        font.close()

        return family_name, postscript_name

    except Exception as e:
        print(f"读取字体文件 {os.path.basename(font_path)} 失败：{e}")
        return None, None


def scan_fonts_in_current_directory() -> list[dict]:

    font_info_list = []
    font_extensions = ('.ttf', '.otf', '.ttc', '.otc')

    current_directory = Path(__file__).resolve().parent

    for root, _, files in os.walk(current_directory):
        for file in files:
            if file.lower().endswith(font_extensions):
                file_path = os.path.abspath(os.path.join(root, file))
                family_name, postscript_name = get_font_postscript_name(file_path)

                if postscript_name:
                    font_info_list.append({
                        'file_path': file_path,
                        'family_name': family_name,
                        'postscript_name': postscript_name
                    })

    return font_info_list


def main():
    print("正在使用 fontTools 扫描当前程序目录下的字体文件...")
    font_info_list = scan_fonts_in_current_directory()

    if font_info_list:
        print(f"\n共找到 {len(font_info_list)} 个有效字体文件：")
        print("-" * 80)
        current_directory = Path(__file__).resolve().parent
        for i, font_info in enumerate(font_info_list, 1):
            relative_path = os.path.relpath(font_info['file_path'], current_directory)
            print(
                f"{i:3d}. 家族名称：{font_info['family_name']:20s} | PostScript 名称：{font_info['postscript_name']:25s} | 文件：{relative_path}")
        print("-" * 80)
    else:
        print("\n在当前程序目录及其子目录下未找到任何可识别的有效字体文件。")


if __name__ == "__main__":
    main()