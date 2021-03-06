import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import \
    Material as MaterialModel, \
    MaterialSpecification as MaterialSpecificationModel

from .attribute import AttributeInput
from .base import NamedInput
from .helpers import get_model_by_id_or_name, update_model_from_input
from .identifier import IdentifierInput
from .organization import OrganizationInput
from .property import PropertyInput


# noinspection PyMethodParameters
class MaterialSpecification(DjangoObjectType):
    class Meta:
        model = MaterialSpecificationModel


# noinspection PyMethodParameters
class Material(DjangoObjectType):
    class Meta:
        model = MaterialModel


class MaterialSpecificationInput(NamedInput):
    description = graphene.String()
    version = graphene.String()
    parent = graphene.InputField(lambda: MaterialSpecificationInput)
    attributes = graphene.List(AttributeInput)
    identifiers = graphene.List(IdentifierInput)
    properties = graphene.List(PropertyInput)
    supplier = graphene.InputField(OrganizationInput)


class MaterialInput(NamedInput):
    description = graphene.String()
    specification = graphene.Field(MaterialSpecificationInput)
    # process = graphene.Field(Process)
    # process_step = graphene.Field(Process)
    attributes = graphene.List(AttributeInput)
    identifiers = graphene.List(IdentifierInput)
    properties = graphene.List(PropertyInput)
    producer = graphene.InputField(OrganizationInput)


# noinspection PyMethodParameters,PyMethodMayBeStatic
class MaterialQuery(graphene.ObjectType):
    materials = graphene.List(Material)
    material_specs = graphene.List(MaterialSpecification)

    def resolve_materials(root, info) -> List[MaterialModel]:
        return MaterialModel.objects.all()

    def resolve_material_specs(root, info) -> List[MaterialSpecificationModel]:
        return MaterialSpecificationModel.objects.all()


class UpdateMaterial(graphene.Mutation):
    class Arguments:
        material = MaterialInput(required=True)

    material = graphene.Field(Material)

    def mutate(root, info, material=None):
        mat_model = get_model_by_id_or_name(MaterialModel, material)
        if mat_model is None:
            mat_model = MaterialModel()
        update_model_from_input(mat_model, material)
        mat_model.save()
        return UpdateMaterial(material=mat_model)


class UpdateMaterialSpecification(graphene.Mutation):
    class Arguments:
        material_spec = MaterialSpecificationInput(required=True)

    material_spec = graphene.Field(MaterialSpecification)

    def mutate(root, info, material_spec=None):
        spec_model = get_model_by_id_or_name(MaterialSpecificationModel, material_spec)
        if spec_model is None:
            spec_model = MaterialSpecificationModel()
        update_model_from_input(spec_model, material_spec)
        spec_model.save()
        return UpdateMaterialSpecification(material_spec=spec_model)


class MaterialMutation(graphene.ObjectType):
    update_material = UpdateMaterial.Field()
    update_material_spec = UpdateMaterialSpecification.Field()
