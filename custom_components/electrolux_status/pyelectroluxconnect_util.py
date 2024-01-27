from pyelectroluxocp import OneAppApi


class pyelectroluxconnect_util:
    @staticmethod
    def get_session(username, password, language ="eng") -> OneAppApi:
        return OneAppApi(username, password)

