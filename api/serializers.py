from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission

from api.models import Address, PaymentDate, Militant, Core, PaymentNorm, Payment, PaymentDeclaration, DeclarationDate


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Core
        fields = ['code', 'name', 'municipality', 'province', 'district', 'political_area',
                  'sector', 'subordinate']
                  
class PaymentNormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentNorm
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['payment_declaration']


class PaymentDeclarationSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    class Meta:
        model = PaymentDeclaration
        exclude = ['militant', 'payment', 'norm']

class DeclarationDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclarationDate
        fields = "__all__"


class PaymentDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDate
        fields = "__all__"


class MilitantSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Militant
        fields = ['ci', 'name', 'first_lastname',
                  'second_lastname', 'sex', 'status', 'address']


class MilitantPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Militant
        fields = '__all__'


class MilitantDeclarationsSerializer(serializers.ModelSerializer):
    payment_declaration = PaymentDeclarationSerializer(
        many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Militant
        fields = ['ci', 'name', 'first_lastname',
                  'second_lastname', 'address', 'payment_declaration']


class MilitantDebtsSerializer(object):

    @staticmethod
    def serialize(militants, many=False):
        indexs = []

        for mil in militants:
            share = mil.arrears_fees()
            if len(share) > 0:
                indexs.append(mil.ci)

        militants_filter = []
        for item in indexs:
            militants_filter.append(Militant.objects.get(pk=item))

        militant_debts = MilitantSerializer(militants_filter, many=True)

        index_militante = 0
        for mil in militants_filter:
            share = mil.arrears_fees()
            # amount = 'not_declared' if not share[0].get('amount') else share[0].get('amount')
            # s_debts = '{}-{}-{}'.format(share[0].get('year'), share[0].get('month'), amount)
            militant_debts.data[index_militante]['debts'] = share
            index_militante += 1

        if many:
            return militant_debts.data
        return militant_debts.data[0]


class CoreDetailSerializer(serializers.ModelSerializer):
    militants = MilitantSerializer(many=True, read_only=True)

    class Meta:
        model = Core
        fields = ['code', 'name', 'municipality', 'province', 'district', 'political_area',
                  'sector', 'subordinate', 'militants']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['last_login']


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'
