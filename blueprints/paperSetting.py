#组卷
from flask import Blueprint
from sqlalchemy.exc import IntegrityError

from exts import db
from flask import request
from models import choiceQuestionModel, testPaperModel

from flask import jsonify
import random
#（固定，固定，url前缀）
bp = Blueprint('paperSetting', __name__, url_prefix='/paperSetting')

@bp.route('/', methods=['GET', 'POST', 'DELETE'])
def paperSetting():
    if request.method == 'GET':
        testPaperRecords = testPaperModel.query.all()
        # courses0是元组：('python',)这样的形式
        courses0 = choiceQuestionModel.query.with_entities(choiceQuestionModel.course).distinct().all()
        # print(courses0)
        courses = [course[0] for course in courses0]
        # print("课程查询结果为：",courses)

        testPapers = []
        for testPaperRecord in testPaperRecords:
            testPaper = {}
            testPaper["paperId"] = testPaperRecord.paper_id
            testPaper["course"] = testPaperRecord.course
            testPaper["questionId"] = testPaperRecord.question_id
            testPapers.append(testPaper)

        info = choiceQuestionModel.query.all()
        questions = []
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
            question.update({'knowledgePoint': i.knowledge_point})
            questions.append(question)
        # print("题目列表：", questions)

        return jsonify({"code": 200, "testingPapers": testPapers, "courses": courses, "questions": questions}), 200

    if request.method == 'POST':
        data = request.get_json()
        print("前端传回数据：",data)

        # 如果本次请求是为了随机组卷
        if 'scorePerQuestion' in data and 'isAdd' not in data:
            course = data['course']
            scorePerQuestion = data['scorePerQuestion']
            choiceQuestionIds1 = None
            judgmentQuestionIdsStr = None
            judgmentQuestionIds1 = None
            choiceQuestionIdsStr = None
            choiceQuestionIds = None
            judgmentQuestionIds = None
            if "0" in data["level"]:
                choiceQuestionLevel = data["level"]["0"]
                choiceQuestionIds = []
                choiceQuestionIds0 = choiceQuestionModel.query.filter_by(course=course, type="0",
                                                                         level=choiceQuestionLevel).all()
                for choiceQuestionId in choiceQuestionIds0:
                    choiceQuestionIds.append(choiceQuestionId.id)
                    # print(choiceQuestionIds)
                    # 随机选择的各类题目的数量
                choiceQuestionNum = int(data['questionNum']['0'])
                # 使用sample函数随机选择题目序号
                choiceQuestionIds1 = random.sample(choiceQuestionIds, min(choiceQuestionNum, len(choiceQuestionIds)))
                # 将选中的题目序号以逗号分隔的方式连接成一个字符串
                choiceQuestionIdsStr = ','.join(map(str, choiceQuestionIds1))
            if "1" in data["level"]:
                judgmentQuestionLevel = data["level"]["1"]
                judgmentQuestionIds = []
                judgmentQuestionIds0 = choiceQuestionModel.query.filter_by(course=course, type="1",level=judgmentQuestionLevel).all()
                for choiceQuestionId in judgmentQuestionIds0:
                    judgmentQuestionIds.append(choiceQuestionId.id)
            # print(judgmentQuestionIds)
            # 随机选择的各类题目的数量
                judgmentQuestionNum = int(data['questionNum']['1'])
                # 使用sample函数随机选择题目序号
                judgmentQuestionIds1 = random.sample(judgmentQuestionIds, min(judgmentQuestionNum, len(judgmentQuestionIds)))
                # 将选中的题目序号以逗号分隔的方式连接成一个字符串
                judgmentQuestionIdsStr = ','.join(map(str, judgmentQuestionIds1))

            # 确定最终的 questionIds 字符串
            if not choiceQuestionIds1:  # 空列表转换为字符串是空字符串
                questionIds = judgmentQuestionIdsStr
            elif not judgmentQuestionIds1:
                questionIds = choiceQuestionIdsStr
            else:
                questionIds = f"{choiceQuestionIdsStr},{judgmentQuestionIdsStr}".strip(',')

            # 创建试卷并保存到数据库
            testPaper = testPaperModel(course=course, question_id=questionIds, score_per_question=scorePerQuestion)
            db.session.add(testPaper)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()  # 发生异常时回滚
                print("创建试卷失败：", e)
                return jsonify({"code": 500, "error": "创建试卷失败"})

            print("选择题id：", choiceQuestionIds, "判断题id:", judgmentQuestionIds)
            return jsonify({"code": 200}), 200


        # 如果这次是请求试卷详情
        if 'paperId' in data:
            paperId = str(data['paperId'])
            questionIdsStr = data['questionIds']
            questionIds = questionIdsStr.split(',')
            print("前端传来的题目id:", questionIds)
            print(paperId)
            testingPaper = testPaperModel.query.filter_by(paper_id=paperId).first()
            print(testingPaper)
            choicequestions = choiceQuestionModel.query.filter(choiceQuestionModel.id.in_(questionIds)).all()
            scorePerQuestion = testingPaper.score_per_question
            questions = []
            for choicequestion in choicequestions:
                question = {}
                question["id"] = choicequestion.id
                question["question"] = choicequestion.question
                optionsList = choicequestion.option.split('\n')
                question["options"] = optionsList
                question["answer"] = choicequestion.answer
                question["analysis"] = choicequestion.analysis
                question["knowledgePoint"] = choicequestion.knowledge_point
                question["level"] = choicequestion.level
                question["type"] = choicequestion.type
                questions.append(question)
            # print(questions)
            print("每题分数：",scorePerQuestion)

            return jsonify({"code": 200, "questions": questions, "scorePerQuestion": scorePerQuestion}), 200
        # 如果此次请求是要新增题目
        if 'isAdd' in data:
            scorePerQuestion = data['scorePerQuestion']
            course = data['form']['course']
            if 'choiceQuestionIds' in data['form']:
                choiceQuestionIds = data['form']['choiceQuestionIds']
            else:
                choiceQuestionIds = None
            if 'judgmentQuestionIds' in data['form']:
                judgmentQuestionIds = data['form']['judgmentQuestionIds']
            else:
                judgmentQuestionIds = None
            # 确定最终的 questionIds 字符串
            if not choiceQuestionIds:  # 选择题题号字符串是空字符串
                questionIds = judgmentQuestionIds
            elif not judgmentQuestionIds:   # 判断题题号字符串是空字符串
                questionIds = choiceQuestionIds
            else:
                questionIds = f"{choiceQuestionIds},{judgmentQuestionIds}".strip(',')
            if data['isAdd'] == 'true':
                choiceQuestion = testPaperModel(course=course, question_id=questionIds, score_per_question=scorePerQuestion)
                db.session.add(choiceQuestion)
                db.session.commit()
                return jsonify({"code": 200}), 200
            # 如果不是新增，就是修改试卷信息
            else:
                paperId = data['form']['paperId']
                choiceQuestion = testPaperModel.query.filter_by(paper_id=paperId).first()
                choiceQuestion.question_id = questionIds
                choiceQuestion.course = course
                db.session.add(choiceQuestion)
                db.session.commit()
                return jsonify({"code": 200}), 200
    if request.method == 'DELETE':
        data = request.get_json()
        print("前端删除时传回数据：", data)

        try:
            # 尝试获取要删除的记录
            testpaper = testPaperModel.query.filter_by(paper_id=data["paperId"]).first()
            if testpaper is None:
                return jsonify({"code": 404, "message": "未找到指定的试卷"}), 404

            # 执行删除操作
            db.session.delete(testpaper)
            db.session.commit()

            # 返回成功的响应
            return jsonify({"code": 200, "message": "删除成功"}), 200

        except IntegrityError as e:
            # 捕获由于外键约束导致的错误
            db.session.rollback()  # 回滚会话，以撤销部分更改

            # 返回外键约束错误的消息
            return jsonify({"code": 409, "message": "删除失败，存在外键约束"}), 409
        except Exception as e:
            # 捕获其他可能的错误
            db.session.rollback()

            # 返回一个通用错误消息
            return jsonify({"code": 500, "message": "内部服务器错误"}), 500






        


