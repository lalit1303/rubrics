from django.core.management import BaseCommand
from optparse import make_option
import csv
from rubrics.modules.rubric_level import RubricLevel
from rubrics.models.rubric import RubricLevel1, RubricLevel2, RubricLevel3
from django.db.utils import IntegrityError


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--read-file',
            action='store',
            default=None,
            dest='source_file',
            help='file path to read from'
        ),
    )

    def handle(self, *args, **kwargs):
        source_file = kwargs['source_file']
        if source_file is None:
            raise Exception('please enter the file name to read data from')
        level_data = {}
        with open(source_file, 'rb') as csv_file:
            line = csv.reader(csv_file, delimiter=',', quotechar='"')
            next(line)
            for row in line:
                rl = RubricLevel(row)
                if rl.level_name == 1:
                    level_data[rl.l1] = {}
                if rl.level_name == 2:
                    level_data[rl.l1][rl.l2] = []
                if rl.level_name == 3:
                    temp_data = {
                        'key': rl.l3,
                        'max_marks': rl.max_marks
                    }
                    level_data[rl.l1][rl.l2].append(temp_data)
        for x in level_data.keys():
            self.put_level_data_in_db(x, level_data[x])

    def put_level_data_in_db(self, level1_key, level1_data):
        try:
            rub_l1 = RubricLevel1()
            rub_l1.name = level1_key
            rub_l1.save()
        except IntegrityError:
            rub_l1 = RubricLevel1.objects.get(name=level1_key)
        for x in level1_data.keys():
            level2_key = x
            try:
                rub_l2 = RubricLevel2()
                rub_l2.name = level2_key
                rub_l2.level1 = rub_l1
                rub_l2.save()
            except IntegrityError:
                rub_l2 = RubricLevel2.objects.get(name=level2_key)
            level2_data = level1_data[x]
            for y in level2_data:
                try:
                    level3_key = y['key']
                    max_marks = y['max_marks']
                    rub_l3 = RubricLevel3()
                    rub_l3.name = level3_key
                    rub_l3.max_marks = max_marks
                    rub_l3.level2 = rub_l2
                    rub_l3.save()
                except IntegrityError:
                    pass
