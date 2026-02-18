from textnode import *

def main():
    """
    The main function of the script.
    Contains the primary logic to be executed.
    """
    node = TextNode("Anchor text", TextType.LINK, "https://github.com/KobeLouis/static-site-generator")
    print(node)

if __name__ == "__main__":
    main()