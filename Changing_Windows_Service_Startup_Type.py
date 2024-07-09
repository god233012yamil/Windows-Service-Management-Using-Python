import win32service

def change_service_start_type(service_name: str, start_type: str) -> None:
    """
    Change the startup type of the specified Windows service.

    Parameters
    ----------
    service_name : str
        The name of the service to change the startup type for.
    start_type : str
        The new startup type for the service. Valid values are 'automatic', 
        'manual', and 'disabled'.

    Returns
    -------
    None
    """
    start_type_dict = {
        'automatic': win32service.SERVICE_AUTO_START,
        'manual': win32service.SERVICE_DEMAND_START,
        'disabled': win32service.SERVICE_DISABLED
    }

    if start_type.lower() not in start_type_dict:
        print(f"Invalid start type: {start_type}")
        return

    try:
        scm = win32service.OpenSCManager(None, None, 
                                         win32service.SC_MANAGER_ALL_ACCESS)
        service = win32service.OpenService(scm, service_name, 
                                           win32service.SERVICE_CHANGE_CONFIG)
        win32service.ChangeServiceConfig(
            service,
            win32service.SERVICE_NO_CHANGE,
            start_type_dict[start_type.lower()],
            win32service.SERVICE_NO_CHANGE,
            None,
            None,
            0,
            None,
            None,
            None,
            None
        )
        win32service.CloseServiceHandle(service)
        win32service.CloseServiceHandle(scm)
        print(f"Service '{service_name}' start type changed to '{start_type}'.")
    except Exception as e:
        print(f"Failed to change start type for service '{service_name}': {e}")

if __name__ == "__main__":
    # Example usage
    service_name = "MyPythonService"
    new_start_type = "automatic"
    change_service_start_type(service_name, new_start_type)
