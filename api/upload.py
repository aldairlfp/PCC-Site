import csv
from cv2 import add

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

fs = FileSystemStorage(location='tmp/')


class UploadData_APIView(APIView):
    def get_queryset(self):
        Militant.objects.none
        Address.objects.none
        return Core.objects.all()

    def post(self, request, format=None):
        # try:
        file = request.FILES['file']

        content = file.read()

        file_content = ContentFile(content)
        file_name = fs.save('_tmp.csv', file_content)
        tmp_file = fs.path(file_name)

        csv_file = open(tmp_file, errors='ignore')
        reader = csv.reader(csv_file)
        next(reader)

        line = next(reader)
        province = line[0][11:]
        municipality = line[4][11:]
        district = line[16][10:]

        line = next(reader)
        name = line[0][8:]
        code = line[2][8:]

        line = next(reader)
        sector = line[0][48:]

        line = next(reader)
        subordinate = line[0][49:]
        core = Core(code=code, name=name, municipality=municipality, province=province,
                    district=district, sector=sector, subordinate=subordinate)

        try:
            core.save()
        except core.DoesNotExist:
            pass

        for i in range(4):
            next(reader)

        militant_list = []
        for id_, row in enumerate(reader):
            ci = row[0]
            name = row[1]
            first_lastname = row[2]
            second_lastname = row[3]
            house_phone = row[37]
            work_phone = row[38]
            cell_phone = row[39]
            email = row [40]
            pcc_position = row[30]
            observations = row[48]
            pcc_reserve_position = row[31]
            institutional_reserve_position = row[32]
            birth_year = row[33]
            age = row[34]
            job = row[19]
            job_clasification = row[20]
            no_ci = row[15]
            fundator = True if row[16] == 1 else False
            skin_color = row[20]
            scolarity = row[22]
            work_file = row[29]
            sex = row[17]
            status = row[28]

            street = row[41]
            apto = row[42]
            corner = row[43]
            neighborhood = row[44]
            municipality = row[45]
            province = row[46]
            # address = Address(street=street, apto=apto, corner_or_ave=corner, neighborhood=neighborhood,
            #                   municipality=municipality, province=province)

            # try:
                # address.save()
            militant = Militant(ci=ci, name=name, first_lastname=first_lastname, second_lastname=second_lastname, core=core, sex=sex, status=status, house_phone=house_phone, work_phone=work_phone, cell_phone=cell_phone, email=email, pcc_position=pcc_position, observations=observations, pcc_reserve_position=pcc_reserve_position, institutional_reserve_positon=institutional_reserve_position, birth_year=birth_year, age=age, job=job, job_clasification=job_clasification, no_ci=no_ci, fundator=fundator, skin_color=skin_color, scolarity=scolarity, work_file=work_file)
            # except ValueError:
            #     if address.exist:
            #         address = address.find()[0]
            #         militant = Militant(ci=ci, address=address, name=name, first_lastname=first_lastname, second_lastname=second_lastname, core=core, sex=sex, status=status, house_phone=house_phone, work_phone=work_phone, cell_phone=cell_phone, email=email, pcc_position=pcc_position, observations=observations, pcc_reserve_position=pcc_reserve_position, institutional_reserve_positon=institutional_reserve_position, birth_year=birth_year, age=age, job=job, job_clasification=job_clasification, no_ci=no_ci, fundator=fundator, skin_color=skin_color, scolarity=scolarity, work_file=work_file)
            #     else:
            #         militant = Militant(ci=ci, name=name, first_lastname=first_lastname, second_lastname=second_lastname, core=core, sex=sex, status=status, house_phone=house_phone, work_phone=work_phone, cell_phone=cell_phone, email=email, pcc_position=pcc_position, observations=observations, pcc_reserve_position=pcc_reserve_position, institutional_reserve_positon=institutional_reserve_position, birth_year=birth_year, age=age, job=job, job_clasification=job_clasification, no_ci=no_ci, fundator=fundator, skin_color=skin_color, scolarity=scolarity, work_file=work_file)

            try:
                militant.save()
            except militant.DoesNotExist:
                pass
            except ValueError:
                pass

        # fs.delete(file_name)
        return Response({'detail': 'Succesfully uploaded the data'})
        # except Exception as e:
        #     return Response({'detail': 'Error uploading the data'}, status=status.HTTP_400_BAD_REQUEST)
