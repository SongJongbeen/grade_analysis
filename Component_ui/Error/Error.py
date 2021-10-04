import os


class Error(Exception):
    def __init__(self, path='', type='', message=''):
        self.path = path
        self.message = message
        self.type = type


# Analyze 컴포넌트의 에러
class GetDataError(Error):
    def __init__(self, path, message):
        super(GetDataError, self).__init__(
            path=os.path.basename(path).replace('.xlsx', ''),
            type="채점 오류",
            message=message
        )


class GetExamDataError(GetDataError):
    """정답 및 배점 엑셀 파일에서 값을 가져올 때 생기는 에러 """


class GetStudentsDataError(GetDataError):
    """학생 제출 엑셀 파일에서 값을 가져올 때 생기는 에러 """


# Util 컴포넌트의 에러
class ExcelNotClosedError(Error):
    def __init__(self, path):
        super(ExcelNotClosedError, self).__init__(
            path=path,
            type="채점오류",
            message="열려 있는 파일을 닫아 주세요."
        )


class WrongFileNameError(Error):
    def __init__(self, path):
        super(WrongFileNameError, self).__init__(
            path=path,
            type="잘못된 파일명 오료",
            message="잘못된 이름을 입력하였습니다.(\\ , / 의 문자가 파일 명에 들어감)"
        )


class FileExistsError(Error):
    def __init__(self, path):
        super(FileExistsError, self).__init__(
            path=path,
            type="파일 존재 오류",
            message="해당 파일이 이미 존재합니다."
        )


class NotScoredError(Error):
    def __init__(self):
        super(NotScoredError, self).__init__(
            path='',
            type='분석 열람 오류',
            message="채점을 먼저 진행해 주세요!"
        )
