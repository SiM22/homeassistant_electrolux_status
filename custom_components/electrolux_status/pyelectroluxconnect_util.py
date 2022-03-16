import pyelectroluxconnect


class pyelectroluxconnect_util:
    @staticmethod
    def get_session(username, password, region="emea"):
        return pyelectroluxconnect.Session(username,
                                           password,
                                           deviceId="ElectroluxHomeAssistant",
                                           region=region)
