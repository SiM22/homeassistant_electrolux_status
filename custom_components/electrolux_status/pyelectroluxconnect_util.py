import pyelectroluxconnect


class pyelectroluxconnect_util:
    @staticmethod
    def get_session(username, password):
        return pyelectroluxconnect.Session(username, password, tokenFileName=".electrolux-token", country="US",
                                          language=None, deviceId="ElectroluxHomeAssistant", raw=False, verifySsl=True)
