from enum import Enum
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import TextType, text_node_to_html_node, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            child = block_to_html_node(block)
            children.append(child)
        if block_type == BlockType.CODE:
            child = block_to_html_node(block)
            children.append(child)
        if block_type == BlockType.HEADING:
            child = block_to_html_node(block)
            children.append(child)
        if block_type == BlockType.ULIST:
            child = block_to_html_node(block)
            children.append(child)
        if block_type == BlockType.OLIST:
            child = block_to_html_node(block)
            children.append(child)
        if block_type == BlockType.QUOTE:
            child = block_to_html_node(block)
            children.append(child)
    return ParentNode("div",children)
            
def block_to_html_node(block):
    if block_to_block_type(block) == BlockType.PARAGRAPH:
        return paragraph_to_node(block)
    if block_to_block_type(block) == BlockType.CODE:
        return code_to_node(block)
    if block_to_block_type(block) == BlockType.HEADING:
        return heading_to_node(block)
    if block_to_block_type(block) == BlockType.OLIST:
        return ol_to_node(block)
    if block_to_block_type(block) == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_to_block_type(block) == BlockType.ULIST:
        return ulist_to_html_node(block)
    
def code_to_node(block):
    text = block.strip("`")
    node = TextNode(text,TextType.CODE)
    html_node = text_node_to_html_node(node)
    return ParentNode("pre",[html_node])

def heading_to_node(block):
    head_size = block.count("#")
    text = block.strip("#").strip()
    nodes = text_to_children(text)
    return ParentNode(f"h{head_size}",nodes)

def paragraph_to_node(block):
    text = " ".join(block.split("\n"))
    nodes = text_to_children(text)
    return ParentNode("p",nodes)

def ol_to_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = list(map(text_node_to_html_node,text_nodes))
    return html_nodes