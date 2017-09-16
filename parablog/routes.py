class _Route:
    """
    Route Object used to define routes.
    """
    NAME = None
    PATH = None

    def __init__(self, name, path):
        self.NAME = name
        self.PATH = path

    @property
    def config(self):
        return [self.NAME, self.PATH]


class ROUTES:
    POSTS = _Route('blog_post', '/posts')
    POST_DETAILS = _Route('blog_post_details', '/posts/{uri}')
    POST_COMMENTS = _Route('blog_post_comments', '/posts/{uri}/comments')


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route(*ROUTES.POSTS.config)
    config.add_route(*ROUTES.POST_DETAILS.config)
    config.add_route(*ROUTES.POST_COMMENTS.config)

