from textnode import TextNode, TextType
from split_node_delimiter import extract_markdown_images


def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    res = extract_markdown_images(text="This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
    print(res)
    
if __name__ == "__main__":
    main()