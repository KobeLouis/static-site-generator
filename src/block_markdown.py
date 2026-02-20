from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    OLIST = "ordered_list"
    ULIST = "unordered_list"
    QUOTE = "quote"
    CODE = "code"

def markdown_to_blocks(markdown: str)-> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block: str) -> BlockType:
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

def text_to_children(text: str)-> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes

def markdown_to_html_node(markdown: str) -> ParentNode:
    parent = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                # Determine how many #
                level = block.count("#", 0, block.find(" "))
                child = ParentNode(f"h{level}", [])
                if level + 1 >= len(block):
                    raise ValueError(f"invalid heading level: {level}")
                
                grand_children = text_to_children(block[level + 1:])
                child.children.extend(grand_children)

            case BlockType.CODE:
                # encase <code> in <pre>
                child = ParentNode("pre", [])
                grand_child = ParentNode("code", [])

                # Remove the first and last lines (```)
                code = block[4:-3]
                code_node = TextNode(code, TextType.TEXT)
                html_code_node = text_node_to_html_node(code_node)
                grand_child.children.append(html_code_node)
                child.children.append(grand_child)


            case BlockType.ULIST:
                # encase <li> in <ul>
                child = ParentNode("ul", [])
                
                # Seperate items and remove "- "
                items = block.split("\n")

                for item in items:
                    item = item[2:]
                    grand_child = text_to_children(item)
                    child.children.append(ParentNode("li", grand_child))



            case BlockType.OLIST:
                # encase <li> in <ol>
                child = ParentNode("ol", [])
                
                # Seperate items and remove "- "
                items = block.split("\n")

                for item in items:
                    item = item[3:]

                    grand_child = text_to_children(item)
                    child.children.append(ParentNode("li", grand_child))


            case BlockType.PARAGRAPH:
                # Remove new lines
                child = ParentNode("p", [])
                lines = block.split("\n")
                paragraph = " ".join(lines)
                grand_children = text_to_children(paragraph)
                child.children.extend(grand_children)

                
            case BlockType.QUOTE:
                child = ParentNode("blockquote", [])
                lines = block.split("\n")

                for line in lines:
                    if not line.startswith(">"):
                        raise ValueError(f"Invalid quote block: line does not start with >: {line}")
                    
                    lines = [line.strip(">").strip() for line in lines]
                quote = " ".join(lines)
                grand_children = text_to_children(quote)
                child.children = grand_children
            
            case _:
                raise ValueError(f"Unsupported block type: {block_type}")

        parent.children.append(child)

    
    return parent

