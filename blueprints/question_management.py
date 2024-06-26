from flask import Blueprint, request,jsonify,make_response
from models import choiceQuestionModel
from exts import db
from sqlalchemy.sql import func
import pandas as pd
from io import BytesIO
#qa的蓝图，用来写视图
bp = Blueprint('question_management', __name__, url_prefix='/question_management')

# 渲染题库到前端，对应load方法
@bp.route("/returnquestions", methods=['GET'])
def returnquestion():
    try:
        questions = choiceQuestionModel.query.filter_by(type='0').all()
        responseBody1 = {
            'data': [{
        'id': question.id,
        'question': question.question,
        'option1': question.option.split('\n')[0],
        'option2': question.option.split('\n')[1],
        'option3': question.option.split('\n')[2],
        'option4': question.option.split('\n')[3],
        'answer': question.answer,
        'analysis': question.analysis,
        'course': question.course,
        'knowledge_point': question.knowledge_point,
        'level':question.level

    } for question in questions]
        }
        questions_new = choiceQuestionModel.query.filter_by(type='1').all()
        responseBody2 = {
            'data': [{
                'id': question.id,
                'question': question.question,
                'answer': question.answer,
                'analysis': question.analysis,
                'course': question.course,
                'knowledge_point': question.knowledge_point,
                'level': question.level
            } for question in questions_new]
        }
        responseBody={'data1': responseBody1, 'data2': responseBody2}
        return make_response(jsonify(responseBody)), 200
    except Exception as e:
        # 这里可以根据需要记录日志
        return make_response(jsonify({'error': 'An error occurred', 'message': str(e)})), 500

@bp.route("/deletequestion", methods=['DELETE'])
def deletequestion():
    response_object = {'status': 'fail', 'message': ''}
    if request.method == 'DELETE':
        post_data = request.get_json()
        # print('调用删除试题方传过来的参数是：', post_data)
        id = post_data.get('id')
        question = choiceQuestionModel.query.filter_by(id=id).first()
        if question:
            db.session.delete(question)  # 修正：使用 delete()
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = '删除成功!'
        else:
            response_object['message'] = '删除失败，题号不存在!'
    else:
        response_object['message'] = '请求方法不正确'
    return jsonify(response_object)  # 确保返回 JSON 响应


# 编辑试题接口，包括增加和编辑
@bp.route("/editquestion",methods=['POST'])
def editquestion():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        # print('调用编辑试题方法传过来的参数是：', post_data)
        question = post_data.get('question')
        option1 = post_data.get('option1')
        option2 = post_data.get('option2')
        option3 = post_data.get('option3')
        option4 = post_data.get('option4')
        option=option1+'\n'+option2+'\n'+option3+'\n'+option4
        answer = post_data.get('answer')
        analysis = post_data.get('analysis')
        course = post_data.get('course')
        knowledge_point = post_data.get('knowledge_point')
        level = str(post_data.get('level'))
        type='0'
        if level not in ('0', '1', '2', '3', '4', '5'):
            response_object['message'] = '难度格式错误,难度值只能是0~5!'
            response_object["status"] = 'fail'
            return response_object
        elif answer not in (option1, option2, option3, option4):
             response_object['message'] = '答案格式错误,请保持答案与正确选项相对应(注意：答案应是某个选项的具体数值而非其的编号)!'
             response_object["status"] = 'fail'
             return response_object
        else:
            if  'id' not in post_data:
                Question = choiceQuestionModel(question=question, option=option, answer=answer,
                                 analysis=analysis, course=course, knowledge_point=knowledge_point,level=level, type=type)
                db.session.add(Question)
                db.session.commit()
                response_object['message'] = '添加成功!'
                response_object["status"] = 'success'
                return response_object
            else:
                id = post_data.get('id')
                Question = choiceQuestionModel.query.filter_by(id=id).first()
                Question.question = question
                Question.option = option
                Question.answer = answer
                Question.analysis = analysis
                Question.course = course
                Question.knowledge_point = knowledge_point
                Question.level = level
                Question.type = type
                db.session.commit()
                response_object['message'] = '修改成功!'
                response_object["status"] = 'success'
                return response_object
@bp.route("/editquestion_new",methods=['POST'])
def editquestion_new():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        # print('调用编辑试题方法传过来的参数是：', post_data)
        question = post_data.get('question')
        option ='正确\n错误'
        answer = post_data.get('answer')
        analysis = post_data.get('analysis')
        course = post_data.get('course')
        knowledge_point = post_data.get('knowledge_point')
        level = str(post_data.get('level'))
        type='1'
        if level not in ('0', '1', '2', '3', '4', '5'):
            response_object['message'] = '难度格式错误,难度值只能是0~5!'
            response_object["status"] = 'fail'
            return response_object
        elif answer not in ('正确','错误'):
             response_object['message'] = '答案格式错误,答案应是正确或错误!'
             response_object["status"] = 'fail'
             return response_object
        else:
            if  'id' not in post_data:
                Question = choiceQuestionModel(question=question, option=option, answer=answer,
                                 analysis=analysis, course=course, knowledge_point=knowledge_point,level=level, type=type)
                db.session.add(Question)
                db.session.commit()
                response_object['message'] = '添加成功!'
                response_object["status"] = 'success'
                return response_object
            else:
                id = post_data.get('id')
                Question = choiceQuestionModel.query.filter_by(id=id).first()
                Question.question = question
                Question.option = option
                Question.answer = answer
                Question.analysis = analysis
                Question.course = course
                Question.knowledge_point = knowledge_point
                Question.level = level
                Question.type = type
                db.session.commit()
                response_object['message'] = '修改成功!'
                response_object["status"] = 'success'
                return response_object

@bp.route('/analysis_bank', methods=['GET'])
def analysis_bank():
    try:
        # 查询不同种类的试题数量
        course_stats = choiceQuestionModel.query.with_entities(
            choiceQuestionModel.course,
            func.count(choiceQuestionModel.id)
        ).group_by(choiceQuestionModel.course).all()

        # 查询不同种类的试题的平均难度
        level_stats = choiceQuestionModel.query.with_entities(
            choiceQuestionModel.course,
            func.avg(choiceQuestionModel.level)
        ).group_by(choiceQuestionModel.course).all()

        # 准备返回的数据结构
        result = {
            'course_stats': [{'name': course, 'value': count} for course, count in course_stats],
            'level_stats': [{'course': course, 'average_level': avg} for course, avg in level_stats]
        }
        # print(result)
        return jsonify(result), 200

    except Exception as e:
        # 错误处理
        return jsonify({'error': str(e)}), 500

# 导出试题
@bp.route('/export_questions', methods=['GET'])
def export_questions():
    # 查询数据
    questions = choiceQuestionModel.query.all()
    for question in questions:
        question.option=question.option.replace("\n","   ")
    # 准备数据用于 DataFrame
    data = []
    for question in questions:
        row = {column.name: getattr(question, column.name) for column in question.__table__.columns}
        data.append(row)

    # 将数据转换为 DataFrame
    df = pd.DataFrame(data)

    # 将 DataFrame 写入 Excel 文件
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')

    # 重置 BytesIO 对象的指针到开始位置
    output.seek(0)

    # 设置响应头和内容类型
    response = make_response(output.read())
    response.headers.set('Content-Disposition', 'attachment', filename='questions.xlsx')
    response.headers.set('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    return response


@bp.route('/import_questions',methods=['POST'])
def import_questions():
    response_object = {'status': 'success'}
    if 'file' not in request.files:
        response_object['message'] = '导入失败,没有识别到文件!'
        response_object["status"] = 'fail'
        return response_object

    file = request.files['file']
    if file.filename == '':
        response_object['message'] = '导入失败，文件不存在!'
        response_object["status"] = 'fail'
        return response_object

    # 解析 Excel 文件
    try:
        data = pd.read_excel(file)
    except:
        response_object['message'] = '导入失败，文件格式错误，解析失败!'
        response_object["status"] = 'fail'
        return response_object

    # 验证数据（根据您模型的需要进行调整）
    if not data.columns.tolist() == ['question', 'option', 'answer', 'analysis', 'course', 'knowledge_point', 'level', 'type']:
        response_object['message'] = '导入失败，文件数据不符合规范!'
        response_object["status"] = 'fail'
        return response_object

    # 保存到数据库
    try:
        for index, row in data.iterrows():
            # 根据需要转换数据类型或处理数据
            question = choiceQuestionModel(
                question=row['question'],
                option=row['option'],
                answer=row['answer'],
                analysis=row['analysis'],
                course=row['course'],
                knowledge_point=row['knowledge_point'],
                level=row['level'],
                type=row['type'],

            )
            # 添加到数据库会话
            # print(question)
            db.session.add(question)
        # # 提交事务
        db.session.commit()
    except:
        db.session.rollback()  # 如果出现错误，回滚事务
        response_object['message'] = "导入失败，文件数据导入数据库失败，请重新尝试!"
        response_object["status"] = 'fail'
        return response_object

    response_object['message'] = '导入成功!'
    response_object["status"] = 'success'
    return response_object

