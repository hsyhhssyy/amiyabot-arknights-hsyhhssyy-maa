from amiyabot.log import LoggerManager

class MaaLogger:
    def __init__(self):
        self.logger = LoggerManager('MaaAdpt')
        self.bot = None

    def info(self,message:str):
        if self.bot == None:
            self.logger.info(f'{message}')
        
        show_log = self.bot.get_config("show_log")
        if show_log == True:
            self.logger.info(f'{message}')

log = MaaLogger()