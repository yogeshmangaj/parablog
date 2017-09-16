from pyramid.view import view_config, view_defaults

from parablog.const import METHODS
from parablog.models import BlogPost
from parablog.routes import ROUTES
from parablog.services.blogpost import BlogPostService
from parablog.services.comment import CommentService
from parablog.utils import alchemy_result_to_dict


@view_config(route_name='home', renderer='json')
def home_view(request):
    return {'project': 'parablog'}


class ViewsMixin(object):
    def __init__(self, request):
        self.request = request

    def success(self, response_dictionary=None):
        if not response_dictionary:
            response_dictionary = dict()
        self.request.response.status = 200
        return response_dictionary


@view_defaults(route_name=ROUTES.POSTS.NAME)
class BlogPostsViews(ViewsMixin):
    def __init__(self, request):
        super(BlogPostsViews, self).__init__(request)
        self.posts_service = BlogPostService(self.request.dbsession)

    @view_config(request_method=METHODS.GET)
    def list_posts(self):
        posts_list = []
        for post in self.posts_service.list(columns=[
            BlogPost.title, BlogPost.created_at, BlogPost.updated_at, BlogPost.uri, BlogPost.id
        ]):
            posts_list.append(alchemy_result_to_dict(post))
        return posts_list

    @view_config(request_method=METHODS.POST)
    def add_post(self):
        title = self.request.json_body['title']
        content = self.request.json_body['content']
        post = self.posts_service.create(title, content)
        return self.success({"uri": post.uri})


@view_defaults(route_name=ROUTES.POST_DETAILS.NAME)
class BlogPostDetailsViews(ViewsMixin):
    def __init__(self, request):
        super(BlogPostDetailsViews, self).__init__(request)
        self.posts_service = BlogPostService(self.request.dbsession)
        self.comments_service = CommentService(self.request.dbsession)

    @view_config(request_method=METHODS.GET)
    def get_post_details(self):
        uri = self.request.matchdict['uri']
        post = self.posts_service.get_by_uri(uri)
        resp = post.as_dict()
        comments = {}
        for comment in self.comments_service.get_by_blogpost_id(post.id):
            para_id = comment.paragraph_id
            if para_id not in comments:
                comments[para_id] = []
            comments[para_id].append(comment.as_dict())
        resp['comments'] = comments
        return self.success(resp)


@view_defaults(route_name=ROUTES.POST_COMMENTS.NAME)
class BlogPostCommentsViews(ViewsMixin):
    def __init__(self, request):
        super(BlogPostCommentsViews, self).__init__(request)
        self.posts_service = BlogPostService(self.request.dbsession)
        self.comments_service = CommentService(self.request.dbsession)

    @view_config(request_method=METHODS.POST)
    def add_comment(self):
        uri = self.request.matchdict['uri']
        content = self.request.json_body['content']
        paragraph_id = int(self.request.json_body['paragraph_id'])
        post = self.posts_service.get_by_uri(uri)
        comment = self.comments_service.add(post.id, paragraph_id, content)
        return self.success({'comment_id': comment.id})



db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_parablog_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
