import os


# Analyze 컴포넌트의 에러
class GetDataError(Exception):
    def __init__(self, path, message):
        self.path = os.path.basename(path).replace('.xlsx', '')
        self.message = message
        self.type = "채점 오류"

    def __str__(self):
        return self.message


class GetExamDataError(GetDataError):
    """정답 및 배점 엑셀 파일에서 값을 가져올 때 생기는 에러 """


class GetStudentsDataError(GetDataError):
    """학생 제출 엑셀 파일에서 값을 가져올 때 생기는 에러 """


# Util 컴포넌트의 에러
class ExcelNotClosedError(Exception):
    def __init__(self, path):
        self.path = path
        self.message = "열려 있는 모의고사를 닫아 주세요."
        self.type = "채점 오류"

    def __str__(self):
        return self.message


class WrongFileNameError(Exception):
    def __init__(self, path):
        self.path = path
        self.type = "잘못된 파일명"
        self.message = "잘못된 이름을 입력하였습니다.($, % 등 특수 문자 사용 불가)"
