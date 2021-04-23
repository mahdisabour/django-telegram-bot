import graphene
from graphene_django import DjangoObjectType
from rx import Observable
from .consumer import BotConsumer
from graphene_subscriptions.events import CREATED

from .models import UserBot

class UserBotType(DjangoObjectType):
    class Meta:
        model = UserBot
        fields = '__all__'

class Query(graphene.ObjectType):
    users = graphene.List(UserBotType)
    def resolve_users(self, info, **kwargs):
        return UserBot.objects.all()


# input object to create new instance
class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()


# create new object(user)
class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required= True)

    user = graphene.Field(UserBotType)

    def mutate(self, info, user_data=None):
        user_instance = UserBot(
            first_name= user_data.first_name,
            last_name= user_data.last_name
        )
        user_instance.save()
        return CreateUser(user= user_instance)


class Subscription(graphene.ObjectType):
    user_created = graphene.Field(UserBotType)

    def resolve_user_created(self, info):
        return self.filter(
            lambda event:
                event.operation == CREATED and
                isinstance(event.instance, UserBot)
        ).map(lambda event: event.instance)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)