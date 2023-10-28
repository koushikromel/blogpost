import graphene
from graphene_django import DjangoObjectType
from .models import Post, Comment
from graphql import GraphQLError


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class PostType(DjangoObjectType):
    class Meta:
        model = Post
    comments = graphene.List(CommentType)

    def resolve_comments(self, info):
        return Comment.objects.filter(post=self)


class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int(required=True))


    def resolve_posts(self, info):
        return Post.objects.all()

    def resolve_post(self, info, id):
        try:
            post = Post.objects.get(pk=id)
            return post
        except Post.DoesNotExist:
            return None


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        published_date = graphene.Date()
        author = graphene.String()
    
    post = graphene.Field(PostType)

    def mutate(self, info, title, description, published_date, author):
        post = Post(title=title, description=description, published_date=published_date, author=author)
        post.save()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        title = graphene.String()
        description = graphene.String()
        published_date = graphene.String()
        author = graphene.String()
    
    post = graphene.Field(PostType)

    def mutate(self, info, id, title=None, description=None, published_date=None, author=None):
        post = Post.objects.get(pk=id)
        if title is not None:
            post.title = title
        if description is not None:
            post.description = description
        if published_date is not None:
            post.published_date = published_date
        if author is not None:
            post.author = author
        post.save()
        return UpdatePost(post=post)


class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)
        text = graphene.String()
        author = graphene.String()
    
    comment = graphene.Field(CommentType)

    def mutate(self, info, post_id, text, author):
        try:
            post = Post.objects.get(pk=post_id)
        except:
            raise GraphQLError(f"Post with the id {post_id} is not found")

        comment = Comment(post=post, text=text, author=author)
        comment.save()
        return CreateComment(comment=comment)


class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            comment = Comment.objects.get(pk=id)
            comment.delete()
            return DeleteComment(success=True)
        except:
            return DeleteComment(success=False)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
