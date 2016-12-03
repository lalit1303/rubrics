from django.core.management import BaseCommand
from optparse import make_option
from rubrics.models.rubric import RubricLevel1, QuizSubmission, RubricStudentScoreMapping


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--query',
            action='store',
            default=None,
            dest='query_id',
            help='query id to run'
        ),
    )

    def handle(self, *args, **kwargs):
        query_id = kwargs['query_id']
        if query_id is None:
            raise Exception('pass query id which to run')
        query_id = int(query_id)
        if query_id == 1:
            student_scores = self.query1_2_ops(args)
            for student in student_scores:
                log = 'student - {0} : score - {1}'.format(student['student'], student['score'])
                print log
        elif query_id == 2:
            student_scores = self.query1_2_ops(args)
            score_sum = 0
            count = 0
            for student in student_scores:
                count += 1
                score_sum += int(student['score'])
            print 'Average score: {0}'.format(str(score_sum))
        elif query_id == 3:
            resp = self.query3_ops(args)
            print 'Top 3 rubrics - '
            for x in resp:
                print x[1]

    def query1_2_ops(self, args):
        rubric_name = str(args[0]).strip()
        quiz_identifier = args[1]
        print rubric_name, quiz_identifier
        quiz_submissions = QuizSubmission.objects.filter(quiz_id=quiz_identifier)
        quiz_submission_student_dict = {}
        quiz_submission_ids = []
        for x in quiz_submissions:
            quiz_submission_ids.append(x.id)
            quiz_submission_student_dict[x.id] = x.student_id
        rubric_data = RubricLevel1.objects.filter(name=rubric_name)
        rubric_data = rubric_data.prefetch_related(
            'level2_mappings__level3_mappings__level3_score_mappings'
        )
        all_level2 = rubric_data[0].level2_mappings.all()
        result_data = {}
        for level2 in all_level2:
            all_level3 = level2.level3_mappings.all()
            for level3 in all_level3:
                score_datas = level3.level3_score_mappings.all()
                for score in score_datas:
                    if score.quiz_submission_id in quiz_submission_ids:
                        rd = result_data.get(score.quiz_submission_id)
                        if rd is None:
                            result_data[score.quiz_submission_id] = score.score
                        else:
                            result_data[score.quiz_submission_id] += score.score
        student_scores = []
        for key in result_data.keys():
            student_scores.append({
                'student': quiz_submission_student_dict[key],
                'score': result_data[key]
            })
        return student_scores

    def query3_ops(self, args):
        quiz_id = args[0]
        student_id = args[1]
        quiz_submission_id = QuizSubmission.objects.get(quiz_id=quiz_id, student_id=student_id).id
        rubric_student_mapping = RubricStudentScoreMapping.objects.filter(quiz_submission_id=quiz_submission_id)
        rubric_student_mapping.select_related(
            'rubric3__level2__level1_id'
        )
        rubric_score_map = {}
        for row in rubric_student_mapping:
            l1_id = row.rubric3.level2.level1.id
            score = rubric_score_map.get(l1_id)
            if score is None:
                rubric_score_map[l1_id] = {
                    'id': RubricLevel1.objects.get(id=l1_id).name,
                    'score': row.score
                }
            else:
                rubric_score_map[l1_id]['score'] += row.score

        student_score_list = rubric_score_map.values()
        student_score_list.sort(key=lambda x: x['score'], reverse=True)
        return student_score_list[:3]
