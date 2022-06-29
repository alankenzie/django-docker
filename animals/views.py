# Create your views here.
from ast import IsNot
from tokenize import Token
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from characteristics.serializers import CharacteristicSerializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from groups.serializers import GroupSerializer

from .models import Animal
from .serializers import AnimalRequestSerializer, AnimalResponseSerializer, AnimalSerializer


class AnimalView(APIView):
    queryset = Animal
    serializer_class = AnimalResponseSerializer

# @extend_schema(
#     Altera o nome da visualização no navegador
#     operation_id = Optional[str] = None, 

#     Altera o serializer utilizado como parâmetros na visualização, permite adicionar campos e tipos
#     parameters = Optional[
#         List[
#             Union[
#                 drf_spectacular.utils.OpenApiParameter, 
#                 rest_framework.serializers.Serializer, 
#                 Type[rest_framework.serializers.Serializer
#                 ]
#             ]
#         ]
#     ] = None, 
#     Altera o serializer utilizado em Request
#     request = Any = <class 'rest_framework.fields.empty'>, 
# 
#     Altera o serializer utilizado em Response
#     responses = Any = <class 'rest_framework.fields.empty'>, 
# 
#     Altera a autenticação do sistema, não consegui testar
#     auth = Optional[List[str]] = None, 
#     
#     Altera a descrição da rota
#     description = Optional[str] = None, 
# 
#     Altera o sumário que aparece em frente à rota   
#     summary = Optional[str] = None, 
#    
#     Marca a operação como obsoleta
#     deprecated = Optional[bool] = None, 

#     Altera a tag da visualização
#     tags = Optional[List[str]] = None,
# 
#      
#     filters = Optional[bool] = None, 

#     Excluir a operação do schema de visualização
#     exclude = bool = False, 

#     operation = Optional[Dict] = None, 

#     methods = Optional[List[str]] = None, 

#     versions = Optional[List[str]] = None, 

#     examples = Optional[List[drf_spectacular.utils.OpenApiExample]] = None, 

#     extensions = Optional[Dict[str, Any]] = None, 

#     callbacks = Optional[List[drf_spectacular.utils.OpenApiCallback]] = None, 

#     Link para documentação externa
#     external_docs = Optional[Union[Dict[str, str], str]] = None)→ Callable[[drf_spectacular.utils.F],
#     drf_spectacular.utils.F]

# OpenApiExample ( name : str , value : Optional [ Any ] = None , external_value : str = '' , summary : str = '' , description : str = '' , request_only : bool = False , response_only : bool = False , parameter_only : Opcional [ Tuple [ str , typo_extensions.Literal [ query , path , header , cookie ] ] ] = Nenhum , media_type : str = 'application/json' , status_codes : Optional [ List [ str ] ] = None )

    @extend_schema(
        # operation_id = 'animals_post',
        # parameters=[
        #   AnimalSerializer,
        #   OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        #   OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),
        # ],
        # request=AnimalRequestSerializer,
        # responses={201: AnimalResponseSerializer},
        # description = 'Rota para criação de animais',
        # summary = 'Criação de animais',
        # deprecated = True,
        # tags = ['Criação de animais'],
        # exclude = True,
    )
    def post(self, request: Request):
        serializer = AnimalSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses=AnimalRequestSerializer(many=True)
    )
    def get(self, _):
        animals = Animal.objects.all()

        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data)


class AnimalDetailView(APIView):
    queryset = Animal
    serializer_class = AnimalSerializer

    def patch(self, request: Request, animal_id: int):
        try:
            animal = Animal.objects.get(pk=animal_id)
        except Animal.DoesNotExist:
            return Response({"message": "Animal not found"}, status=status.HTTP_404_NOT_FOUND)
        # animal = get_object_or_404(Animal, pk=animal_id)

        serializer = AnimalSerializer(animal, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except KeyError as err:
            return Response(
                {"message": err.args[0]},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, _, animal_id: int=None):
        try:
            animal = Animal.objects.get(pk=animal_id)
        except Animal.DoesNotExist:
            return Response({"message": "Animal not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AnimalSerializer(animal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, animal_id):
        try:
            animal = Animal.objects.get(pk=animal_id)
        except Animal.DoesNotExist:
            return Response({"message": "Animal not found"}, status=status.HTTP_404_NOT_FOUND)
        animal.delete()

        return Response('', status=status.HTTP_204_NO_CONTENT)