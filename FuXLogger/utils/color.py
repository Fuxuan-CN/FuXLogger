import enum
import re
from .exceptions import RendererException

class Color(enum.Enum):
    """
    定义终端文本颜色的枚举类。
    """
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    PURPLE = '\033[95m'
    RESET = '\033[0m'
    GREY = '\033[90m'

class Font(enum.Enum):
    """
    定义终端文本字体样式的枚举类。
    """
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDE = '\033[8m'

def getColorDICT() -> dict[str, str]:
    """
    返回一个包含所有颜色枚举的字典。
    """
    colorDict = {color.name: color.value for color in Color}
    return colorDict

def getFontDICT() -> dict[str, str]:
    """
    返回一个包含所有字体样式枚举的字典。
    """
    fontDict = {font.name: font.value for font in Font}
    return fontDict

class Render:
    """
    提供文本渲染功能的类。
    """

    @staticmethod
    def render(text: str, color: Color, font: Font) -> str:
        """
        根据指定的颜色和字体样式渲染文本。

        :param text: 要渲染的文本。
        :param color: 颜色枚举值。
        :param font: 字体样式枚举值。
        :return: 渲染后的文本。
        """
        return f"{color.value}{font.value}{text}{Color.RESET.value}" if color and font else text
    
    @staticmethod
    def removeTags(text: str) -> str:
        """
        移除XML标签。
        
        :param text: 要移除标签的文本。
        :return: 移除标签后的文本。
        """
        pattern = r'<(\w+):(\w+)>(.*?)</(\w+):(\w+)>'
        return re.sub(pattern, r'\3', text, flags=re.DOTALL)
    
    @staticmethod
    def renderWithXML(text: str | bytes) -> str:
        """
        根据XML标签渲染文本。

        :param text: 要渲染的文本。
        :return: 渲染后的文本。
        :raises RendererException: 标签匹配错误。
        """
        colorDict = getColorDICT()
        fontDict = getFontDICT()
        pattern = r'<(\w+):(\w+)>(.*?)</(\w+):(\w+)>'
        def replaceFunc(match):
            start_color_name: str = match.group(1)
            start_font_name: str = match.group(2)
            content: str = match.group(3)
            end_color_name: str = match.group(4)
            end_font_name: str = match.group(5)

            # 检查开始和结束标签是否匹配
            if start_color_name.upper() != end_color_name.upper() or start_font_name.upper() != end_font_name.upper():
                raise RendererException(f"Mismatched tags: <{start_color_name}:{start_font_name}> does not match </{end_color_name}:{end_font_name}>")
            
            start_color = colorDict.get(start_color_name.upper())
            start_font = fontDict.get(start_font_name.upper())
            if start_color and start_font:
                return f"{start_color}{start_font}{content}{Color.RESET.value}"
            elif start_color:
                return f"{start_color}{content}{Color.RESET.value}"
            elif start_font:
                return f"{start_font}{content}{Color.RESET.value}"
            else:
                return content
        return re.sub(pattern, replaceFunc, text, flags=re.DOTALL) # type: ignore
    
if __name__ == '__main__':
    # text = "This is <purple:bold>purple</blue:bold> and <red:underline>red</red:underline> text."
    # print(Render.renderWithXML(text))
    # if you do this, you will get a exception: Mismatched tags: <purple:bold> does not match </blue:bold>
    pass
    