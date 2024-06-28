#考试相关
import json

from flask import Blueprint
from exts import db
from flask import request
from models import choiceQuestionModel, testPaperModel, testingResultModel, userModel
from flask import jsonify



bp = Blueprint('testing', __name__, url_prefix='/testing')

questions_dict0 = {}
answers_dict0 = {}
analysis_dict0 = {}
level_dict0 = {}
knowledge_point_dict0 = {}
question_type_dict0 = []
@bp.route('/', methods=['GET', 'POST'])
# @login_required
def question():
    global questions_dict0
    global answers_dict0
    global analysis_dict0
    global level_dict0
    global knowledge_point_dict0
    global question_type_dict0
    # 如果前端请求考试结果
    if request.method == 'GET':
        test_results = testingResultModel.query.all()
        testpapers = testPaperModel.query.all()
        testpaperCourse = {}
        for testpaper in testpapers:
            testpaperCourse[str(testpaper.paper_id)] = testpaper.course
        records = []

        for test_result in test_results:
            record = {}
            record["id"] = test_result.id
            record["userId"] = test_result.user_id
            record["paperId"] = test_result.paper_id
            record["score"] = test_result.score
            record["course"] = testpaperCourse[str(test_result.paper_id)]
            record["answerSituation"] = test_result.answer_situation
            record["testingTime"] = test_result.testingTime
            records.append(record)
        # print("考试记录：",records)


        def prepare_data(exam_records):
            # 存储转换后的数据
            stacked_line_data = {
                'courses': [],
                'allDates': []  # 存储所有日期的列表，允许重复
            }
            # 用于存储所有日期的集合，如果日期允许重复，这个集合可以是列表
            all_dates_list = []
            # 遍历考试记录数据
            for record in exam_records:
                course = record['course']
                user_id = record['userId']
                score = float(record['score'])  # 转换 Decimal 类型为 float
                testing_time = record['testingTime'].strftime('%Y-%m-%d')

                # 添加日期到列表中，允许重复
                all_dates_list.append(testing_time)

                # 初始化课程数据结构
                course_exists = False
                for course_data in stacked_line_data['courses']:
                    if course_data['course'] == course:
                        course_exists = True
                        # 如果课程已经存在，添加用户数据
                        user_exists = False
                        for user_data in course_data['users']:
                            if user_data['userId'] == user_id:
                                user_data['scores'].append(score)
                                user_data['dates'].append(testing_time)
                                user_exists = True
                                break
                        if not user_exists:
                            # 如果用户不存在，添加新用户数据
                            course_data['users'].append({
                                'userId': user_id,
                                'scores': [score],
                                'dates': [testing_time]
                            })
                        break
                if not course_exists:
                    # 如果课程不存在，添加新课程数据
                    stacked_line_data['courses'].append({
                        'course': course,
                        'users': [{
                            'userId': user_id,
                            'scores': [score],
                            'dates': [testing_time]
                        }]
                    })
            # 由于允许重复，直接使用 all_dates_list 作为 allDates
            stacked_line_data['allDates'] = all_dates_list
            # 如果需要排序，可以对 allDates 进行排序
            stacked_line_data['allDates'].sort()
            # print(stacked_line_data)
            return stacked_line_data


        def prepare_data_for_user(exams_data):
            # 创建一个字典来存储按用户分类的数据
            data_for_per_user = {}
            # 遍历每条考试记录
            for record in exams_data:
                user_id = record['userId']
                course = record['course']
                score = float(record['score'])
                testing_time = record['testingTime'].strftime('%Y-%m-%d')
                # 如果用户ID不在字典中，初始化用户数据
                if user_id not in data_for_per_user:
                    data_for_per_user[user_id] = {
                        'userId': user_id,
                        'courses': {}  # 存储该用户所有课程的数据
                    }
                # 如果课程不在用户课程字典中，初始化课程数据
                if course not in data_for_per_user[user_id]['courses']:
                    data_for_per_user[user_id]['courses'][course] = {
                        'course': course,
                        'scores': [],
                        'dates': []
                    }
                # 将分数和日期添加到相应的课程中
                data_for_per_user[user_id]['courses'][course]['scores'].append(score)
                data_for_per_user[user_id]['courses'][course]['dates'].append(testing_time)
            # 返回处理后的数据
            # print(data_for_per_user)
            return data_for_per_user
        # 调用两个函数
        processed_data = prepare_data_for_user(records)
        stacked_line_chart_data = prepare_data(records)
        # 使用in_()查询多个用户
        userIds = []
        for record in records:
            userIds.append(record['userId'])
        # 使用filter方法和in_函数来过滤用户
        users_query = userModel.query.filter(userModel.id.in_(userIds))
        # 执行查询并获取所有匹配的用户
        users = users_query.all()
        userUserName = {}
        for user in users:
            userUserName[str(user.id)] = user.username
        # 返回 JSON 格式的题目数据
        return jsonify({'code': 200, 'records': records,'dataForPerCourse': stacked_line_chart_data,
                        'dataForPerUser': processed_data, 'userUserName': userUserName}), 200

        # 如果前端还没有输入要测试的试卷id:
        # return render_template('testing.html')


    if request.method == 'POST':
        # 如果前端请求的是试卷id
        if 'isFetchTestingPaperIds' in request.get_json():
            testingPaperIds = []
            testPapers = testPaperModel.query.with_entities(testPaperModel.paper_id).all()
            for testPaper in testPapers:
                testingPaperIds.append(testPaper.paper_id)
#             print("传回前端的试卷id:",testingPaperIds)
            return jsonify({'code': 200, 'testingPaperIds': testingPaperIds}), 200


        if 'fetchScoreDate' in request.get_json():
            testingResults = testingResultModel.query.all()
            scoreDate = []
            for testingResult in testingResults:
                scoreDate0 = {}
                time_str = str(testingResult.testingTime)
                score_str = str(testingResult.score)
#                 print(time_str)
                scoreDate0["date"] = time_str
                scoreDate0["score"] = score_str
                scoreDate.append(scoreDate0)
#             print(scoreDate)
#             print(scoreDate[0]["date"],scoreDate[0]["score"])
            return jsonify({'code': 200, 'scoreDate': scoreDate}), 200


        # 如果前端请求的是试卷
        if 'paperId' in request.get_json() and 'answers' not in request.get_json():
            data = request.get_json()
            paper_id = int(data.get('paperId'))
            # print("试卷id：",paper_id)
            info = choiceQuestionModel.query.all()
            questions = {}
            for i in info:
                question = {}
                options_str = i.option
                # 在视图函数中处理数据
                options_list = options_str.split('\n')
                question.update({'id': i.id})
                question.update({'question': i.question})
                question.update({'options': options_list})
                question.update({'course': i.course})
                question.update({'answer': i.answer})
                question.update({'analysis': i.analysis})
                question.update({'level': i.level})
                question.update({'knowledge_point': i.knowledge_point})
                question.update({'question_type': i.type})
                questions[i.id] = question
            # print(questions)

            # print(paper_id)
            test_paper = testPaperModel.query.filter_by(paper_id=paper_id).first()
            course = test_paper.course
            question_ids = test_paper.question_id.split(',')
            question_ids_int = [int(i) for i in question_ids]
            paper = {}
            paper['paper_id'] = test_paper.paper_id
            paper['course'] = course
            questions_dict = {}
            answers_dict = {}
            analysis_dict = {}
            level_dict = {}
            knowledge_point_dict = {}
            question_type_dict = {}
            for i in question_ids_int:
                question_id_str = str(questions[i].get('id'))
                questions_dict[question_id_str] = questions[i]
                answers_dict[question_id_str] = questions[i].get('answer')
                analysis_dict[question_id_str] = questions[i].get('analysis')
                level_dict[question_id_str] = questions[i].get('level')
                knowledge_point_dict[question_id_str] = questions[i].get('knowledge_point')
                question_type_dict[question_id_str] = questions[i].get('question_type')
            questions_dict0 = questions_dict
            answers_dict0 = answers_dict
            analysis_dict0 = analysis_dict
            level_dict0 = level_dict
            knowledge_point_dict0 = knowledge_point_dict
            question_type_dict0 = question_type_dict

            # print("题目字典", questions_dict)
            # print(answers_list)
            return jsonify({'code': 200, 'questions': questions_dict, "course": course, "paperId": paper_id}), 200
        # 如果前端提交了答案，进行验证后返回结果
        if 'answers' in request.get_json():
            # print(len(questions_dict0))
            data = request.get_json()
            paper_id = int(data.get('paperId'))
            test_paper = testPaperModel.query.filter_by(paper_id=paper_id).first()
            user = data['user']
            # print(user)
            answers = data['answers']
            results = {}
            answer_situations = []
            number = len(questions_dict0)
            scorePerQuestion = test_paper.score_per_question
            scorePerChoiceQuestion = '0'
            scorePerJudgmentQuestion = '0'
            if scorePerQuestion["0"] != None:
                scorePerChoiceQuestion = scorePerQuestion["0"]
            if scorePerQuestion["1"] != None:
                scorePerJudgmentQuestion = scorePerQuestion["1"]
            countForChoiceQuestion = 0
            countForJudgmentQuestion = 0
            for answer in answers.items():

                result = {}
                answer_situation = {}
                # 计数答对的题目数量
                # print("答案字典：",analysis_dict0)

                result['correctAnswer'] = answers_dict0[answer[0]]
                result['analysis'] = analysis_dict0[answer[0]]
                answer_situation["questionId"] = questions_dict0[answer[0]]["id"]
                answer_situation["chosen"] = answer[1]
                answer_situation["correctAnswer"] = answers_dict0[answer[0]]
                if answers[str(answer[0])] == answers_dict0[answer[0]]:
                    # print(2)
                    # 如果答对的是选择题
                    if questions_dict0[str(answer[0])]["question_type"] == "0":
                        countForChoiceQuestion = countForChoiceQuestion + 1
                        answer_situation["score"] = scorePerChoiceQuestion
                    # 如果答对的是判断题
                    else:
                        countForJudgmentQuestion = countForJudgmentQuestion + 1
                        answer_situation["score"] = scorePerJudgmentQuestion
                    result['message'] = '哟哟哟，答对了呢~这就是高手？也太厉害了吧！'
                    result['correct'] = 'true'
                    answer_situation["correct"] = "true"
                # 如果没有答对
                else:
                    result['message'] = '小菜鸡，答错了呢~菜就得多练哦！'
                    result['correct'] = 'false'
                    # print(questions_dict0[answer[0]]["id"])
                    answer_situation["correct"] = "false"
                    answer_situation["score"] = 0
                answer_situations.append(answer_situation)
                results[str(answer[0])] = result
            score = float(scorePerChoiceQuestion) * countForChoiceQuestion + float(scorePerJudgmentQuestion) * countForJudgmentQuestion
            results["score"] = str(score)
            # print(results)

            testing_result = testingResultModel(user_id=user["id"], paper_id=paper_id, score=score, answer_situation=answer_situations)
            db.session.add(testing_result)
            db.session.commit()

            return jsonify({'code': 200, 'results': results}), 200

            # print(results)
            # print(answers)

