import config,requests,pickle

class login():
    def __init__(self):
        self.user = config.user
        self.headers = config.common_headers
        self.data = config.user
        self.url = config.urls['doLogin']

    def saveCookie(self):

        response = requests.post(self.url , data = self.data , headers = self.headers)

        if response.ok:
            with open('cookies.jar','wb') as f:
                pickle.dump(requests.utils.dict_from_cookiejar(response.cookies),f)
            # login  success
            return True
        #login  error
        return False

    def getCookie(self):

        with open('cookies.jar','rb') as f:
            content = pickle.load(f)

        cookies = requests.utils.cookiejar_from_dict(content)

        return cookies