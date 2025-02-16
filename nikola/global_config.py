import abc
import os.path

dst_path = os.path.join(os.getcwd(), '../huhuang03.github.io')
post_src = os.path.join(os.getcwd())


class IPostConfig(abc.ABC):
    @abc.abstractmethod
    def getRoot(self) -> str:
        """
        the post root
        """
        pass

    @abc.abstractmethod
    def getPattern(self) -> str:
        """
        the post src pattern
        """
        pass


class PostConfig(IPostConfig):
    def __init__(self, root: str, pattern: str):
        self.root = root
        self.pattern = pattern

    def getPattern(self):
        return self.pattern

    def getRoot(self):
        return self.root


post_config = PostConfig('../posts', '*.org')

POSTS = (
    ("../posts/*.org", "posts", "post.tmpl"),
)

OUTPUT_FOLDER = dst_path

COMPILERS = {
    "html": ['.html', '.htm'],
    "orgmode": ['.org']
}

PAGES = (
    ("pages/*.rst", "pages", "page.tmpl"),
    ("pages/*.md", "pages", "page.tmpl"),
    ("pages/*.txt", "pages", "page.tmpl"),
    ("pages/*.html", "pages", "page.tmpl"),
)
