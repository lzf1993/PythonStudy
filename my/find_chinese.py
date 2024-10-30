import sys
import xml.etree.ElementTree as ET


def is_comment(line):
    line = line.strip()
    return line.startswith("//") or line.startswith("/*") or line.endswith("*/") or line.startswith(
        "* ")


def contains_chinese(text):
    if text is None: return False
    try:
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
    except Exception as e:
        print(f"发生异常：{e}")
        return False


def check_file_for_chinese(file_path):
    output = ""
    with open(file_path, 'r', encoding='utf-8') as file:
        lineCount = 0
        for line in file:
            lineCount += 1
            # 注释行不检查
            if not is_comment(line) and contains_chinese(line):
                output += f'line:{lineCount} \t' + line

    if output == "":
        return output

    output = "\n" + f'-------{file_path}-------' + "\n" + output + "\n"
    return output


def check_file(file_path):
    if file_path.endswith('.kt') or file_path.endswith('.java'):
        return check_file_for_chinese(file_path)
    elif file_path.endswith('.xml'):
        return check_has_chinese_in_xml(file_path)
    else:
        return ""


def check_has_chinese_in_xml(xmlPath):
    if 'values-ja' in xmlPath:
        return f'{xmlPath} 日服xml，忽略检查'

    output = ""

    # 加载 XML 文件
    tree = ET.parse(xmlPath)
    root = tree.getroot()

    # 遍历 XML 数据
    # <string name="game_common_ready">Ready</string>
    for stringLabel in root.findall('string'):
        name = stringLabel.get('name')
        text = stringLabel.text
        data = stringLabel.find('Data')
        if data is not None:
            text = data.text

        has = contains_chinese(text)
        if has:
            output += f'<string> name: {name}, text: {text}' + "\n"

    # <string-array name="photo_array_list">
    #     <item>Album</item>
    #     <item>Camera</item>
    # </string-array>
    for stringArray in root.findall('string-array'):
        name = stringArray.get('name')

        for item in stringArray.findall('item'):
            text = item.text
            data = item.find('Data')
            if data is not None:
                text = data.text

            has = contains_chinese(text)
            if has:
                output += f'<string-array> name: {name}, text: {text}' + "\n"

    # < plurals name = "me_tab_view_7" >
    #     < item quantity = "other" >
    #       & quot; Pengunjungbaru & quot;
    #     < / item >
    # < / plurals >
    for plurals in root.findall('plurals'):
        name = plurals.get('name')
        item = plurals.find('item')

        text = item.text
        data = item.find('Data')
        if data is not None:
            text = data.text

        has = contains_chinese(text)
        if has:
            output += f'<plurals> name: {name}, text: {text}' + "\n"

    if output == "":
        return ""

    output = "\n" + f'-------{xmlPath}-------' + "\n" + output + "\n"
    return output


# 指定要检查的目录
if __name__ == '__main__':
    print("\n-------- start check chinese -----------\n")

    # codeDir = "/Users/lvqiu/AndroidStudioProjects/wejoy"
    # project_name = "wejoy"
    # class_list = "wepie/src/com/wepie/wespy/helper/dialog/DialogUtil.java,wepie/src/com/wepie/wespy/helper/imageLoader/GameImageDisplayUtil.java,wepie/src/com/wepie/wespy/module/draw/widget/msg/DrawMsgItemView.java,wepie/src/com/wepie/wespy/module/draw/DrawGuessGameView.java,wepie/src/com/wepie/wespy/module/fixroom/convene/ConveneRecentAdapter.java,wepie/src/com/wepie/wespy/module/fixroom/FixRoomActivity.java,wepie/src/com/wepie/wespy/module/game/game/base/BaseSocialGamePresenter.java,wepie/src/com/wepie/wespy/module/localpeople/activity/LocalPeopleActivity.java,wepie/src/com/wepie/wespy/module/localpeople/activity/LocalPeoplePresenter.java,wepie/src/com/wepie/wespy/module/main/manage/GameRecoverActivity.java,wepie/src/com/wepie/wespy/module/musichum/match/MusicHumBannerViewPager.java,wepie/src/com/wepie/wespy/module/musichum/MusicHumGamePresenter.java,wepie/src/com/wepie/wespy/module/spy/dialogs/SocialGameUserDialog.java,wepie/src/com/wepie/wespy/module/spy/dialogs/SpyBaseDialog.java,wepie/src/com/wepie/wespy/module/spy/dialogs/SpyBombingView.java,wepie/src/com/wepie/wespy/module/spy/dialogs/SpyDialogDoubleBtnTip.java,wepie/src/com/wepie/wespy/module/spy/dialogs/SpyDialogHelper.java,wepie/src/com/wepie/wespy/module/spy/dialogs/SpyDialogInputDesc.java,wepie/src/com/wepie/wespy/module/spy/msglist/SpyTextItem.java,wepie/src/com/wepie/wespy/module/spy/sender/SpySenderPresenter.java,wepie/src/com/wepie/wespy/module/spy/view/SpySeatView.java,wepie/src/com/wepie/wespy/module/spy/SpyGamePresenter.java,wepie/src/com/wepie/wespy/module/spy/SpyGameView.java,wepie/src/com/wepie/wespy/module/spy/SpyUtil.kt,wepie/src/com/wepie/wespy/module/voiceroom/video/youtube/views/YoutubeVideoListAdapter.java,wepie/src/com/wepie/wespy/net/tcp/handler/SpyPacketHandler.java"
    # xml_list = "wepie/res/values/strings.xml,wepie/res/values/strings_games.xml,wepie/res/values-ar/strings.xml,wepie/res/values-in/strings.xml,wepie/res/values-ja/strings.xml,wepie/res/values-ms/strings.xml,wepie/res/values-pt/strings.xml,wepie/res/values-pt/strings_games.xml,wepie/res/values-ru/strings.xml,wepie/res/values-th/strings.xml,wepie/res/values-vi/strings.xml,wepie/res/values-zh/strings.xml,wepie/res/values-zh-rTW/strings.xml"

    codeDir = sys.argv[1]
    project_name = sys.argv[2]
    class_list = sys.argv[3]
    xml_list = sys.argv[4]

    files_path = class_list.split(',') + xml_list.split(',')

    for file_path in files_path:
        if project_name == "wejoy":
            file_path = codeDir + "/" + file_path
        else:
            file_path = codeDir + "/" + project_name + "/" + file_path
        print(check_file(file_path))

    print("\n-------- end check chinese -----------\n")
