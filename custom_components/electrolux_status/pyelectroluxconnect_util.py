import pyelectroluxconnect


class pyelectroluxconnect_util:
    @staticmethod
    def get_session(username, password, region="emea", language ="eng"):
        return pyelectroluxconnect.Session(
            username, password, deviceId="ElectroluxHomeAssistant", language=language, region=region,
        )
