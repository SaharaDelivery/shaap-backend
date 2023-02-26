from rest_framework import serializers


def create_serializer_class(name, fields):
    # needs documetation, refer to https://github.com/HackSoftware/Django-Styleguide#apis--serializers
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    """This function allows you to create a serializer class inline.

    Args:
        fields (_dict_): the fields of the serializer class.
        data (_type_, optional): Defaults to None.

    Returns:
       serializer object
    """
    serializer_class = create_serializer_class(name="", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
