import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
import time


class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyPythonService"
    _svc_display_name_ = "My Python Service"
    _svc_description_ = "A sample Python service that logs a message every 10 seconds."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._setup_logging()
        self.is_running = True

    @staticmethod
    def _setup_logging():
        logger = logging.getLogger('[MyPythonService]')
        # handler = logging.FileHandler('C:\\path\\to\\your\\logfile.log')  # Specify your log file path
        handler = logging.FileHandler('C:\\logfile.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def SvcStop(self):
        self.logger.info('Service is stopping...')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.logger.info('Service is starting...')
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        while self.is_running:
            self.logger.info('Service is running...')
            time.sleep(10)
        self.logger.info('Service has stopped.')


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
