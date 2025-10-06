from enum import Enum
from htmlnode import LeafNode
class TextType(Enum):
    TEXT = "text"
    BOLD = "i"
    ITALIC ="i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"
    
class TextNode:
    def __init__(self,text,text_type,url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None,value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag=text_node.text_type,value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag=text_node.text_type,value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag=text_node.text_type,value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag=text_node.text_type,value=text_node.text,props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag=text_node.text_type,value="",props={"src":text_node.url,"alt":text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
