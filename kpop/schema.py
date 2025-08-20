import graphene

from kpop.utils.upload import generate_presigned_url


class PresignedURLType(graphene.ObjectType):
    upload_url = graphene.String()
    file_url = graphene.String()


class GeneratePresignedURL(graphene.Mutation):
    class Arguments:
        filename = graphene.String(required=True)
        content_type = graphene.String(required=True)

    Output = PresignedURLType

    @classmethod
    def mutate(cls, root, info, filename, content_type):
        return generate_presigned_url(filename, content_type)


class Mutation(graphene.ObjectType):
    generate_presigned_url = GeneratePresignedURL.Field()
