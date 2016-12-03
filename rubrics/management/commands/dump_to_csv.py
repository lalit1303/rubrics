from django.core.management import BaseCommand
from rubrics.models.rubric import RubricLevel1
import csv
from optparse import make_option


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--dump-file',
            action='store',
            default=None,
            dest='out_file',
            help='file path to read from'
        ),
    )

    def handle(self, *args, **kwargs):
        out_file = kwargs['out_file']
        if out_file is None:
            raise Exception('please enter the file name to dump data')
        level1s = RubricLevel1.objects.all()
        level1s = level1s.prefetch_related(
            'level2_mappings__level3_mappings'
        )
        with open(out_file, 'wb') as csvfile:
            fwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            fwriter.writerow(['Level 1', 'Level 2', 'Level 3', 'Max Marks'])
            templ1 = ''
            templ2 = ''
            templ3 = ''
            templ4 = ''
            for l1 in level1s:
                templ1 = l1.name
                fwriter.writerow([templ1, templ2, templ3, templ4])
                for l2 in l1.level2_mappings.all():
                    templ2 = l2.name
                    fwriter.writerow([templ1, templ2, templ3, templ4])
                    for l3 in l2.level3_mappings.all():
                        templ3 = l3.name
                        templ4 = l3.max_marks
                        fwriter.writerow([templ1, templ2, templ3, templ4])
