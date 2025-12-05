import graphene
from django.core.paginator import Paginator
from ...models import User
from ..Types.user_type import UserType

class UserPaginatedType(graphene.ObjectType):
    items = graphene.List(UserType)
    total_count = graphene.Int()
    num_pages = graphene.Int()
    current_page = graphene.Int()
    page_size = graphene.Int()

class UserQuery(graphene.ObjectType):
    users = graphene.Field(
        UserPaginatedType,
        username=graphene.String(),
        email=graphene.String(),
        role=graphene.String(),
        page=graphene.Int(default_value=1),
        page_size=graphene.Int(default_value=10)
    )
    user = graphene.Field(UserType, id=graphene.Int())

    @staticmethod
    def resolve_users(root, info, username=None, email=None, role=None, page=1, page_size=10, **kwargs):
        queryset = User.objects.all().order_by('-date_joined')

        if username:
            queryset = queryset.filter(username__icontains=username)
        
        if email:
            queryset = queryset.filter(email__icontains=email)

        if role:
            # Filtrage par nom de rôle (relation ManyToMany)
            queryset = queryset.filter(roles__name__iexact=role)

        paginator = Paginator(queryset, page_size)
        
        try:
            page_obj = paginator.page(page)
        except:
            page_obj = paginator.page(1)

        return UserPaginatedType(
            items=page_obj.object_list,
            total_count=paginator.count,
            num_pages=paginator.num_pages,
            current_page=page_obj.number,
            page_size=page_size
        )

    @staticmethod
    def resolve_user(root, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
