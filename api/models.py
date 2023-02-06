from dateutil.tz import UTC

from django.db import models

from dateutil import rrule
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator

from .utils import date_compare


def validate_null_strings(value):
    if len(value) <= 0:
        raise ValidationError('{} must not be null'.format(value))


def validate_int_number(value):
    try:
        int(value)
    except:
        raise ValidationError(
            'A valid integer is required.')


class Address(models.Model):
    street = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    corner_or_ave = models.CharField(max_length=100)
    apto = models.CharField('No. Y/O APTO', max_length=100)

    def is_valid(self):
        address = Address.objects.filter(
            street=self.street, municipality=self.municipality,
            province=self.province, neighborhood=self.neighborhood,
            corner_or_ave=self.corner_or_ave, apto=self.apto)
        valid_length = len(self.street) > 0 or len(self.municipality) > 0
        valid_length = valid_length or len(
            self.province) > 0 or len(self.neighborhood) > 0
        valid_length = valid_length or len(
            self.corner_or_ave) > 0 or len(self.apto) > 0
        return len(address) == 0 and valid_length

    def save(self, *args, **kwargs):
        if not self.is_valid():
            raise ValueError('Address must exist.')
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return '{} {} {} {}'.format(self.province, self.street, self.municipality, self.corner_or_ave)

    class Meta:
        db_table = 'address'
        # unique_together = ['street', 'municipality',
        #                    'province', 'neighborhood', 'corner_or_ave', 'apto']


class Core(models.Model):
    code = models.CharField(primary_key=True, max_length=5, validators=[
                            MinLengthValidator(
                                5, message='Min length of code must have more than 4 numbers.'),
                            MaxLengthValidator(
                                5, message='Min length of code must have less than 6 numbers.'),
                            validate_int_number])
    name = models.CharField(max_length=100, validators=[
                            MinLengthValidator(
                                1, message='Name cannot be empty.')])
    municipality = models.CharField(max_length=100, validators=[
        MinLengthValidator(
            1, message='Municipality cannot be empty.')])
    province = models.CharField(max_length=100, validators=[
        MinLengthValidator(
                                1, message='Province cannot be empty.')])
    district = models.PositiveIntegerField(validators=[
        MinValueValidator(
            1, message='District cannot be empty.',)])
    political_area = models.CharField(max_length=100, validators=[
        MinLengthValidator(
            1, message='Political area cannot be empty.')])
    sector = models.CharField(max_length=100, validators=[
        MinLengthValidator(
            1, message='Sector cannot be empty.')])
    subordinate = models.CharField(max_length=100, validators=[
        MinLengthValidator(
            1, message='Subordinate cannot be empty.')])

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'core'


class DeclarationDate(models.Model):
    date = models.DateTimeField(primary_key=True)

    def __str__(self) -> str:
        return self.date.__str__()

    class Meta:
        db_table = 'declaration_date'


class PaymentDate(models.Model):
    date = models.DateTimeField(primary_key=True)

    def __str__(self) -> str:
        return self.date.__str__()

    class Meta:
        db_table = 'payment_date'


class Militant(models.Model):
    Sex = models.TextChoices('Sex', 'Masculino Femenino')
    Status = models.TextChoices('Status', 'Casado/a Soltero/a Divorciado/a')
    ci = models.CharField(primary_key=True, max_length=11,
                          validators=[MinLengthValidator(11)])
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    first_lastname = models.CharField(
        max_length=100, validators=[MinLengthValidator(1)])
    second_lastname = models.CharField(
        max_length=100, validators=[MinLengthValidator(1)])
    core = models.ForeignKey(
        Core, related_name='militants', on_delete=models.CASCADE)
    register_date = models.DateTimeField(default=datetime.now())
    sex = models.CharField(max_length=10, choices=Sex.choices, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    payment_declaration = models.ManyToManyField(
        DeclarationDate, through='PaymentDeclaration')
    
    house_phone = models.CharField(max_length=10,  null=True)
    work_phone = models.CharField(max_length=10,  null=True)
    cell_phone  = models.CharField(max_length=10,  null=True)

    email = models.CharField(max_length=100,  null=True)
    pcc_position = models.CharField(max_length=20,  null=True)
    observations = models.CharField(max_length=100,  null=True) 
    pcc_reserve_position = models.CharField(max_length=20,  null=True)
    institutional_reserve_positon = models.CharField(max_length=100,  null=True)
   
    birth_year = models.PositiveIntegerField(null=True)
    age = models.PositiveIntegerField(null=True)
    
    job = models.CharField(max_length=100,  null=True)
    job_clasification = models.CharField(max_length=100,  null=True)
    no_ci = models.CharField(max_length=20,  null=True)
    fundator = models.BooleanField(default=False)
    skin_color = models.CharField(max_length=1,  null=True)
    scolarity = models.PositiveIntegerField(null=True) 
    work_file = models.CharField(max_length=20, null=True)

    def payment_contribution(self):
        payments = Payment.objects.filter(
            payment_declaration__militant__ci=self.ci)
        return payments

    def payment_declaration(self):
        return PaymentDeclaration.objects.filter(militant=self.ci)

    def arrears_fees(self):
        arrears_fees = []
        real_decla = PaymentDeclaration.real_payment_declaration(self)

        start = self.register_date
        end = datetime.now(UTC) - timedelta(days=datetime.now(UTC).day - 1)

        payments = []
        i_decla = 0

        for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
            backwardness = True
            share = {'year': dt.year, 'month': dt.month,
                     'amount_payable': None, 'amount_paid': None}
            if i_decla < len(real_decla) and date_compare(dt, real_decla[i_decla]):
                payments = Payment.objects.filter(
                    payment_declaration=real_decla[i_decla])

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

    def is_valid(self):
        return len(self.ci) > 0 and len(self.name) > 0 and len(self.second_lastname) > 0

    def save(self, *args, **kwargs):
        if not self.is_valid():
            raise ValueError('Address must exist')
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

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
    norm = models.ForeignKey(
        PaymentNorm, on_delete=models.CASCADE)
    share = models.PositiveIntegerField()
    declaration_date = models.ForeignKey(
        DeclarationDate, on_delete=models.CASCADE)
    militant = models.ForeignKey(
        Militant, related_name='payment_declaration', on_delete=models.CASCADE)
    payment = models.ManyToManyField(PaymentDate, through='Payment')

    @staticmethod
    def real_payment_declaration(ci):
        declarations_query = PaymentDeclaration.objects.filter(
            militant=ci).order_by('-year', '-month', '-declaration_date')

        declarations = []

        if len(declarations_query) > 0:
            declarations.append(declarations_query[0])

        for i in range(1, len(declarations_query)):
            query_i = declarations_query[i]
            query_ip1 = declarations_query[i - 1]
            if query_i.year != query_ip1.year or query_i.month != query_ip1.month:
                declarations.append(query_i)

        return list(reversed(declarations))

    def save(self, *args, **kwargs):
        norms = PaymentNorm.objects.all().order_by('lower_limit')
        for norm in norms:
            if norm.upper_limit == 0 and norm.lower_limit <= self.salary:
                if norm.amount_to_pay > 0:
                    self.share = norm.amount_to_pay
                    self.norm = norm
                else:
                    self.norm = norm
                    self.share = self.salary * norm.percent / 100
                break
            elif self.salary >= norm.lower_limit and self.salary <= norm.upper_limit:
                if norm.amount_to_pay > 0:
                    self.norm = norm
                    self.share = norm.amount_to_pay
                else:
                    self.norm = norm
                    self.share = self.salary * norm.percent / 100
                break
        super().save(*args, **kwargs)
        declarations_query = PaymentDeclaration.objects.filter(
            militant=self.militant, year=self.year, month=self.month).order_by('-year', '-month', '-declaration_date')
        if len(declarations_query) > 1:
            payments = declarations_query[1].payments.all()
            for pay in payments:
                Payment.objects.create(
                    payment_declaration=self, payment_date=pay.payment_date, amount=pay.amount)

    class Meta:
        db_table = 'payment_declaration'
        # unique_together = ['declaration_date', 'militant', 'id']

    def __str__(self) -> str:
        return self.militant.name + " salary of " + str(self.salary)


class Payment(models.Model):
    payment_declaration = models.ForeignKey(
        PaymentDeclaration, related_name='payments', on_delete=models.CASCADE)
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
