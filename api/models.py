import sys, inspect
from dateutil.tz import UTC

from django.db import models

from dateutil import rrule
from datetime import datetime, timedelta

from sklearn import neighbors

from .utils import date_compare


class Address(models.Model):
    street = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    corner_or_ave = models.CharField(max_length=100)
    apto = models.CharField('No. Y/O APTO', max_length=100)

    def __str__(self) -> str:
        return '{} {} {} {}'.format(self.province, self.street, self.municipality, self.corner_or_ave)

    class Meta:
        db_table = 'address'
        # unique_together = ['street', 'municipality',
        #                    'province', 'neighborhood', 'corner_or_ave', 'apto']


class Core(models.Model):
    code = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100)
    district = models.PositiveIntegerField()
    political_area = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    subordinate = models.CharField(max_length=100)

    def integrantes(self):
        militant = Militant.objects.filter(core=self.code)
        return militant

    def __str__(self) -> str:
        return self.core_name

    class Meta:
        db_table = 'core'    


class DeclarationDate(models.Model):
    date = models.DateTimeField(primary_key=True)

    def __str__(self) -> str:
        return self.declaration_date.__str__()

    class Meta:
        db_table = 'declaration_date'


class PaymentDate(models.Model):
    date = models.DateField(primary_key=True)

    def __str__(self) -> str:
        return self.payment_date.__str__()

    class Meta:
        db_table = 'payment_date'


class Militant(models.Model):
    Sex = models.TextChoices('Sex', 'Masculino Femenino')
    Status = models.TextChoices('Status', 'Casado/a Soltero/a Divorciado/a')
    ci = models.CharField(primary_key=True, max_length=11)
    name = models.CharField(max_length=100)
    first_lastname = models.CharField(max_length=100)
    second_lastname = models.CharField(max_length=100)
    # sexo = models.CharField(max_length=10, choices=Sexo.choices)
    # estado = models.CharField(max_length=20, choices=Estado.choices)
    register_date = models.DateTimeField(default=datetime.now())
    core = models.ForeignKey(
        Core, related_name='militants', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    declaration_date = models.ManyToManyField(
        DeclarationDate, through='PaymentDeclaration')

    def payment_contribution(self):
        payments = Payment.objects.filter(
            payment_declaration__militant__ci=self.ci)
        return Payment

    def payment_declaration(self):
        return PaymentDeclaration.objects.filter(militant=self.ci)

    def arrears_fees(self):
        arrears_fees = []
        real_decla = PaymentDeclaration.real_payment_declaration(self)

        start = self.register_date
        end = datetime.now(UTC) - timedelta(days = datetime.now(UTC).day - 1)
        
        payments = []
        i_decla = 0

        for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
            backwardness = True
            share = {'year': dt.year, 'month': dt.month, 'amount_payable': None, 'amount_paid': None}
            if i_decla < len(real_decla) and date_compare(dt, real_decla[i_decla]):
                payments = Payment.objects.filter(
                    payment_declaration = real_decla[i_decla])

                sum = 0
                for pay in payments:
                    sum += pay.amount
                if sum < real_decla[i_decla].share:
                    share['amount_payable'] = real_decla[i_decla].share
                    share['amount_paid'] = sum
                else:
                    backwardness = False
                i_decla += 1

            if backwardness:
                arrears_fees.append(share)

        return arrears_fees

    def __str__(self) -> str:
        return self.militant_name

    class Meta:
        db_table = 'militant'


class PaymentNorm(models.Model):
    lower_limit = models.PositiveIntegerField(primary_key=True)
    upper_limit = models.PositiveIntegerField()
    percent = models.PositiveIntegerField(null=True)
    amount_to_pay = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = 'payment_norm'
        unique_together = (('lower_limit', 'upper_limit'))


class PaymentDeclaration(models.Model):
    salary = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    payment_norm = models.ForeignKey(
        PaymentNorm, on_delete=models.CASCADE)
    share = models.PositiveIntegerField()
    declaration_date = models.ForeignKey(
        DeclarationDate, on_delete=models.CASCADE)
    militant = models.ForeignKey(
        Militant, related_name='payment_declaration', on_delete=models.CASCADE)
    payment_date = models.ManyToManyField(PaymentDate, through='Payment')

    @staticmethod
    def real_payment_declaration(ci):
        declarations_query = PaymentDeclaration.objects.filter(
            payment_militant=ci).order_by('-year', '-month')

        declarations = []

        if len(declarations_query) > 0:
            declarations.append(declarations_query[0])

        for i in range(1, len(declarations_query)):
            query_i = declarations_query[i]
            query_ip1 = declarations_query[i - 1]
            if query_i.year != query_ip1.year or query_i.month != query_ip1.month:
                declarations.append(query_i)

        return list(reversed(declarations))

    class Meta:
        db_table = 'payment_declaration'
        # unique_together = ['declaration_date', 'militant', 'id']

    def __str__(self) -> str:
        return self.militant.name + " salary of " + str(self.salary)

class Payment(models.Model):
    payment_declaration = models.ForeignKey(
        PaymentDeclaration, on_delete=models.CASCADE)
    payment_date = models.ForeignKey(PaymentDate, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self) -> str:
        return '{} pago en {} con {} pesos'.format(self.payment_declaration.__str__(), self.payment_date.__str__(), str(self.amount))

    class Meta:
        db_table = 'payment'
        unique_together = (('payment_declaration', 'payment_date'))


class Task(models.Model):
    name = models.CharField(max_length=100)
    orientation = models.TextField()
    militants = models.ManyToManyField(Militant, through='Participant')

    class Meta:
        db_table = 'task'

    def __str__(self) -> str:
        return self.task_name + ' ' + self.orientation


class Participant(models.Model):
    militant = models.ForeignKey(Militant, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    Eval = models.TextChoices('Evaluación', 'Excelente Bien Majomeno Mal')
    evaluation = models.CharField(max_length=10, choices=Eval.choices)

    class Meta:
        db_table = 'participant'
        unique_together = (('militant', 'task'))

    def __str__(self) -> str:
        return self.militant.name + ' ' + self.task.name
